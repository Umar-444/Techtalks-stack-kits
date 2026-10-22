# Python + Litestar + SQLAlchemy 2 + PostgreSQL + Redis — Agent Operating Rules (AGENTS.md)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Table of Contents
- [01 Framework Architecture And Standards](#01-framework-architecture-and-standards)
- [02 Sqlalchemy Async Sessions And Models](#02-sqlalchemy-async-sessions-and-models)
- [03 Dto Architecture And Msgspec Validation](#03-dto-architecture-and-msgspec-validation)
- [04 Api Security And Tenant Isolation](#04-api-security-and-tenant-isolation)
- [05 Testing Verification And Ci](#05-testing-verification-and-ci)

---

<a id="01-framework-architecture-and-standards"></a>
## 01 Framework Architecture And Standards

﻿---
id: "01-framework-architecture-and-standards"
title: "Litestar Framework Architecture & Clean Dependency Injection"
description: "Architectural standards for modern ASGI services using Litestar 2.12+, layered dependency injection with Provide, Controller routing, and OpenAPI configuration."
globs: ["**/*.py", "Dockerfile", "docker-compose.yml"]
alwaysApply: true
---

# 01 - Litestar Framework Architecture & Clean Dependency Injection

## 1. Architectural Mission & Philosophy
- **The Modern ASGI Standard:** Litestar is an enterprise-grade ASGI framework engineered around Python's typing system, clean architectural layers, and performance. Unlike microframeworks that rely on global state or monkey-patching, Litestar enforces explicit dependency graphs, clean separation of concerns, and native msgspec serialization.
- **Layered Dependency Injection (DI):** Leverage Litestar's `Provide` mechanism to declare dependencies at the application, router, or handler level. Dependencies are resolved once per request lifetime and injected cleanly into handler parameters:
  ```python
  from litestar.di import Provide

  async def provide_item_service(db_session: AsyncSession) -> ItemService:
      return ItemService(session=db_session)

  app = Litestar(
      route_handlers=[item_controller],
      dependencies={"item_service": Provide(provide_item_service)},
  )
  ```

## 2. Directory Layout & Layer Separation
```
starter/
├── app/
│   ├── __init__.py
│   ├── main.py                     # Litestar application factory, CORS, exception handlers
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── models.py               # SQLAlchemy 2.0 DeclarativeBase models
│   │   └── schemas.py              # msgspec Structs and Pydantic v2 schemas
│   ├── services/
│   │   ├── __init__.py
│   │   └── item_service.py         # Business domain repository service
│   └── controllers/
│       ├── __init__.py
│       └── item_controller.py      # Litestar Controller with typed endpoints
├── tests/
│   ├── __init__.py
│   └── test_app.py                 # Pytest suite with AsyncTestClient
├── Dockerfile                      # Rootless container running as UID 10001
├── docker-compose.yml              # Litestar + PostgreSQL 16 + Redis 7
└── requirements.txt                # Pinned production dependencies
```

## 3. Controller Architecture
- Group related endpoints using `litestar.Controller`:
  ```python
  from litestar import Controller, get, post
  from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED

  class ItemController(Controller):
      path = "/api/v1/items"
      tags = ["Items"]

      @get(status_code=HTTP_200_OK)
      async def list_items(self, item_service: ItemService) -> list[ItemSchema]:
          return await item_service.list()

      @post(status_code=HTTP_201_CREATED)
      async def create_item(self, data: ItemCreateSchema, item_service: ItemService) -> ItemSchema:
          return await item_service.create(data)
  ```

## 4. Error Handling & OpenAPI Configuration
- Register centralized exception handlers via `exception_handlers` dictionary in `Litestar(exception_handlers={...})`.
- Configure `OpenAPIConfig(title="...", version="1.0.0", render_plugins=[SwaggerRenderPlugin()])` to expose interactive API docs natively.


---

<a id="02-sqlalchemy-async-sessions-and-models"></a>
## 02 Sqlalchemy Async Sessions And Models

﻿---
id: "02-sqlalchemy-async-sessions-and-models"
title: "SQLAlchemy 2.0 Async Sessions & Database Invariants"
description: "Database persistence standards for asyncpg connection pooling, SQLAlchemy 2.0 DeclarativeBase, explicit indexing, and Alembic migrations."
globs: ["**/models.py", "**/migrations/*.py", "alembic.ini"]
alwaysApply: true
---

# 02 - SQLAlchemy 2.0 Async Sessions & Database Invariants

## 1. Async Engine & Session Lifecycle
- **Native AsyncIO Driver:** Standardize on `asyncpg` with SQLAlchemy 2.0:
  ```python
  from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

  engine = create_async_engine(
      settings.database_url,
      pool_size=20,
      max_overflow=10,
      pool_pre_ping=True,
      echo=False
  )
  session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
  ```
- **Session Injection:** Inject `AsyncSession` into request handlers and services via Litestar's DI. Ensure sessions are committed on success or rolled back automatically on unhandled exceptions.

## 2. Declarative Models & Indexing
- Define models inheriting from `sqlalchemy.orm.DeclarativeBase`:
  ```python
  from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
  from sqlalchemy import String, Boolean, DateTime, Index
  from datetime import datetime

  class Base(DeclarativeBase):
      pass

  class Item(Base):
      __tablename__ = "items"

      id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
      title: Mapped[str] = mapped_column(String(200), nullable=False)
      tenant_id: Mapped[str] = mapped_column(String(64), nullable=False)
      is_active: Mapped[bool] = mapped_column(Boolean, default=True)
      created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

      __table_args__ = (
          Index("idx_items_tenant_active", "tenant_id", "is_active"),
      )
  ```

## 3. Strict Parameterized Queries
- Always construct queries using SQLAlchemy 2.0 `select()` statements:
  ```python
  stmt = select(Item).where(Item.tenant_id == tenant_id, Item.is_active == True).order_by(Item.created_at.desc())
  result = await session.execute(stmt)
  items = result.scalars().all()
  ```
- Never construct raw SQL strings via interpolation (`f"SELECT * FROM items WHERE id = '{item_id}'"`).

## 4. Reversible Alembic Migrations
- Keep all database schema changes tracked inside versioned Alembic migrations.
- Verify migrations run bidirectionally: `alembic upgrade head` followed by `alembic downgrade -1`.


---

<a id="03-dto-architecture-and-msgspec-validation"></a>
## 03 Dto Architecture And Msgspec Validation

﻿---
id: "03-dto-architecture-and-msgspec-validation"
title: "First-Class DTOs & msgspec Validation Standards"
description: "Data Transfer Object (DTO) architecture, field masking, msgspec high-speed serialization, and schema validation invariants."
globs: ["**/schemas.py", "**/controllers/*.py"]
alwaysApply: true
---

# 03 - First-Class DTOs & msgspec Validation Standards

## 1. High-Performance Validation with msgspec & Pydantic
- Litestar provides native support for `msgspec.Struct`, which serializes and validates JSON up to 10x faster than standard Python libraries:
  ```python
  import msgspec

  class ItemCreateDTO(msgspec.Struct, forbid_unknown_fields=True):
      title: str
      tenant_id: str
      description: str = ""

  class ItemResponseDTO(msgspec.Struct):
      id: int
      title: str
      tenant_id: str
      is_active: bool
  ```

## 2. Litestar DTO System & Model Reflection
- Use Litestar's `SQLAlchemyDTO` to automatically generate request/response DTOs directly from SQLAlchemy models while enforcing strict field exclusions:
  ```python
  from litestar.plugins.sqlalchemy import SQLAlchemyDTO, SQLAlchemyDTOConfig

  class ItemWriteDTO(SQLAlchemyDTO[Item]):
      config = SQLAlchemyDTOConfig(exclude={"id", "created_at"})

  class ItemReadDTO(SQLAlchemyDTO[Item]):
      config = SQLAlchemyDTOConfig(exclude={"tenant_secret_key"})
  ```
- Attach DTOs to route handlers using `dto=ItemWriteDTO` for input validation and `return_dto=ItemReadDTO` for output filtering.

## 3. Strict Validation & Unknown Fields Rejection
- Always configure DTOs to reject unexpected payload attributes (`forbid_unknown_fields=True` in msgspec or `extra="forbid"` in Pydantic v2).
- Never allow clients to inject unverified internal attributes (such as `is_admin` or `role`) during model creation.


---

<a id="04-api-security-and-tenant-isolation"></a>
## 04 Api Security And Tenant Isolation

﻿---
id: "04-api-security-and-tenant-isolation"
title: "API Security, Guard Middleware & Tenant Isolation"
description: "Security invariants covering authentication middleware, BOLA/IDOR protection, rate limiting, and CORS configuration in Litestar."
globs: ["**/main.py", "**/controllers/*.py"]
alwaysApply: true
---

# 04 - API Security, Guard Middleware & Tenant Isolation

## 1. Authentication & Route Guards
- Implement token authentication using Litestar's `AbstractAuthenticationMiddleware`:
  ```python
  from litestar.middleware.authentication import AbstractAuthenticationMiddleware, AuthenticationResult
  from litestar.connection import ASGIConnection

  class JWTAuthenticationMiddleware(AbstractAuthenticationMiddleware):
      async def authenticate_request(self, connection: ASGIConnection) -> AuthenticationResult:
          token = connection.headers.get("Authorization")
          if not token or not token.startswith("Bearer "):
              raise NotAuthorizedException("Missing or malformed Authorization header")
          user = await verify_jwt_token(token[7:])
          return AuthenticationResult(user=user, auth=token)
  ```
- Protect routes with declarative guards:
  ```python
  def admin_guard(connection: ASGIConnection, _) -> None:
      if not connection.user or not connection.user.is_admin:
          raise PermissionDeniedException("Administrator clearance required")
  ```

## 2. BOLA / IDOR Tenant Isolation Invariants
- Enforce tenant isolation at the query execution level. Every lookup must verify the record matches both the requested ID and the authenticated tenant:
  ```python
  stmt = select(Item).where(Item.id == item_id, Item.tenant_id == connection.user.tenant_id)
  item = (await session.execute(stmt)).scalar_one_or_none()
  if item is None:
      raise NotFoundException("Item not found or access denied")
  ```

## 3. Explicit CORS Middleware (Zero Wildcards)
- Never use wildcard CORS `allow_origins=["*"]`. Always configure explicit origins from environment variables:
  ```python
  from litestar.config.cors import CORSConfig

  cors_config = CORSConfig(
      allow_origins=[o.strip() for o in settings.allowed_origins.split(",") if o.strip()],
      allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
      allow_headers=["*"],
      allow_credentials=True,
  )
  ```

## 4. Rate Limiting & Denial of Service Defense
- Integrate Litestar's `RateLimitConfig` targeting sensitive login and mutation endpoints to prevent brute-force attacks and resource starvation.


---

<a id="05-testing-verification-and-ci"></a>
## 05 Testing Verification And Ci

﻿---
id: "05-testing-verification-and-ci"
title: "Testing, Container Hardening & Token Benchmark"
description: "Testing standards using AsyncTestClient, pytest-asyncio, in-memory SQLite isolation, and rootless Docker execution (UID 10001)."
globs: ["tests/**/*.py", "Dockerfile", "evals/**"]
alwaysApply: true
---

# 05 - Testing, Container Hardening & Token Benchmark

## 1. Async Testing with AsyncTestClient
- Test Litestar routes using `litestar.testing.AsyncTestClient`:
  ```python
  import pytest
  from litestar.testing import AsyncTestClient
  from app.main import app

  @pytest.mark.asyncio
  async def test_health_endpoint():
      async with AsyncTestClient(app=app) as client:
          res = await client.get("/health")
          assert res.status_code == 200
          data = res.json()
          assert data["status"] == "ok"
          assert data["framework"] == "litestar"
  ```
- Fast execution invariant: Tests must complete within 2 seconds using an in-memory SQLite test database.

## 2. Container Hardening & Rootless Execution
- Docker containers must execute as an unprivileged user (`USER 10001:10001`):
  ```dockerfile
  RUN groupadd -g 10001 appgroup && \
      useradd -u 10001 -g appgroup -s /bin/sh appuser
  USER 10001:10001
  ```
- Discard build tools and header libraries in the multi-stage builder.

## 3. Token Benchmark Metric (Document 20 Part F)
- Benchmark verification: Run `python evals/runner.py --kit python-litestar-postgresql`.
- Target token consumption: ~22,100 tokens (Efficiency Tier: **A**).
- Justification: Clean layered dependency injection and first-class DTO typing eliminate boilerplate and ensure fast, predictable code generation by AI agents.


---

