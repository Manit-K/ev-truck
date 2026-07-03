import hashlib
import json
from datetime import datetime, timezone

import google.auth
from google.oauth2 import service_account
from googleapiclient.discovery import build
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.db.models.import_batch import ImportBatch
from app.repositories.vehicle import VehicleRepository
from app.repositories.vehicle_reading import VehicleReadingRepository
from app.schemas.integration import VehicleReadingImport, normalize_sheet_row


SHEETS_SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


class GoogleSheetConfigurationError(Exception):
    pass


class GoogleSheetSyncService:
    def __init__(self, db: Session, settings: Settings):
        self.db = db
        self.settings = settings
        self.vehicles = VehicleRepository(db)
        self.readings = VehicleReadingRepository(db)

    def sync(self, sheet_id: str | None, sheet_range: str | None) -> ImportBatch:
        resolved_sheet_id = sheet_id or self.settings.google_sheet_id
        resolved_range = sheet_range or self.settings.google_sheet_range
        if not resolved_sheet_id:
            raise GoogleSheetConfigurationError("GOOGLE_SHEET_ID is not configured")

        batch = ImportBatch(
            source="google_sheet",
            status="running",
            sheet_id=resolved_sheet_id,
            sheet_range=resolved_range,
            created_at=datetime.now(timezone.utc),
        )
        self.db.add(batch)
        self.db.commit()
        self.db.refresh(batch)

        try:
            rows = self._read_rows(resolved_sheet_id, resolved_range)
            self._import_rows(batch, rows)
            batch.status = "completed" if batch.failed_rows == 0 else "completed_with_errors"
        except Exception as exc:
            self.db.rollback()
            batch = self.db.get(ImportBatch, batch.id)
            if batch is None:
                raise
            batch.status = "failed"
            batch.error_message = str(exc)[:4000]
            batch.completed_at = datetime.now(timezone.utc)
            self.db.commit()
            raise

        batch.completed_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(batch)
        return batch

    def _credentials(self):
        if self.settings.google_application_credentials:
            return service_account.Credentials.from_service_account_file(
                self.settings.google_application_credentials,
                scopes=SHEETS_SCOPES,
            )
        credentials, _ = google.auth.default(scopes=SHEETS_SCOPES)
        return credentials

    def _read_rows(self, sheet_id: str, sheet_range: str) -> list[list[str]]:
        service = build("sheets", "v4", credentials=self._credentials(), cache_discovery=False)
        response = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=sheet_id, range=sheet_range)
            .execute()
        )
        return response.get("values", [])

    def _import_rows(self, batch: ImportBatch, rows: list[list[str]]) -> None:
        if not rows:
            return

        headers = rows[0]
        data_rows = rows[1:]
        batch.total_rows = len(data_rows)
        errors: list[str] = []

        for row_number, values in enumerate(data_rows, start=2):
            raw_payload = normalize_sheet_row(headers, values)
            try:
                parsed = VehicleReadingImport.model_validate(raw_payload)
                vehicle_id = self._resolve_vehicle_id(parsed)
                record_id = parsed.source_record_id or self._record_hash(raw_payload)
                _, created = self.readings.upsert(
                    {
                        "vehicle_id": vehicle_id,
                        "trip_id": parsed.trip_id,
                        "import_batch_id": batch.id,
                        "source": "google_sheet",
                        "source_record_id": record_id,
                        "recorded_at": parsed.recorded_at,
                        "soc_percent": parsed.soc_percent,
                        "energy_used_kwh": parsed.energy_used_kwh,
                        "distance_km": parsed.distance_km,
                        "latitude": parsed.latitude,
                        "longitude": parsed.longitude,
                        "raw_payload": raw_payload,
                    }
                )
                if created:
                    batch.imported_rows += 1
                else:
                    batch.updated_rows += 1
            except (ValidationError, ValueError) as exc:
                batch.failed_rows += 1
                errors.append(f"row {row_number}: {exc}")

        if errors:
            batch.error_message = json.dumps(errors)[:4000]

    def _resolve_vehicle_id(self, reading: VehicleReadingImport) -> int:
        if reading.vehicle_id is not None:
            vehicle = self.vehicles.get(reading.vehicle_id)
        else:
            vehicle = self.vehicles.get_by_external_id(reading.vehicle_external_id or "")
        if vehicle is None:
            raise ValueError("referenced vehicle does not exist")
        return vehicle.id

    @staticmethod
    def _record_hash(raw_payload: dict) -> str:
        canonical = json.dumps(raw_payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
