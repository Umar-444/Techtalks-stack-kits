from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class ItemCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(..., min_length=1, max_length=200)
    tenant_id: str = Field(..., min_length=1, max_length=64)
    description: str = Field(default="", max_length=1000)

class ItemResponse(BaseModel):
    id: int
    title: str
    tenant_id: str
    description: str
    is_active: bool

class HealthResponse(BaseModel):
    status: str = "ok"
    framework: str = "litestar"
    typing: str = "strict"
