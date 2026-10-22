---
name: install-and-verify
description: Install, orchestrate, and verify the Django 5 + Tailwind CSS + PostgreSQL 16+ full-stack application.
---

# Install & Verify Skill: Django 5 + Tailwind + PostgreSQL

## Prerequisites
- Python 3.12+
- PostgreSQL 16+
- Node.js 18+ (optional, only if recompiling custom Tailwind plugins)

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
Run the verification probes:
```bash
curl -X GET http://localhost:8000/healthz
```
Expected output:
```json
{"status":"ok","app":"django-tailwind-postgresql","version":"1.0.0"}
```

Verify Main Web Interface:
- Dashboard: [http://localhost:8000/](http://localhost:8000/)
- Django Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)

## Failure Recovery Matrix
| Symptom | Probable Cause | Resolution |
| :--- | :--- | :--- |
| `django.db.utils.OperationalError: connection to server on socket failed` | PostgreSQL service not running | Start DB via `docker compose up -d db` or start system postgres service |
| `Static files 404 in production` | WhiteNoise static assets not gathered | Run `python manage.py collectstatic --noinput` |
| `CSRF verification failed. Request aborted` | Missing `{% csrf_token %}` inside POST form | Ensure every template POST form includes `{% csrf_token %}` |

## Done Means
Django web application serves responsive Tailwind CSS HTML interface at `/`, applies migrations to PostgreSQL 16, and passes all unit tests.
