---
name: postgres-connection-pooling
description: Configure PostgreSQL 16+ connection pooling, JSONB indexes, and query optimizations in Django.
---

# PostgreSQL Connection Pooling Skill

## Purpose
Configures production-grade database connectivity for Django 5 with PostgreSQL 16+ using Psycopg 3 and connection pooling.

## Database Configuration in settings.py
```python
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'app_db'),
        'USER': os.environ.get('POSTGRES_USER', 'app_user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'secret'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        'CONN_MAX_AGE': int(os.environ.get('CONN_MAX_AGE', 600)),
        'CONN_HEALTH_CHECKS': True,
        'OPTIONS': {
            'pool': True,
        }
    }
}
```

## Performance Best Practices
- Always create indexes on queried timestamp and foreign key columns.
- Use `select_related()` and `prefetch_related()` across all list views.
- Use `bulk_create()` and `bulk_update()` for batch operations.
