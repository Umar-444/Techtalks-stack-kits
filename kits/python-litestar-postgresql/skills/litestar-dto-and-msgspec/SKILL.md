---
name: "litestar-dto-and-msgspec"
description: "Master Litestar's first-class DTO system, SQLAlchemyDTO reflection, field masking, and msgspec high-speed struct serialization."
---

# Skill: Litestar First-Class DTOs and msgspec Serialization

Use this skill to design performant, type-safe data transfer layers without manual model mapping boilerplate.

## 1. Automatic Model Reflection with SQLAlchemyDTO
Instead of writing separate input and output schemas manually for every database model, declare a `SQLAlchemyDTO`:
```python
from litestar.plugins.sqlalchemy import SQLAlchemyDTO, SQLAlchemyDTOConfig

# Input DTO: excludes auto-generated fields
class UserCreateDTO(SQLAlchemyDTO[User]):
    config = SQLAlchemyDTOConfig(exclude={"id", "created_at", "updated_at"})

# Output DTO: excludes confidential fields
class UserResponseDTO(SQLAlchemyDTO[User]):
    config = SQLAlchemyDTOConfig(exclude={"password_hash", "internal_notes"})
```

Attach to routes:
```python
@post("/users", dto=UserCreateDTO, return_dto=UserResponseDTO)
async def create_user(data: User, user_service: UserService) -> User:
    return await user_service.create(data)
```

## 2. Ultra-Fast JSON Serialization with msgspec
For maximum throughput on high-traffic endpoints, use `msgspec.Struct`:
- Native C/Rust implementation delivers ~10x faster encoding/decoding than standard Python `json`.
- Enforces strict schema validation with zero runtime overhead.
- Supports zero-copy deserialization for high-concurrency microservices.
