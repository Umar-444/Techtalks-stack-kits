import os
from typing import List, Optional
from litestar import Litestar, get, post
from litestar.config.cors import CORSConfig
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from litestar.exceptions import NotFoundException

from app.domain.schemas import ItemCreate, ItemResponse, HealthResponse
from app.services.item_service import item_service

@get("/health", status_code=HTTP_200_OK)
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok", framework="litestar", typing="strict")

@get("/api/v1/items", status_code=HTTP_200_OK)
async def list_items(tenant_id: Optional[str] = None) -> List[ItemResponse]:
    return await item_service.list(tenant_id=tenant_id)

@post("/api/v1/items", status_code=HTTP_201_CREATED)
async def create_item(data: ItemCreate) -> ItemResponse:
    return await item_service.create(data)

@get("/api/v1/items/{item_id:int}", status_code=HTTP_200_OK)
async def get_item(item_id: int, tenant_id: str) -> ItemResponse:
    item = await item_service.get_by_id(item_id, tenant_id)
    if not item:
        raise NotFoundException(detail="Item not found or access denied")
    return item

# Explicit CORS configuration reading from ALLOWED_ORIGINS (no wildcard)
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8080")
origins_list = [o.strip() for o in allowed_origins_env.split(",") if o.strip()]

cors_config = CORSConfig(
    allow_origins=origins_list or ["http://localhost:3000", "http://localhost:8080"],
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=True,
)

app = Litestar(
    route_handlers=[health_check, list_items, create_item, get_item],
    cors_config=cors_config,
)
