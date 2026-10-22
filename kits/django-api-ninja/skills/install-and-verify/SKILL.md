---
name: install-and-verify
description: Install, orchestrate, and verify the Django 5 + Django Ninja + PostgreSQL + Celery API stack.
---

# Install & Verify Skill: Django + Django Ninja + Celery

## Prerequisites
- Python 3.12+
- PostgreSQL 16+
- Redis 7+

## OS-Specific Commands

### Linux / macOS
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Windows (PowerShell)
```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Docker Compose Quickstart
```bash
docker compose up --build -d
```

## Post-Install Verification
Run the verification curl commands:
```bash
curl -X GET http://localhost:8000/api/healthz
```
Expected output:
```json
{"status":"ok","app":"django-api-ninja","version":"1.0.0"}
```

Explore OpenAPI Interactive Docs:
- Swagger UI: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)

## Failure Recovery Matrix
| Symptom | Probable Cause | Resolution |
| :--- | :--- | :--- |
| `django.db.utils.OperationalError: could not translate host name "db"` | Local host trying to resolve Docker container hostname | Set `POSTGRES_HOST=localhost` in `.env` for native host execution |
| `celery.exceptions.OperationalError: Error 111 connecting to localhost:6379` | Celery worker cannot reach Redis broker | Start Redis container via `docker compose up -d redis` |
| `ninja.errors.ConfigError` | Schema validation mismatch | Verify Pydantic schemas in `app/schemas.py` match model field types |

## Done Means
Django booted with Django Ninja OpenAPI docs at `/api/docs`, migrations applied to PostgreSQL, and Celery worker running without errors.
