# 04 Authentication Security And Celery

﻿---
id: "04-authentication-security-and-celery"
title: "Authentication, API Security & Celery Task Queue"
description: "Security standards for Bearer token authentication, API keys, Celery 5.4 async background worker orchestration, and Redis broker settings."
globs: ["**/api.py", "**/celery.py", "**/settings.py"]
alwaysApply: true
---

# 04 - Authentication, API Security & Celery Task Queue

## 1. Authentication with HttpBearer & API Keys
- Protect endpoints using Django Ninja's native security classes (`HttpBearer`, `APIKeyHeader`):
  ```python
  from ninja.security import HttpBearer
  from django.contrib.auth.models import User

  class JWTAuth(HttpBearer):
      def authenticate(self, request, token):
          user = verify_jwt_token(token)
          if user:
              return user
          return None

  auth = JWTAuth()

  @router.get("/protected", auth=auth)
  def protected_endpoint(request):
      return {"user": request.auth.username}
  ```

## 2. Celery 5.4 Async Task Dispatching
- Never perform blocking network calls (sending transactional emails, indexing embeddings, calling payment gateways) inside HTTP request handlers.
- Offload long-running operations to Celery background tasks:
  ```python
  from config.celery import app as celery_app

  @celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
  def send_project_notification(self, project_id: int):
      try:
          # Background processing logic
          pass
      except Exception as exc:
          raise self.retry(exc=exc)
  ```
- Trigger tasks with `.delay()` after transactions commit:
  ```python
  from django.db import transaction

  transaction.on_commit(lambda: send_project_notification.delay(project.id))
  ```

## 3. Celery Security & Serialization Invariants
- Enforce strict JSON serialization in `settings.py`:
  ```python
  CELERY_ACCEPT_CONTENT = ["json"]
  CELERY_TASK_SERIALIZER = "json"
  CELERY_RESULT_SERIALIZER = "json"
  ```
- Never allow `pickle` serialization in Celery, as it enables arbitrary remote code execution (RCE) if Redis is compromised.

