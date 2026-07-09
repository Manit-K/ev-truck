# 02 - Git Workflow Guide

---

# Objective

กำหนดมาตรฐานการใช้ Git ของโครงการ EV Truck Optimization API

Developer ทุกคนต้องปฏิบัติตาม Workflow นี้

ห้าม Commit ลง main โดยตรง

---

# Git Branch Strategy

```
main
 │
 ├────────────── feature/phase-6b-google-sheet-sync
 │
 ├────────────── feature/vehicle-reading
 │
 ├────────────── feature/optimization-engine
 │
 └────────────── feature/dashboard
```

main

- Stable
- Deploy ได้เสมอ

feature/*

- สำหรับพัฒนา Feature ใหม่
- Merge ผ่าน Pull Request เท่านั้น

---

# Feature Development Workflow

```
Start

↓

Checkout main

↓

Pull Latest

↓

Create Feature Branch

↓

Coding

↓

Testing

↓

Commit

↓

Push

↓

Pull Request

↓

Code Review

↓

Merge

↓

Delete Branch

End
```

---

# เริ่ม Feature ใหม่

## Step 1

เปลี่ยนมาที่ main

```bash
git checkout main
```

---

## Step 2

ดึง main ล่าสุด

```bash
git pull origin main
```

ห้ามสร้าง Feature จาก main เก่า

---

## Step 3

สร้าง Branch

ตัวอย่าง

```bash
git checkout -b feature/phase-6b-google-sheet-sync
```

ชื่อ Branch

```
feature/xxxxx
```

ตัวอย่าง

```
feature/trip-crud

feature/google-sheet-sync

feature/optimization

feature/dashboard
```

---

# Coding

ระหว่างทำงาน

ดูสถานะ

```bash
git status
```

ดู Branch

```bash
git branch
```

---

# Commit

Commit บ่อย ๆ

ตัวอย่าง

```bash
git add .

git commit -m "feat: add google sheet repository"
```

ไม่ควรรอ Commit ทีเดียวตอนงานเสร็จ

---

# Commit Message Standard

ใช้ Conventional Commit

Feature

```
feat:
```

Bug

```
fix:
```

Document

```
docs:
```

Refactor

```
refactor:
```

Style

```
style:
```

Test

```
test:
```

Examples

```
feat: add trip CRUD

fix: resolve vehicle validation

docs: update onboarding guide

refactor: simplify repository

test: add trip API tests
```

---

# ก่อน Push

ทุกครั้ง

ต้องดึง main ล่าสุด

```bash
git checkout main

git pull origin main
```

กลับ Branch

```bash
git checkout feature/phase-6b-google-sheet-sync
```

Merge main

```bash
git merge main
```

ถ้ามี Conflict

แก้ก่อน

แล้ว

```bash
git add .

git commit
```

---

# Testing

ก่อน Push

ต้องผ่าน

```
alembic upgrade head

uvicorn app.main:app --reload
```

Swagger

```
/docs
```

ผ่านทั้งหมด

จึง Push

---

# Push

```bash
git push origin feature/phase-6b-google-sheet-sync
```

---

# Pull Request

Base

```
main
```

Compare

```
feature/phase-6b-google-sheet-sync
```

---

# Pull Request Template

Title

```
Phase 6B - Google Sheet Sync
```

Description

```
Summary

Features

Testing

Migration

Files Changed
```

---

# Review Checklist

ก่อน Merge

Developer ต้องตรวจ

```
☐ ไม่มี .env

☐ ไม่มี __pycache__

☐ ไม่มีไฟล์ชั่วคราว

☐ ไม่มีโฟลเดอร์ซ้อน

☐ Swagger ผ่าน

☐ curl ผ่าน

☐ Migration ถูกต้อง

☐ README Update

☐ Docs Update
```

---

# Merge

เมื่อ Review ผ่าน

```
Merge Pull Request

↓

Confirm Merge
```

---

# Cleanup

กลับ Local

```bash
git checkout main

git pull origin main
```

ลบ Local Branch

```bash
git branch -d feature/phase-6b-google-sheet-sync
```

ลบ Remote Branch

```bash
git push origin --delete feature/phase-6b-google-sheet-sync
```

---

# Hotfix

หาก Production มีปัญหา

```
main

↓

hotfix/xxxx

↓

Merge main
```

ห้ามแก้บน main โดยตรง

---

# Conflict Resolution

ถ้ามี

```
CONFLICT
```

Workflow

```
git merge main

↓

Resolve

↓

git add .

↓

git commit
```

---

# Git Command Cheat Sheet

Current Branch

```bash
git branch
```

Current Status

```bash
git status
```

Latest Commit

```bash
git log --oneline -10
```

Graph

```bash
git log --graph --decorate --oneline --all
```

Fetch

```bash
git fetch
```

Pull

```bash
git pull origin main
```

Push

```bash
git push origin feature/xxxx
```

Delete Local Branch

```bash
git branch -d feature/xxxx
```

Delete Remote Branch

```bash
git push origin --delete feature/xxxx
```

---

# Common Mistakes

❌ Commit บน main

❌ Push โดยไม่ merge main ล่าสุด

❌ ลืมทดสอบ Swagger

❌ Merge โดยไม่ Review

❌ Commit .env

❌ Commit Database

❌ ใช้ git branch -D ทั้งที่ยังไม่ Merge

---

# Team Rules

Developer ทุกคน

ต้อง

✓ ใช้ Feature Branch

✓ เปิด Pull Request

✓ Merge ผ่าน GitHub

✓ Delete Branch หลัง Merge

✓ Update Documentation

✓ ผ่าน API Test ก่อน Merge
