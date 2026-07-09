# ADR-001

# PostgreSQL as Primary Database

Status

Accepted

Date

2026-07-09

---

# Context

ระบบ EV Truck ต้องรองรับ

- Transaction
- Relationship
- Future Optimization
- Cloud SQL
- Large Dataset
- SQL Standard

จึงต้องเลือก Database

---

# Decision

เลือก

PostgreSQL

เป็น Database หลัก

---

# Reason

รองรับ

- ACID
- Foreign Key
- JSON
- Window Function
- Index
- Extension
- Cloud SQL

SQLAlchemy รองรับดีที่สุด

Cloud Run ใช้งานร่วมได้

---

# Alternative

MySQL

Pros

ง่าย

Cons

Function น้อยกว่า

---

SQLite

Pros

ง่าย

Cons

ไม่เหมาะ Production

---

MongoDB

Pros

Flexible

Cons

ไม่เหมาะกับ Transaction

---

# Consequences

Database

เป็น

Relational Database

ทุก Table

ใช้ Foreign Key

Migration

ใช้ Alembic

ORM

ใช้ SQLAlchemy

---

# Related ADR

ADR-002

ADR-004

ADR-006

---

# References

PostgreSQL

Cloud SQL

SQLAlchemy
