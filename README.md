# EV Truck Optimization API

Backend API for **EV Fleet Management**, **Trip Planning**, **Vehicle Telemetry**, **Plan vs Actual Analysis**, and **Fleet Optimization**.

The project is built using **FastAPI**, **SQLAlchemy 2.x**, **PostgreSQL**, and follows a **Clean Architecture** design for maintainability and scalability.

---

# 🚚 Project Overview

Business Flow

```text
LINE
    │
    ▼
n8n OCR
    │
    ▼
Google Sheet
    │
    ▼
Google Sheet Sync API
    │
    ▼
PostgreSQL
    │
    ▼
Plan vs Actual
    │
    ▼
Optimization Engine
    │
    ▼
Recommendation
```

---

# 🏗 Architecture

The backend follows Clean Architecture.

```text
Router
    │
    ▼
Service
    │
    ▼
Repository
    │
    ▼
SQLAlchemy ORM
    │
    ▼
PostgreSQL
```

Project structure

```text
app/
    routers/
    services/
    repositories/
    schemas/
    db/
        models/

docs/
    developer/
    database/
    api/
    deployment/
    adr/
```

---

# ✨ Current Features

## Completed

- Project Foundation
- Application Factory
- Health Check
- Vehicle CRUD
- Trip CRUD
- Plan vs Actual API
- SQLAlchemy ORM
- Alembic Migration
- PostgreSQL
- Docker Development Environment

## In Progress

- Google Sheet Sync
- Vehicle Reading Import

## Planned

- Optimization Engine
- Recommendation Engine
- Dashboard API
- Analytics

---

# 🚀 Quick Start

## Prerequisites

- Python 3.12
- Docker Engine (WSL Ubuntu)
- VS Code
- Dev Container Extension

## Start Development Environment

Start Docker Engine

```bash
sudo service docker start
```

Start PostgreSQL

```bash
docker compose up -d postgres adminer
```

Open VS Code

```bash
code .
```

Reopen in Dev Container

Run migration

```bash
alembic upgrade head
```

Run API

```bash
uvicorn app.main:app --reload
```

Swagger

```
http://localhost:8000/docs
```

Health Check

```
GET /health
```

---

# 📚 Documentation

Complete project documentation is available under

```text
docs/
```

Developer Handbook

| Document | Description |
|----------|-------------|
| 01-Onboarding | Developer onboarding guide |
| 02-Git-Workflow | Git workflow and Pull Request |
| 03-Architecture | System architecture |
| 04-Feature-Development | Feature development guide |
| 05-Developer-Navigation | Feature map and navigation |
| 06-Project-Overview | Project history and phase overview |

Additional documentation

```text
docs/database/
docs/api/
docs/deployment/
docs/operations/
docs/adr/
```

---

# 🗄 Database

Current database tables

- vehicles
- drivers
- charging_stations
- trips
- vehicle_readings
- import_batches
- optimization_jobs
- optimization_recommendations

---

# ☁ Deployment

Target Platform

- Google Cloud Run
- Google Cloud SQL

---

# 🌱 Development Workflow

Every feature follows

```text
Requirement

↓

Feature Branch

↓

Development

↓

Swagger Test

↓

Pull Request

↓

Merge

↓

Documentation Update
```

---

# 🛣 Roadmap

Completed

- Vehicle CRUD
- Trip CRUD
- Plan vs Actual
- Docker Development Environment

Next

- Phase 6B Google Sheet Sync
- Vehicle Reading Import

Future

- Optimization Engine
- Recommendation Engine
- Dashboard
- Analytics

---

# 📄 License

Internal Project

Fair & Fast Co., Ltd.