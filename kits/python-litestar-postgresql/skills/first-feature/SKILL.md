---
name: "first-feature"
description: "Scaffold a complete end-to-end CRUD feature: SQLAlchemy 2.0 async model, msgspec DTO schema, domain service, and Litestar Controller."
---

# Skill: First Feature - Scaffolding with Litestar & SQLAlchemy 2.0

Follow this workflow to implement an end-to-end API resource in Litestar.

## Step 1: Define SQLAlchemy 2.0 Model
In `app/domain/models.py`:
```python
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime
from datetime import datetime
from app.domain.models import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    tenant_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    price: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
```

## Step 2: Define msgspec DTOs
In `app/domain/schemas.py`:
```python
import msgspec

class ProductCreateDTO(msgspec.Struct, forbid_unknown_fields=True):
    name: str
    tenant_id: str
    price: float

class ProductResponseDTO(msgspec.Struct):
    id: int
    name: str
    tenant_id: str
    price: float
```

## Step 3: Implement Litestar Controller
In `app/controllers/product_controller.py`:
```python
from litestar import Controller, get, post
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED

class ProductController(Controller):
    path = "/api/v1/products"
    tags = ["Products"]

    @get(status_code=HTTP_200_OK)
    async def list_products(self, product_service: ProductService) -> list[ProductResponseDTO]:
        return await product_service.list()

    @post(status_code=HTTP_201_CREATED)
    async def create_product(self, data: ProductCreateDTO, product_service: ProductService) -> ProductResponseDTO:
        return await product_service.create(data)
```

## Step 4: Verify with Curl
```bash
curl -X POST http://localhost:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Database Cluster", "tenant_id": "tenant-01", "price": 499.0}'
```
