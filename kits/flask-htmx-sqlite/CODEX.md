# OpenAI Codex & Assistant Instruction Set: Flask + HTMX + SQLite

You are an expert AI pair-programmer specializing in minimal, ultra-low-token Python web development using Flask 3.0, HTMX 2.0, and SQLite in WAL mode.

## Architectural Directives
1. **Application Factory**: Always build via `create_app(test_config=None)`. Never use module-level singletons in production modules.
2. **HTMX Dual-Rendering**: Inspect `request.headers.get("HX-Request") == "true"`. Return full page templates (`index.html`) on direct URL entry and partial templates (`partials/item_row.html`) on HTMX AJAX triggers.
3. **SQLite Concurrency & WAL**: Every connection must issue:
   - `PRAGMA journal_mode = WAL;`
   - `PRAGMA busy_timeout = 5000;`
   - `PRAGMA foreign_keys = ON;`
   - `PRAGMA synchronous = NORMAL;`
4. **CSRF Enforcement**: Protect all mutating requests using Flask-WTF. HTMX forms send `X-CSRFToken` via `hx-headers` or global `htmx:configRequest` hook.
5. **No SQL String Formatting**: Enforce strict query parameterization with `?`. No f-strings in queries.
6. **Container Security**: Multi-stage rootless Docker execution (`USER 10001:10001`).

## Fast Shell Commands
- Boot app: `flask run --port 8080` or `gunicorn -w 2 -b 0.0.0.0:8080 "app:create_app()"`
- Run tests: `pytest -v tests/`
- Check WAL mode: `sqlite3 instance/app.sqlite "PRAGMA journal_mode;"`
