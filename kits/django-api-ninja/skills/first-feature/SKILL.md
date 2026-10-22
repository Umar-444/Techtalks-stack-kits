---
name: first-feature
description: Build the canonical first API resource with CRUD endpoints, authentication, and Celery async notification.
---

# First Feature Skill: CRUD Resource & Celery Task

## Objective
Implement a secure `/api/items/` endpoint with CRUD operations and background async notifications.

## Implementation Steps
1. Define PostgreSQL Model in `app/models.py`.
2. Define Pydantic Schema in `app/schemas.py`.
3. Implement Router endpoints in `app/api.py`.
4. Trigger Celery async task on item creation:
   ```python
   process_item_async.delay(item.id)
   ```

## Done Means
A developer or agent posts a new item to `/api/items/` with an API token, item saves to PostgreSQL, and Celery processes background tasks.
