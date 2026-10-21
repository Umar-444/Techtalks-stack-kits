from ninja import NinjaAPI, Schema

api = NinjaAPI(title="TechTalks Django Ninja API", version="1.0.0")

class HealthOut(Schema):
    status: str
    framework: str

@api.get("/health", response=HealthOut)
def health_check(request):
    return {"status": "ok", "framework": "django-ninja"}
