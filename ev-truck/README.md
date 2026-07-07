# EV Truck Optimization API

FastAPI MVP for EV fleet data, trip plan-vs-actual analysis, Google Sheet telemetry import, and rule-based optimization. The application uses PostgreSQL, SQLAlchemy, Alembic, and a Router → Service → Repository structure.

## Local setup

Prerequisites: Python 3.12 and Docker with Docker Compose.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

The development database is managed with Docker Compose. See [Local Development Database](#local-development-database) below.

## Local Development Database

Copy the example environment file, then start PostgreSQL:

```bash
cp .env.example .env
docker compose up -d postgres
docker compose ps
```

For an API running from WSL or the host, use:

```env
DATABASE_URL=postgresql+psycopg2://evtruck:evtruck@localhost:5432/evtruck
```

If the API runs in a Compose container on the same network, use `postgres` as the host instead:

```env
DATABASE_URL=postgresql+psycopg2://evtruck:evtruck@postgres:5432/evtruck
```

Apply migrations and run the API from the host:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

Verify the API (Swagger UI is at <http://localhost:8000/docs>):

```bash
curl http://localhost:8000/health
curl http://localhost:8000/vehicles
curl http://localhost:8000/trips
```

Adminer is optional. Start it alongside PostgreSQL with:

```bash
docker compose up -d postgres adminer
```

Open <http://localhost:8080> and use these login values:

| Field | Value |
|---|---|
| System | PostgreSQL |
| Server | `postgres` |
| Username | `evtruck` |
| Password | `evtruck` |
| Database | `evtruck` |

Stop the local services with `docker compose down`. The named volume keeps database data between runs. `make db-reset` deletes that volume and all local database data.

Equivalent shortcuts are available as `make db-up`, `make db-down`, `make db-logs`, `make migrate`, and `make dev`.

## Environment variables

| Variable | Required | Description |
|---|---:|---|
| `APP_NAME` | No | OpenAPI application title |
| `APP_VERSION` | No | OpenAPI application version |
| `ENV` | No | Runtime environment name |
| `DATABASE_URL` | Yes | PostgreSQL SQLAlchemy URL using the `postgresql+psycopg2` driver |
| `GOOGLE_SHEET_ID` | For sync | Default spreadsheet ID |
| `GOOGLE_SHEET_RANGE` | No | Default A1 range; defaults to `vehicle_readings!A:Z` |
| `GOOGLE_APPLICATION_CREDENTIALS` | Local only | Optional path to a service-account JSON file; do not commit it |

On Cloud Run, Google Application Default Credentials are used when `GOOGLE_APPLICATION_CREDENTIALS` is absent. Grant the Cloud Run service account access to the spreadsheet. Never place database passwords or service-account JSON in the image or repository.

## Database migrations

Apply all migrations:

```bash
alembic upgrade head
```

Create a migration after changing models:

```bash
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

Rollback one revision:

```bash
alembic downgrade -1
```

## Google Sheet import

The first row must contain headers. Supported columns are:

```text
source_record_id, vehicle_id, vehicle_external_id, trip_id, recorded_at,
soc_percent, energy_used_kwh, distance_km, latitude, longitude
```

Either `vehicle_id` or `vehicle_external_id` is required. `recorded_at` must be an ISO-8601 timestamp. `source_record_id` is recommended; when omitted, a deterministic hash of the row is used. The database unique constraint prevents duplicate source records.

Run a sync with configured defaults:

```bash
curl -X POST http://localhost:8000/integrations/google-sheet/sync \
  -H 'Content-Type: application/json' \
  -d '{}'
```

## Cloud Run manual deployment

The production image listens on Cloud Run's `PORT`. Store the database URL in Secret Manager first; for Cloud SQL, its value can use the Unix socket form `postgresql+psycopg2://USER:PASSWORD@/DATABASE?host=/cloudsql/PROJECT:REGION:INSTANCE`.

```bash
gcloud run deploy ev-truck-api \
  --source . \
  --region asia-southeast1 \
  --platform managed \
  --allow-unauthenticated \
  --service-account ev-truck-api@PROJECT_ID.iam.gserviceaccount.com \
  --add-cloudsql-instances PROJECT_ID:asia-southeast1:INSTANCE_NAME \
  --set-secrets DATABASE_URL=ev-truck-database-url:latest \
  --set-env-vars APP_NAME=ev-truck,ENV=production,GOOGLE_SHEET_ID=SHEET_ID,GOOGLE_SHEET_RANGE=vehicle_readings!A:Z
```

Run `alembic upgrade head` against the production database as a controlled release step before sending traffic to a schema-dependent revision. Cloud Run should not run concurrent migrations during container startup.
