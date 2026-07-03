from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.db.session import get_db
from app.schemas.integration import GoogleSheetSyncRequest, ImportBatchRead
from app.services.google_sheet import GoogleSheetConfigurationError, GoogleSheetSyncService


router = APIRouter(prefix="/integrations")


@router.post(
    "/google-sheet/sync",
    response_model=ImportBatchRead,
    status_code=status.HTTP_201_CREATED,
)
def sync_google_sheet(
    data: GoogleSheetSyncRequest,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    try:
        return GoogleSheetSyncService(db, settings).sync(data.sheet_id, data.sheet_range)
    except GoogleSheetConfigurationError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Google Sheet sync failed: {exc}") from exc
