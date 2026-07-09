# 03 - System Architecture Guide

Version 1.0

---

# Purpose

เอกสารนี้อธิบาย Architecture ของ EV Truck Optimization API

Developer ใหม่สามารถเปิดเอกสารนี้แล้วเข้าใจ

- Project Structure
- Data Flow
- Layer ต่าง ๆ
- เวลาแก้ Feature ต้องแก้ไฟล์ไหน
- เมื่อเพิ่ม Column ใหม่ต้องแก้อะไรบ้าง

---

# High Level Architecture

```
             Client

                │

                ▼

          FastAPI Router

                │

                ▼

         Service Layer

                │

                ▼

      Repository Layer

                │

                ▼

        SQLAlchemy ORM

                │

                ▼

          PostgreSQL
```

---

# Clean Architecture

ทุก Feature ต้องใช้ Pattern นี้

```
Router

↓

Service

↓

Repository

↓

ORM

↓

Database
```

ห้าม

```
Router

↓

Database
```

โดยตรง

---

# Folder Structure

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

# Responsibility

## Router

รับ Request

Validate

เรียก Service

ส่ง Response

ห้ามมี Business Logic

---

## Service

Business Logic

Validation

Transaction

เรียก Repository

---

## Repository

Database Query

CRUD

SQLAlchemy

---

## Model

ORM Mapping

Table Definition

Relationship

---

## Schema

Pydantic

Request

Response

Validation

---

# Request Flow

```
POST /trips

↓

Router

↓

TripService

↓

TripRepository

↓

Trip ORM

↓

PostgreSQL

↓

Repository

↓

Service

↓

Router

↓

JSON Response
```

---

# Database Flow

```
Request

↓

Schema Validation

↓

Service Validation

↓

Repository

↓

SQLAlchemy

↓

PostgreSQL
```

---

# Feature Structure

ทุก Feature ต้องมี

```
Router

Service

Repository

Schema

Model
```

---

ตัวอย่าง

Trip

```
app/

    routers/

        trips.py

    services/

        trip.py

    repositories/

        trip.py

    schemas/

        trip.py

    db/models/

        trip.py
```

---

Vehicle

```
app/

    routers/

        vehicles.py

    services/

        vehicle.py

    repositories/

        vehicle.py

    schemas/

        vehicle.py

    db/models/

        vehicle.py
```

---

# Feature Map

| Feature | Router | Service | Repository | Schema | Model |
|----------|---------|----------|------------|---------|---------|
| Vehicle | vehicles.py | vehicle.py | vehicle.py | vehicle.py | vehicle.py |
| Trip | trips.py | trip.py | trip.py | trip.py | trip.py |
| Vehicle Reading | vehicle_reading.py | vehicle_reading.py | vehicle_reading.py | vehicle_reading.py | vehicle_reading.py |
| Optimization | optimization.py | optimization.py | optimization.py | optimization.py | optimization.py |

---

# Change Impact Matrix

## เพิ่ม Field ใหม่

ตัวอย่าง

```
battery_health
```

Developer ต้องแก้

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

Router

↓

Swagger
```

Checklist

```
☐ Alembic

☐ Model

☐ Schema

☐ Repository

☐ Service

☐ Router

☐ Swagger

☐ curl Test
```

---

## เพิ่ม API ใหม่

ตัวอย่าง

```
POST /drivers
```

ต้องสร้าง

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

## เพิ่ม Table ใหม่

ตัวอย่าง

```
drivers
```

Checklist

```
☐ Alembic

☐ Model

☐ Repository

☐ Service

☐ Router

☐ Schema
```

---

# Dependency Matrix

```
Trip

│

├── Vehicle

├── Driver

├── Vehicle Reading

└── Optimization
```

Vehicle

```
Vehicle

│

├── Trip

├── Optimization

└── Recommendation
```

Vehicle Reading

```
Vehicle Reading

│

├── Trip

├── Plan vs Actual

└── Optimization
```

---

# Data Ownership

Vehicle

เป็น Master Data

Trip

เป็น Transaction

Vehicle Reading

เป็น Actual Data

Optimization

เป็น Result

---

# Business Flow

```
Vehicle

↓

Trip

↓

Vehicle Reading

↓

Plan vs Actual

↓

Optimization

↓

Recommendation
```

---

# Error Handling

Validation

↓

Service

↓

Repository

↓

Database

↓

Rollback

↓

Response

---

# Logging Flow

Request

↓

Router

↓

Service

↓

Repository

↓

Database

↓

Response

---

# Future Expansion

Phase 6B

Google Sheet Sync

↓

Vehicle Reading

↓

Plan vs Actual

Phase 7

Optimization Engine

↓

Recommendation

Phase 8

Dashboard

↓

Analytics

---

# Architecture Rules

Developer ทุกคน

ต้องปฏิบัติตาม

✓ Repository Pattern

✓ Service Layer

✓ SQLAlchemy ORM

✓ Pydantic Schema

✓ Dependency Injection

✓ Alembic Migration

✓ Type Hint

✓ Clean Code

✓ SOLID

---

# Never Do

ห้าม

Router Query Database

ห้าม

Business Logic ใน Router

ห้าม

Schema Import ORM

ห้าม

Repository Return JSON

Repository Return ORM เท่านั้น

---

# Architecture Checklist

ก่อน Merge

```
☐ Router

☐ Service

☐ Repository

☐ Schema

☐ Model

☐ Migration

☐ Swagger

☐ Test

☐ Documentation
```
