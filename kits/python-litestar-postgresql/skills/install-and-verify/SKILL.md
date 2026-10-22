---
name: "install-and-verify"
description: "Install dependencies, run Docker Compose for PostgreSQL & Redis, execute Alembic migrations, and verify the Litestar service."
---

# Skill: Install and Verify Python Litestar + PostgreSQL + Redis

Use this skill to set up the development environment, configure Docker Compose, run database migrations, and verify the Litestar service.

## Step 1: Environment Setup & Dependencies
Ensure Python 3.12+ is installed:
```bash
python3 --version
```

Create a virtual environment and install pinned dependencies:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r starter/requirements.txt
```

## Step 2: Docker Compose Services
Start PostgreSQL 16 and Redis 7 in the background:
```bash
cd starter
docker compose up -d postgres redis
docker compose ps
```

## Step 3: Run Alembic Database Migrations
Apply database schema migrations:
```bash
alembic upgrade head
```

## Step 4: Run Automated Tests
Execute the pytest suite:
```bash
pytest starter/tests/test_app.py -v
```

## Step 5: Verification Curls
Start the server and check the `/health` endpoint:
```bash
curl -s http://localhost:8000/health | jq .
```
Expected response:
```json
{
  "status": "ok",
  "framework": "litestar",
  "typing": "strict"
}
```

Interactive OpenAPI Swagger docs are available at [http://localhost:8000/schema/swagger](http://localhost:8000/schema/swagger).
