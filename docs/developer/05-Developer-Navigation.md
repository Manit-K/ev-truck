# 05 - Developer Navigation & Feature Map

Version 1.0

---

# Objective

เอกสารนี้เป็นศูนย์กลางของการพัฒนา

Developer สามารถค้นหาได้ทันทีว่า

- Feature อยู่ที่ไหน
- ต้องแก้ไฟล์ไหน
- เพิ่ม API ต้องทำอะไร
- เพิ่ม Table ต้องทำอะไร
- Bug ควรเริ่ม Debug จากตรงไหน

เอกสารนี้ต้อง Update ทุกครั้งที่มี Feature ใหม่

---

# System Navigation

```
Business Requirement

↓

Developer Navigation

↓

Feature Map

↓

Architecture

↓

Coding

↓

Testing

↓

Pull Request
```

---

# Project Structure

```
app/

    routers/

    services/

    repositories/

    schemas/

    db/

        models/

    core/

    main.py
```

---

# Layer Navigation

| Layer | Responsibility |
|---------|----------------|
| Router | API Endpoint |
| Service | Business Logic |
| Repository | Database Query |
| Schema | Request / Response |
| Model | ORM Mapping |
| Alembic | Database Migration |

---

# Feature Map

---

## Vehicle

Business

Vehicle Master

Files

```
Router

app/routers/vehicles.py

↓

Service

app/services/vehicle.py

↓

Repository

app/repositories/vehicle.py

↓

Schema

app/schemas/vehicle.py

↓

Model

app/db/models/vehicle.py
```

Related Feature

```
Trip

Optimization

Vehicle Reading
```

---

## Trip

Business

Trip Planning

Files

```
Router

app/routers/trips.py

↓

Service

app/services/trip.py

↓

Repository

app/repositories/trip.py

↓

Schema

app/schemas/trip.py

↓

Model

app/db/models/trip.py
```

Related Feature

```
Vehicle

Vehicle Reading

Plan vs Actual
```

---

## Vehicle Reading

Business

Actual Vehicle Data

Files

```
Router

(Phase 6B)

↓

Service

app/services/google_sheet.py

↓

Repository

app/repositories/vehicle_reading.py

↓

Schema

app/schemas/vehicle_reading.py

↓

Model

app/db/models/vehicle_reading.py
```

Related

```
Trip

Optimization

Google Sheet
```

---

## Google Sheet Sync

Business

Import Actual Data

Files

```
Router

integrations.py

↓

Service

google_sheet.py

↓

Repository

vehicle_reading.py

↓

Model

vehicle_reading.py
```

---

## Optimization

Business

Recommendation Engine

Files

```
Router

optimization.py

↓

Service

optimization.py

↓

Repository

optimization.py

↓

Model

optimization_job.py

optimization_recommendation.py
```

---

# Change Impact Matrix

## เพิ่ม Column

ตัวอย่าง

battery_health

Developer ต้องเปิด

```
Migration

↓

Model

↓

Schema

↓

Repository

↓

Service

↓

Swagger
```

---

## เพิ่ม API

ตัวอย่าง

```
POST /drivers
```

Developer ต้องเปิด

```
Router

↓

Service

↓

Repository

↓

Schema

↓

Model
```

---

## เพิ่ม Table

ตัวอย่าง

```
charging_history
```

Developer ต้องแก้

```
Alembic

↓

Model

↓

Repository

↓

Service

↓

Router

↓

Schema
```

---

# Feature Dependency

```
Vehicle

│

├── Trip

├── Vehicle Reading

└── Optimization
```

---

```
Trip

│

├── Vehicle

├── Driver

├── Vehicle Reading

└── Plan vs Actual
```

---

```
Vehicle Reading

│

├── Google Sheet

├── Trip

└── Optimization
```

---

# Debug Navigation

---

## POST Vehicle Error

เปิด

```
vehicle.py

↓

vehicle service

↓

vehicle repository
```

---

## POST Trip Error

เปิด

```
trip router

↓

trip service

↓

trip repository

↓

trip model
```

---

## Database Error

เปิด

```
Alembic

↓

Model

↓

Repository
```

---

## Validation Error

เปิด

```
Schema

↓

Router
```

---

## 404 Error

เปิด

```
Router

↓

Service
```

---

## 500 Error

เปิด

```
Repository

↓

Model

↓

Database
```

---

# New Requirement Navigation

Developer ได้ Requirement ใหม่

```
↓

Requirement

↓

Architecture

↓

Database

↓

Feature Map

↓

Coding

↓

Swagger

↓

Testing

↓

Pull Request
```

---

# Phase Navigation

## Phase 1

Foundation

---

## Phase 2

Vehicle CRUD

---

## Phase 3

Optimization Foundation

---

## Phase 4

Application Architecture

---

## Phase 5

Database Foundation

---

## Phase 5.5

Docker Compose

Developer Environment

---

## Phase 6A

Trip CRUD

Plan vs Actual

---

## Phase 6B

Google Sheet Sync

Vehicle Reading

---

## Phase 7

Optimization Engine

---

## Developer Decision Tree

มี Requirement ใหม่

↓

สร้าง Table ใหม่ไหม

YES

↓

Migration

↓

Model

↓

Repository

↓

Service

↓

Router

↓

Swagger

↓

Test

NO

↓

เพิ่ม API อย่างเดียว

↓

Router

↓

Service

↓

Repository

↓

Swagger

↓

Test

---

# Daily Development Checklist

```
☐ git pull

☐ docker compose up

☐ alembic upgrade

☐ run API

☐ Swagger Test

☐ Coding

☐ curl Test

☐ Commit

☐ Push

☐ Pull Request
```

---

# Git Workflow

## ตรวจสอบไฟล์

```bash
cat docs/developer/05-Developer-Navigation.md
```

---

## Git Status

```bash
git status
```

---

## Add

```bash
git add docs/developer/05-Developer-Navigation.md
```

---

## Commit

```bash
git commit -m "docs: add developer navigation guide"
```

---

## ตรวจสอบ Commit

```bash
git log --oneline -5
```
