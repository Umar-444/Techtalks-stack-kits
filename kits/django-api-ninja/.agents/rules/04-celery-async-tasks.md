# 04 Celery Async Tasks

# Celery Async Background Workers & Queue Management

# Celery Async Worker Invariants
- Offload long-running operations (>150ms), email sending, and external API calls to Celery tasks.
- Pass database primary keys (project_id: int) to tasks rather than complex serialized model instances.
- Set task timeouts: 	ime_limit=300 and soft_time_limit=240 to prevent hung worker threads.
- Ensure all Celery tasks are strictly idempotent with retry policies (ind=True, max_retries=3).

