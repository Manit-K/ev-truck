# FairFast Python Template

Standard FastAPI + Dev Container + Docker Engine (WSL)

---

## Requirements

- Windows 11
- WSL2
- Docker Engine
- VS Code
- Dev Containers Extension

---

## Getting Started

1. Clone repository

```bash
git clone ...
```

2. Open in VS Code

3. Reopen in Dev Container

4. Verify environment

```bash
make check
```

5. Run API

```bash
make run
```

6. Open Swagger

http://localhost:8000/docs

---

## Team Rules

- Source Code อยู่ใน WSL (`~/projects`)
- ห้ามเก็บ Source Code ซ้ำใน Windows (`D:\Projects`)
- ใช้ Docker Engine บน WSL
- ห้ามใช้ Docker Desktop
- Git Push/Pull ผ่าน WSL Terminal
