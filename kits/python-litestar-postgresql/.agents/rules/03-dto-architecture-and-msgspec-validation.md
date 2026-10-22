# 03 Dto Architecture And Msgspec Validation

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

