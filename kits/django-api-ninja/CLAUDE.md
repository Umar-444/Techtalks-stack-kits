# Django + Django Ninja + PostgreSQL + Celery — Claude Code Guidelines (CLAUDE.md)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Quick Reference & Non-Negotiable Standards
### 01 Framework Architecture And Standards
﻿---
id: "01-framework-architecture-and-standards"
title: "Django 5 & Django Ninja Framework Architecture"
description: "Architectural standards for high-throughput typed APIs using Django 5.1, Django Ninja 1.3, Pydantic v2 schemas, and modular domain routers."
globs: ["**/*.py", "manage.py", "Dockerfile", "docker-compose.yml"]
alwaysApply: true
---

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


### 02 Orm Models And Query Optimization
﻿---
id: "02-orm-models-and-query-optimization"
title: "Django ORM Invariants & Query Optimization"
description: "Database standards for PostgreSQL models, N+1 query prevention with select_related/prefetch_related, explicit indexing, and tenant isolation."
globs: ["**/models.py", "**/migrations/*.py"]
alwaysApply: true
---

# 02 - Django ORM Invariants & Query Optimization

## 1. N+1 Query Elimination Invariants
- **Foreign Key Traversal:** Never access foreign key attributes inside loops or serializers without `select_related()`:
  ```python
  # CORRECT: Single SQL JOIN
  projects = Project.objects.select_related("organization", "owner").filter(is_active=True)
  ```
- **Many-to-Many & Reverse Relations:** Always use `prefetch_related()` for many-to-many sets or reverse foreign keys:
  ```python
  # CORRECT: Batch prefetch query
  projects = Project.objects.prefetch_related("tags", "collaborators").filter(is_active=True)
  ```

## 2. Explicit Database Indexing
- Define explicit composite or single-column indexes using `models.Index` inside model `Meta`:
  ```python
  class Project(models.Model):
      name = models.CharField(max_length=200, db_index=True)
      slug = models.SlugField(max_length=200, unique=True)
      tenant_id = models.CharField(max_length=64, db_index=True)
      is_active = models.BooleanField(default=True)
      created_at = models.DateTimeField(auto_now_add=True)

      class Meta:
          indexes = [
              models.Index(fields=["tenant_id", "is_active", "-created_at"]),
          ]
  ```

## 3. Multi-Tenant Query Scoping & BOLA Defense
- Every query accessing customer data must be explicitly scoped by the authenticated user's `tenant_id` or `owner`:
  ```python
  @router.get("/{project_id}", response=ProjectOut)
  def get_project(request, project_id: int):
      try:
          return Project.objects.get(id=project_id, tenant_id=request.auth.tenant_id)
      except Project.DoesNotExist:
          raise HttpError(404, "Project not found")
  ```
- Never execute naked `Project.objects.get(id=project_id)` lookups without tenant constraints.

## 4. Reversible, Backward-Compatible Migrations
- All Django migrations committed to source control must be fully reversible (`migrations.RunPython(forward_fn, reverse_fn)`).
- Never drop a column or rename a table in a single migration. Use a two-phase rollout to maintain backward compatibility during zero-downtime rolling deployments.


### 03 Pydantic Schemas And Serialization
﻿---
id: "03-pydantic-schemas-and-serialization"
title: "Pydantic v2 Schemas & Serialization Standards"
description: "Validation rules for Django Ninja Schema models, request payload bounds, response filtering, and custom error formatting."
globs: ["**/schemas.py", "**/api.py"]
alwaysApply: true
---

# 03 - Pydantic v2 Schemas & Serialization Standards

## 1. Schema Inheritance & Configuration
- Inherit all API schemas from `ninja.Schema` (which wraps Pydantic v2 `BaseModel`):
  ```python
  from ninja import Schema, Field
  from datetime import datetime
  from typing import Optional

  class ProjectIn(Schema):
      name: str = Field(..., min_length=2, max_length=200)
      slug: str = Field(..., min_length=2, max_length=200, pattern=r"^[a-z0-9-]+$")
      description: str = Field(default="", max_length=2000)

  class ProjectOut(Schema):
      id: int
      name: str
      slug: str
      description: str
      is_active: bool
      created_at: datetime
  ```

## 2. Mass Assignment Defense & Field Exclusion
- Never expose sensitive internal model fields (`password_hash`, `stripe_customer_id`, `internal_notes`) in response schemas.
- Explicitly declare every field returned in `ProjectOut`. Never use unbounded dictionary serializers (`dict(instance.__dict__)`).

