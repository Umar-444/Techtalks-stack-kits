# Agent Build Steps: Django 5 + Tailwind CSS + PostgreSQL 16+

Execute the following sequential steps to build, orchestrate, verify, and test the full-stack Django 5 + Tailwind + PostgreSQL kit. Every step includes an explicit verification command and expected output.

---

## Step 1: Environment Initialization & Dependency Installation
Create the isolated Python virtual environment and install all pinned dependencies including Django 5.1+, Psycopg 3, and Pytest.

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r starter/requirements.txt
```

**Verification Command**:
```bash
python -c "import django, psycopg; print('Django:', django.__version__, '| Psycopg:', psycopg.__version__)"
```
**Expected Output**:
```
Django: 5.1.x | Psycopg: 3.2.x
```

---

## Step 2: Environment Configuration & Secret Keys
Copy the template `.env.example` into `.env` and verify database and security parameters.

```bash
cp starter/.env.example starter/.env
```

**Verification Command**:
```bash
python -c "import os; from pathlib import Path; assert Path('starter/.env').exists(), 'Missing .env file'"
```
**Expected Output**:
```
(No error; exit code 0)
```

---

## Step 3: Database Migration Execution
Apply the core Django authentication, contenttypes, sessions, and custom `app` migrations against PostgreSQL.

```bash
cd starter/
python manage.py makemigrations
python manage.py migrate
```

**Verification Command**:
```bash
python manage.py showmigrations app
```
**Expected Output**:
```
app
 [X] 0001_initial
```

---

## Step 4: Static Asset Compilation & WhiteNoise Verification
Collect and content-hash all static assets and Tailwind CSS stylesheets into the production static root.

```bash
python manage.py collectstatic --no-input
```

**Verification Command**:
```bash
python -c "from django.conf import settings; import os; assert os.path.exists(settings.STATIC_ROOT), 'Static root missing'"
```
**Expected Output**:
```
(No error; exit code 0)
```

---

## Step 5: Multi-Container Docker Orchestration
Spin up the coordinated multi-container architecture (Django 5 web app + PostgreSQL 16 Alpine database with healthcheck).

```bash
docker compose up --build -d
```

**Verification Command**:
```bash
docker compose ps
```
**Expected Output**:
```
NAME                         IMAGE               STATUS                   PORTS
starter-db-1                 postgres:16-alpine  Up (healthy)             0.0.0.0:5432->5432/tcp
starter-web-1                starter-web         Up                       0.0.0.0:8000->8000/tcp
```

---

## Step 6: End-to-End Health Probe & Test Suite Execution
Execute the automated test suite and curl the `/healthz` probe.

```bash
curl -s http://localhost:8000/healthz
pytest starter/tests/
```

**Verification Command**:
```bash
curl -I http://localhost:8000/healthz
```
**Expected Output**:
```
HTTP/1.1 200 OK
Content-Type: application/json
{"status":"ok","app":"django-tailwind-postgresql","version":"1.0.0"}
```
