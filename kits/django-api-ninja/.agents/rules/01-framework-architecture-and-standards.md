# Django 5 & Django Ninja Framework Architecture

# 01 - Django 5 & Django Ninja Framework Architecture

## 1. Architectural Philosophy
- **Type-Safe API-First Django:** Leverage the full power of Django 5.1's ORM, migrations, and security middleware while eliminating legacy DRF serializers and monolithic views in favor of Django Ninja's lightweight Pydantic v2 integration.
- **Fast Execution & Low Overhead:** Django Ninja executes up to 2-3x faster than Django REST Framework by leveraging Pydantic's Rust-backed parsing core (`pydantic-core`) and generating native OpenAPI 3.1 specifications automatically.
- **ASGI & WSGI Compatibility:** Structure applications to support both traditional WSGI deployment (Gunicorn) and high-concurrency async ASGI execution (Uvicorn) with zero architectural rewrites.

## 2. Directory Layout & Modular Routers
```
starter/
├── config/
│   ├── __init__.py
│   ├── settings.py                 # Hardened Django 5 settings, environment configuration
│   ├── urls.py                     # Root URL routing mounting NinjaAPI
│   ├── api.py                      # NinjaAPI instance, global security, router mounting
│   └── celery.py                   # Celery 5.4 broker configuration
├── app/
│   ├── __init__.py
│   ├── models.py                   # Django ORM models with explicit indexes
│   ├── schemas.py                  # Pydantic v2 Schema request & response models
│   └── api.py                      # Domain router with typed endpoints
├── tests/
│   ├── __init__.py
│   └── test_api.py                 # Pytest-django and Ninja TestClient test suite
├── Dockerfile                      # Rootless container running as UID 10001
├── docker-compose.yml              # Django + PostgreSQL 16 + Redis 7 + Celery worker
└── requirements.txt                # Pinned production dependencies
```

## 3. NinjaAPI Configuration Invariants
- Instantiate a single root `NinjaAPI` instance in `config/api.py`:
  ```python
  from ninja import NinjaAPI
  from app.api import router as project_router

  api = NinjaAPI(
      title="TechTalks Enterprise API",
      version="1.0.0",
      description="Production-grade typed API with Django ORM and Celery",
      docs_url="/docs",
      openapi_url="/openapi.json"
  )

  api.add_router("/projects", project_router)
  ```
- Always mount sub-routers with explicit URL prefixes (`/projects`, `/auth`, `/tasks`).
- Never write untyped function-based views for API endpoints; all public interfaces must pass through `NinjaAPI` routers with explicit Pydantic request and response schemas.
