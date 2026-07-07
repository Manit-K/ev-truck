PYTHON=python3
COMPOSE=docker compose

.PHONY: run dev db-up db-down db-logs migrate db-reset check status

run:
	$(PYTHON) -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

dev: run

db-up:
	$(COMPOSE) up -d postgres

db-down:
	$(COMPOSE) down

db-logs:
	$(COMPOSE) logs -f postgres

migrate:
	$(PYTHON) -m alembic upgrade head

# Destructive: stops Compose and permanently deletes the local PostgreSQL data volume.
db-reset:
	$(COMPOSE) down --volumes
	$(COMPOSE) up -d postgres

check:
	$(PYTHON) -m compileall app

status:
	git status
