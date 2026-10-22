# 03 Pydantic Schemas And Serialization

﻿---
id: "03-pydantic-schemas-and-serialization"
title: "Pydantic v2 Schemas & Serialization Standards"
description: "Validation rules for Django Ninja Schema models, request payload bounds, response filtering, and custom error formatting."
globs: ["**/schemas.py", "**/api.py"]
alwaysApply: true
---

# 03 - Pydantic v2 Schemas & Serialization Standards

## 1. Schema Inheritance & Configuration
- Inherit all API schemas from `ninja.Schema` (which wraps Pydantic v2 `BaseModel`):
  ```python
  from ninja import Schema, Field
  from datetime import datetime
  from typing import Optional

  class ProjectIn(Schema):
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
  ```

## 2. Mass Assignment Defense & Field Exclusion
- Never expose sensitive internal model fields (`password_hash`, `stripe_customer_id`, `internal_notes`) in response schemas.
- Explicitly declare every field returned in `ProjectOut`. Never use unbounded dictionary serializers (`dict(instance.__dict__)`).

## 3. Strict Input Coercion
- Set `extra = "forbid"` in `model_config` on mutation schemas to reject unknown query or JSON body attributes:
  ```python
  class StrictSchema(Schema):
      model_config = {"extra": "forbid"}
  ```

## 4. Custom Error Handling
- Capture validation errors gracefully via Django Ninja's exception handler:
  ```python
  @api.exception_handler(ValidationError)
  def validation_error_handler(request, exc):
      return api.create_response(
          request,
          {"detail": exc.errors(), "code": "VALIDATION_ERROR"},
          status=422
      )
  ```

