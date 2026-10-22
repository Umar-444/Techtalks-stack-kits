from ninja import NinjaAPI
from app.api import router as app_router

api = NinjaAPI(
    title="Django Ninja Production API",
    version="1.0.0",
    description="High-speed typed API backed by Django ORM and Celery."
)

@api.get("/health", tags=["System"])
def health_check(request):
    return {"status": "healthy", "service": "django-api-ninja", "version": "1.0.0"}

api.add_router("/projects", app_router)
