# 01 - Developer Onboarding Guide
## Project Name
EV Truck Optimization API
## Purpose
ระบบ Backend API สำหรับเก็บข้อมูลรถ EV Truck, แผนการเดินรถ, ข้อมูลจริงจาก OCR/Google Sheet และนำไปใช้วิเคราะห์ Plan vs Actual รวมถึง Optimization Recommendation ใน Phase ถัดไป

## Business Flow
```text
LINE
↓
n8n
↓
OCR
↓
Google Sheet
↓
FastAPI Backend Sync
↓
PostgreSQL
↓
Plan vs Actual
↓
Optimization Recommendation
Tech Stack
	• FastAPI 
	• SQLAlchemy 2.x 
	• Alembic 
	• PostgreSQL 
	• Pydantic v2 
	• Docker Engine on WSL Ubuntu 
	• Dev Container 
	• GitHub 
	• Cloud Run target 
	• Cloud SQL target 
Architecture

Router
↓
Service
↓
Repository
↓
SQLAlchemy ORM
↓
PostgreSQL
Repository

GitHub: ev-truck
Main branch: main
Development: feature branch
Merge method: Pull Request
Local Development Prerequisites
Developer ต้องมีเครื่องมือเหล่านี้ก่อนเริ่มงาน
	• Windows + WSL Ubuntu 
	• Docker Engine ติดตั้งใน WSL 
	• VS Code 
	• Dev Containers extension 
	• Git 
	• Python tools ภายใน Dev Container 
First Time Setup
Clone repository

cd ~/projects
git clone git@github.com:Manit-K/ev-truck.git
cd ev-truck
Start Docker Engine

sudo service docker start
Start local database

docker compose up -d postgres adminer
Check containers

docker compose ps
ควรเห็น

ev-truck-postgres    running / healthy
ev-truck-adminer     running
Open VS Code

code .
ถ้า code . ใช้ไม่ได้ ให้เปิด VS Code จาก Windows แล้วเลือก folder:

\\wsl.localhost\Ubuntu\home\manitk\projects\ev-truck
จากนั้นเลือก

Reopen in Container
Environment
Local database URL สำหรับ FastAPI ใน Dev Container ควรชี้ไปยัง PostgreSQL container

DATABASE_URL=postgresql+psycopg2://evtruck:evtruck@host.docker.internal:5432/evtruck
หรือถ้า container network ใช้ service name ได้

DATABASE_URL=postgresql+psycopg2://evtruck:evtruck@postgres:5432/evtruck
ห้าม commit .env ที่มีข้อมูลลับขึ้น Git
Run Migration
ใน Dev Container

alembic upgrade head
Run API

uvicorn app.main:app --reload
Swagger URL

http://localhost:8000/docs
Health Check

curl http://localhost:8000/health
Morning Startup Checklist
ใช้ทุกครั้งที่กลับมาเริ่มพัฒนา

cd ~/projects/ev-truck
sudo service docker start
docker compose up -d postgres adminer
docker compose ps
จากนั้นเปิด VS Code และเข้า Dev Container
ใน Dev Container

alembic upgrade head
uvicorn app.main:app --reload
End of Day Checklist
หยุด API

Ctrl + C
ปิด VS Code
หยุด container

docker compose down
ถ้าต้องการประหยัด RAM

sudo service docker stop
ออกจาก WSL

exit
Common Commands
Check git branch

git branch
Check working tree

git status
Check containers

docker ps
docker compose ps
Check logs

docker compose logs postgres
Run migration

alembic upgrade head
Run API

uvicorn app.main:app --reload
First API Test
Create vehicle

curl -X POST http://localhost:8000/vehicles \
  -H "Content-Type: application/json" \
  -d '{"external_id":"EV-001","name":"EV Truck 001","license_plate":"TEST-001","battery_capacity_kwh":300,"minimum_soc_percent":20,"active":true}'
List vehicles

curl http://localhost:8000/vehicles
List trips

curl http://localhost:8000/trips
Troubleshooting
docker: command not found
อาจกำลังรันคำสั่งใน Dev Container ไม่ใช่ WSL Ubuntu
ให้รัน Docker command ที่ Ubuntu WSL
no configuration file provided
ยังไม่มี docker-compose.yml หรือไม่ได้อยู่ที่ root project

cd ~/projects/ev-truck
ls
Database connection refused
PostgreSQL container ยังไม่รัน

docker compose up -d postgres
docker compose ps
422 Unprocessable Entity
Request body ไม่ตรง schema ให้ดู Swagger /docs
500 Internal Server Error
ดู log ของ Uvicorn และตรวจว่า database ต่อได้หรือไม่
Rule for New Developers
ก่อนเริ่มแก้โค้ดทุกครั้ง

git checkout main
git pull origin main
git checkout -b feature/your-feature-name
ห้ามแก้บน main โดยตรง


---


