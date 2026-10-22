# Django + Django Ninja + PostgreSQL + Celery Stack Kit

API-only Django: full power of Django ORM, migrations, and admin panel behind high-speed typed Pydantic endpoints, OpenAPI 3.1, and asynchronous Celery background workers.

## Quickstart

### 1. Clone & Start Containers
````bash
git clone https://github.com/Umar-444/Techtalks-stack-kits.git
cd Techtalks-stack-kits/kits/django-api-ninja/starter
cp .env.example .env
docker compose up -d
`

### 2. Run Migrations
````bash
docker compose exec web python manage.py migrate
`

### 3. Verify Health
````bash
curl http://localhost:8000/api/health
# {"status":"healthy","service":"django-api-ninja","version":"1.0.0"}
`

### 4. Interactive OpenAPI Documentation
Open your browser at http://localhost:8000/api/docs to view the interactive Swagger/OpenAPI documentation.

### 5. Run Tests
````bash
docker compose exec web pytest tests/ -v
`

## Agent Onboarding Prompt
`
You are building with the Django + Django Ninja + PostgreSQL + Celery kit. Follow rules in CLAUDE.md / .cursor/rules, Pydantic v2 schemas in app/schemas.py, and steps/agent-build-steps.md.
`
