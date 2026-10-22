from ninja import Schema
from datetime import datetime

class ProjectIn(Schema):
    name: str
    slug: str
    description: str = ""

class ProjectOut(Schema):
    id: int
    name: str
    slug: str
    description: str
    is_active: bool
    created_at: datetime
