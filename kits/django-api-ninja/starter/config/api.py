from django.db import connection
from ninja import NinjaAPI
from ninja.errors import ValidationError

from app.api import router as app_router

api = NinjaAPI(
    title="Django Ninja Production API",
    version="1.0.0",
    description="High-speed typed API backed by Django ORM and Celery.",
)


@api.exception_handler(ValidationError)
def validation_error_handler(request, exc):
    """Return the field errors without echoing a traceback."""
    return api.create_response(
        request, {"detail": exc.errors, "code": "VALIDATION_ERROR"}, status=422
    )


@api.get("/health", tags=["System"], auth=None)
def health_check(request):
    """Liveness probe that actually touches the database.

    A health endpoint that only returns a literal will report healthy while
    the database is unreachable, which is the failure it exists to catch.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            database_ok = cursor.fetchone()[0] == 1
    except Exception:
        database_ok = False

    return api.create_response(
        request,
        {
            "status": "healthy" if database_ok else "degraded",
            "service": "django-api-ninja",
            "version": "1.0.0",
            "database": "ok" if database_ok else "unreachable",
        },
        status=200 if database_ok else 503,
    )


api.add_router("/projects", app_router)
