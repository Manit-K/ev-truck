# 04 - Feature Development Guide

Version 1.0

---

# Purpose

เอกสารนี้อธิบาย

Developer จะเริ่มพัฒนา Feature ใหม่อย่างไร

เพื่อให้ทุกคนเขียนโค้ดในรูปแบบเดียวกัน

และลด Bug จากการแก้ไขไม่ครบทุก Layer

---

# Development Flow

ทุก Feature ใหม่

ต้องเดินตามลำดับนี้

```
Requirement

↓

Database Design

↓

Alembic Migration

↓

SQLAlchemy Model

↓

Pydantic Schema

↓

Repository

↓

Service

↓

Router

↓

Swagger Test

↓

curl Test

↓

Git Commit

↓

Pull Request

↓

Merge
```

---

# New Feature Checklist

ก่อนเริ่ม

```
☐ อ่าน Requirement

☐ วิเคราะห์ Database

☐ วิเคราะห์ Feature ที่เกี่ยวข้อง

☐ วิเคราะห์ผลกระทบ

☐ เปิด Feature Map

☐ เปิด Change Impact Matrix
```

---

# Standard Folder

ทุก Feature

```
app/

    routers/

    services/

    repositories/

    schemas/

    db/models/
```

---

# ตัวอย่าง

เพิ่ม Driver CRUD

ต้องมี

```
Router

drivers.py

↓

Service

driver.py

↓

Repository

driver.py

↓

Schema

driver.py

↓

Model

driver.py
```

---

# ขั้นตอนเพิ่ม API ใหม่

ตัวอย่าง

```
POST /drivers
```

Workflow

```
Requirement

↓

Schema

↓

Service

↓

Repository

↓

Router

↓

Swagger

↓

Test
```

---

# ขั้นตอนเพิ่ม Table ใหม่

ตัวอย่าง

```
driver_license
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

# ขั้นตอนเพิ่ม Column ใหม่

ตัวอย่าง

battery_health

Developer ต้องแก้

```
Alembic

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

# Feature Development Template

## Step 1

อ่าน Requirement

ตัวอย่าง

```
ต้องเพิ่ม Driver CRUD
```

---

## Step 2

ถาม

ข้อมูลจะเก็บที่ Table ไหน

ถ้ายังไม่มี

สร้าง Migration

---

## Step 3

สร้าง Model

```
driver.py
```

---

## Step 4

สร้าง Schema

```
DriverCreate

DriverUpdate

DriverRead

DriverList
```

---

## Step 5

สร้าง Repository

CRUD

```
create()

get()

list()

update()

delete()
```

---

## Step 6

สร้าง Service

Business Logic

Validation

---

## Step 7

สร้าง Router

```
POST

GET

PATCH

DELETE
```

---

## Step 8

Register Router

```
main.py

หรือ

api/router.py
```

---

## Step 9

Swagger Test

```
POST

GET

PATCH

DELETE
```

---

## Step 10

curl Test

ทุก API

---

# Bug Fix Workflow

Bug

↓

อ่าน Error

↓

เปิด Architecture Guide

↓

เปิด Feature Map

↓

หา Layer

↓

แก้เฉพาะ Layer

↓

Test

↓

Commit

↓

PR

---

# Change Impact Analysis

ตัวอย่าง

แก้ Trip

ต้องเช็ค

```
Trip Router

↓

Trip Service

↓

Trip Repository

↓

Trip Schema

↓

Trip Model
```

---

แก้ Vehicle

ต้องเช็ค

```
Vehicle

↓

Trip

↓

Optimization

↓

Vehicle Reading
```

---

แก้ Vehicle Reading

ต้องเช็ค

```
Vehicle Reading

↓

Google Sheet Sync

↓

Plan vs Actual

↓

Optimization
```

---

# Feature Dependency Matrix

| Feature | Depends On |
|----------|------------|
| Vehicle | - |
| Driver | - |
| Trip | Vehicle, Driver |
| Vehicle Reading | Vehicle |
| Google Sheet Sync | Vehicle Reading |
| Plan vs Actual | Trip + Vehicle Reading |
| Optimization | Trip + Vehicle Reading |

---

# Feature Status

| Feature | Status |
|----------|--------|
| Vehicle CRUD | Complete |
| Trip CRUD | Complete |
| Driver CRUD | Planned |
| Charging CRUD | Planned |
| Google Sheet Sync | Phase 6B |
| Optimization Engine | Phase 7 |

---

# Definition of Done

Feature ถือว่าเสร็จเมื่อ

```
☐ Migration ผ่าน

☐ Model

☐ Schema

☐ Repository

☐ Service

☐ Router

☐ Swagger ผ่าน

☐ curl ผ่าน

☐ Documentation

☐ Pull Request

☐ Merge
```

---

# Coding Rules

ทุก Feature

ใช้

Repository Pattern

Service Layer

Type Hint

Dependency Injection

Pydantic

SQLAlchemy

---

# Naming Convention

Router

```
vehicles.py

drivers.py

trips.py
```

Service

```
vehicle.py

driver.py

trip.py
```

Repository

```
vehicle.py

driver.py

trip.py
```

Schema

```
vehicle.py

driver.py

trip.py
```

Model

```
vehicle.py

driver.py

trip.py
```

---

# Before Commit Checklist

```
☐ Swagger

☐ curl

☐ Alembic

☐ git status

☐ git diff

☐ README

☐ Docs

☐ Files Changed
```

---

# Phase Development Rule

Developer ห้าม

เพิ่ม Feature ข้าม Phase

ตัวอย่าง

Phase 6B

ทำเฉพาะ

Google Sheet Sync

ห้าม

ทำ Dashboard

ห้าม

ทำ Optimization

เพื่อให้

PR มีขนาดเล็ก

Review ง่าย

Rollback ง่าย
