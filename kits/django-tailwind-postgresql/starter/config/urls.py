from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "ok", "app": "django-tailwind-postgresql", "version": "1.0.0"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('healthz', health_check, name='health_check'),
    path('', include('app.urls', namespace='app')),
]
