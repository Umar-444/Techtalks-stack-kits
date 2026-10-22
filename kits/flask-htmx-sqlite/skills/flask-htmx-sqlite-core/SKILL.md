---
name: flask-htmx-sqlite-core
description: Comprehensive agent reference and operating manual for Flask 3.0, HTMX 2.0, and SQLite in WAL mode.
---
# Flask + HTMX + SQLite Core Operations Manual

## 1. Stack Architecture Overview
This stack represents the flagship ultra-low-token Python web architecture. It avoids the heavy cognitive and token load of client-side JavaScript frameworks (React/Vue/Angular) while providing dynamic, reactive single-page experience via HTMX 2.0 over native HTML fragments.

## 2. Invariants & Rules of Engagement
1. **Application Factory**: Always build Flask via `create_app(test_config=None)`.
2. **Dual-Rendering**: Inspect `request.headers.get("HX-Request") == "true"` to differentiate between full document renders and HTMX partial fragment returns.
3. **SQLite WAL Mode**: Set `PRAGMA journal_mode = WAL;` and `PRAGMA busy_timeout = 5000;` on every database connection.
4. **CSRF Validation**: All POST/PUT/DELETE mutations must be protected by Flask-WTF CSRF tokens forwarded through `X-CSRFToken`.
5. **No SQL Injections**: Zero unparameterized SQL queries. Always use placeholder parameters (`?`).
6. **Container User**: Non-root container UID `10001:10001`.

## 3. Fast Reference Commands
- **Boot Application**: `flask --app "app:create_app()" run --port 8080 --debug`
- **Initialize DB**: `flask --app "app:create_app()" init-db`
- **Run Tests**: `pytest -v tests/`
- **Container Build**: `docker compose up --build -d`