## 3. Strict Input Coercion
- Set `extra = "forbid"` in `model_config` on mutation schemas to reject unknown query or JSON body attributes:
  ```python
  class StrictSchema(Schema):
      model_config = {"extra": "forbid"}
  ```

## 4. Custom Error Handling
- Capture validation errors gracefully via Django Ninja's exception handler:
  ```python
  @api.exception_handler(ValidationError)
  def validation_error_handler(request, exc):
      return api.create_response(
          request,
          {"detail": exc.errors(), "code": "VALIDATION_ERROR"},
          status=422
      )
  ```


### 04 Authentication Security And Celery
﻿---
id: "04-authentication-security-and-celery"
title: "Authentication, API Security & Celery Task Queue"
description: "Security standards for Bearer token authentication, API keys, Celery 5.4 async background worker orchestration, and Redis broker settings."
globs: ["**/api.py", "**/celery.py", "**/settings.py"]
alwaysApply: true
---

# 04 - Authentication, API Security & Celery Task Queue

## 1. Authentication with HttpBearer & API Keys
- Protect endpoints using Django Ninja's native security classes (`HttpBearer`, `APIKeyHeader`):
  ```python
  from ninja.security import HttpBearer
  from django.contrib.auth.models import User

  class JWTAuth(HttpBearer):
      def authenticate(self, request, token):
          user = verify_jwt_token(token)
          if user:
              return user
          return None

  auth = JWTAuth()

  @router.get("/protected", auth=auth)
  def protected_endpoint(request):
      return {"user": request.auth.username}
  ```

## 2. Celery 5.4 Async Task Dispatching
- Never perform blocking network calls (sending transactional emails, indexing embeddings, calling payment gateways) inside HTTP request handlers.
- Offload long-running operations to Celery background tasks:
  ```python
  from config.celery import app as celery_app

  @celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
  def send_project_notification(self, project_id: int):
      try:
          # Background processing logic
          pass
      except Exception as exc:
          raise self.retry(exc=exc)
  ```
- Trigger tasks with `.delay()` after transactions commit:
  ```python
  from django.db import transaction

  transaction.on_commit(lambda: send_project_notification.delay(project.id))
  ```

## 3. Celery Security & Serialization Invariants
- Enforce strict JSON serialization in `settings.py`:
  ```python
  CELERY_ACCEPT_CONTENT = ["json"]
  CELERY_TASK_SERIALIZER = "json"
  CELERY_RESULT_SERIALIZER = "json"
  ```
- Never allow `pickle` serialization in Celery, as it enables arbitrary remote code execution (RCE) if Redis is compromised.


### 05 Testing Verification And Ci
﻿---
id: "05-testing-verification-and-ci"
title: "Testing, Container Hardening & Token Benchmark"
description: "Testing standards using Ninja TestClient, pytest-django, rootless Docker execution (UID 10001), and token-light efficiency verification."
globs: ["tests/**/*.py", "Dockerfile", "evals/**"]
alwaysApply: true
---

# 05 - Testing, Container Hardening & Token Benchmark

## 1. Fast Automated Testing with TestClient
- Test Django Ninja endpoints using `ninja.testing.TestClient`:
  ```python
  import pytest
  from ninja.testing import TestClient
  from config.api import api
  from app.models import Project

  client = TestClient(api)

  def test_health():
      res = client.get("/health")
      assert res.status_code == 200
      assert res.json()["status"] == "healthy"

  @pytest.mark.django_db
  def test_project_crud():
      res = client.post("/projects/", json={"name": "API Audit", "slug": "api-audit"})
      assert res.status_code == 201
      assert res.json()["slug"] == "api-audit"
  ```
- Fast execution invariant: Tests must complete within 2 seconds using an in-memory SQLite test database.

## 2. Container Hardening & Rootless Execution
- Docker containers must execute as an unprivileged user (`USER 10001:10001`):
  ```dockerfile
  RUN groupadd -g 10001 appgroup && \
      useradd -u 10001 -g appgroup -s /bin/sh -m appuser
  USER 10001:10001
  ```
- Set `ALLOWED_HOSTS` dynamically from environment variables, avoiding insecure wildcards in production.

## 3. Token Benchmark & Efficiency Tier
- Benchmark verification: Run `python evals/runner.py --kit django-api-ninja`.
- Target token consumption: ~20,500 tokens (Efficiency Tier: **A**).
- Justification: Django ORM migrations and admin panel batteries combined with typed Pydantic endpoints minimize agent implementation tokens.


