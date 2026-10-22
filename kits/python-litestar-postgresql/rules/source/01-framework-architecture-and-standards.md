---
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
