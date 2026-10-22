from ninja import Router
from typing import List
from app.models import Project
from app.schemas import ProjectIn, ProjectOut

router = Router(tags=["Projects"])

@router.get("/", response=List[ProjectOut])
def list_projects(request):
    return Project.objects.filter(is_active=True).order_by("-created_at")

@router.post("/", response={201: ProjectOut})
def create_project(request, payload: ProjectIn):
    project = Project.objects.create(**payload.dict())
    return 201, project
