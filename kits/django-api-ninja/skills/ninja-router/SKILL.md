---
name: ninja-router
description: Define modular Django Ninja routers with Pydantic v2 request/response schemas.
---
# Django Ninja Router Skill

`python
from ninja import Router
from app.schemas import ProjectIn, ProjectOut
from app.models import Project

router = Router(tags=["Projects"])

@router.get("/", response=list[ProjectOut])
def list_projects(request):
    return Project.objects.filter(is_active=True)
`
