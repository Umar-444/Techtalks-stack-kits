from typing import List

from django.db import transaction
from ninja import Router
from ninja.errors import HttpError

from app.auth import auth
from app.models import Project
from app.schemas import ProjectIn, ProjectOut
from app.tasks import send_project_notification

router = Router(tags=["Projects"], auth=auth)


def _tenant_scope(request):
    """Every read path starts here. There is no unscoped Project manager call."""
    return Project.objects.filter(tenant_id=request.auth.tenant_id)


@router.get("/", response=List[ProjectOut])
def list_projects(request, limit: int = 50, offset: int = 0):
    # Clamp pagination so a caller cannot ask for the whole table.
    limit = max(1, min(limit, 100))
    offset = max(0, offset)
    return _tenant_scope(request).filter(is_active=True).order_by("-created_at")[
        offset : offset + limit
    ]


@router.get("/{int:project_id}", response=ProjectOut)
def get_project(request, project_id: int):
    project = _tenant_scope(request).filter(pk=project_id).first()
    if project is None:
        # 404 rather than 403: a foreign id must not be distinguishable from
        # one that does not exist, or the endpoint leaks tenant membership.
        raise HttpError(404, "Project not found")
    return project


@router.post("/", response={201: ProjectOut})
def create_project(request, payload: ProjectIn):
    tenant_id = request.auth.tenant_id
    if _tenant_scope(request).filter(slug=payload.slug).exists():
        raise HttpError(409, "A project with that slug already exists")

    with transaction.atomic():
        project = Project.objects.create(
            tenant_id=tenant_id, **payload.model_dump()
        )

    transaction.on_commit(lambda: send_project_notification.delay(project.id))
    return 201, project


@router.delete("/{int:project_id}", response={204: None})
def delete_project(request, project_id: int):
    deleted, _ = _tenant_scope(request).filter(pk=project_id).delete()
    if not deleted:
        raise HttpError(404, "Project not found")
    return 204, None


@router.get("/search", response=List[ProjectOut])
def search_projects(request, q: str = ""):
    # Parameterized through the ORM; q is never interpolated into SQL.
    return _tenant_scope(request).filter(name__icontains=q).order_by("-created_at")[:100]
