# Phase 6A

Trip CRUD & Plan vs Actual

Status

✅ Completed

---

# Objective

สร้างระบบ Trip Management

รองรับ

- CRUD
- Plan vs Actual
- Validation
- Vehicle Check

---

# Scope

Included

- POST /trips
- GET /trips
- GET /trips/{id}
- PATCH /trips/{id}
- DELETE /trips/{id}
- GET /trips/{id}/plan-vs-actual

Not Included

- Google Sheet

- Driver CRUD

- Optimization

---

# Business Requirement

รองรับการสร้าง Trip

ใช้ Vehicle

เตรียมข้อมูลสำหรับ

Plan vs Actual

---

# Database

Affected Table

```
trips
```

Related

```
vehicles

vehicle_readings
```

Migration

No new migration

---

# Files Changed

Router

```
app/routers/trips.py
```

Service

```
app/services/trip.py
```

Repository

```
app/repositories/trip.py
```

Schema

```
app/schemas/trip.py
```

Model

```
app/db/models/trip.py
```

---

# API

POST

```
/trips
```

GET

```
/trips
```

GET

```
/trips/{id}
```

PATCH

```
/trips/{id}
```

DELETE

```
/trips/{id}
```

GET

```
/trips/{id}/plan-vs-actual
```

---

# Validation

Vehicle ต้องมีจริง

Trip ต้องไม่เป็น Null

404

422

500

---

# Testing

Swagger

✓

curl

✓

Vehicle CRUD

✓

Trip CRUD

✓

Plan vs Actual

✓

---

# Acceptance Test

☑ POST ผ่าน

☑ GET ผ่าน

☑ PATCH ผ่าน

☑ DELETE ผ่าน

☑ Plan vs Actual ผ่าน

---

# Lessons Learned

Trip ต้องมี Vehicle ก่อน

Master Data สำคัญ

Swagger ช่วย Test ได้เร็ว

ควรมี Seed Data

---

# Improvement

Driver CRUD

Google Sheet

Optimization

---

# Pull Request

PR

```
#2
```

---

# Merge

Merged to main

---

# Developer Notes

หากต้องการแก้ Trip

เปิด

```
03 Architecture

↓

05 Navigation

↓

Trip Folder
```

---

# Git Workflow

```bash
git add docs/developer/phases/phase-06A.md

git commit -m "docs: add Phase 6A documentation"
```
