from datetime import datetime

from ninja import Field, Schema


class StrictSchema(Schema):
    """Rejects unknown keys so a client cannot smuggle extra fields through.

    Without extra="forbid", a POST carrying {"tenant_id": "victim"} would be
    silently accepted and ignored by the schema but could still reach the ORM
    if a handler ever splatted the raw payload.
    """

    model_config = {"extra": "forbid"}


class ProjectIn(StrictSchema):
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
    # tenant_id is deliberately not exposed: it is an internal isolation key,
    # not client-facing data.
