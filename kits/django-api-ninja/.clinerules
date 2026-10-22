# CLAUDE.md ? Django + Django Ninja + PostgreSQL + Celery

You are pair programming on a production-grade Django Ninja API application.

## Core Invariants
1. **API Only**: Use Django Ninja with Pydantic v2 schemas. Never write legacy Django templates or DRF serializers.
2. **Database Optimization**: Always use select_related() and prefetch_related() to avoid N+1 queries.
3. **Async Tasks**: Offload background jobs to Celery tasks with Redis broker.
4. **Security**: Enforce Bearer token authentication and tenant authorization on all endpoints.

## Essential Commands
- Run dev server: python manage.py runserver 0.0.0.0:8000
- Run migrations: python manage.py migrate
- Run Celery worker: celery -A config worker -l info
- Run tests: pytest tests/ -v
