# GitHub Copilot Instructions for Flask + HTMX + SQLite
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## 01 Framework Architecture And Standards
﻿---
id: framework-architecture-and-standards
title: Framework Architecture & Standards
globs: "**/*.py"
alwaysApply: true
---
# Flask Application Factory Architecture & Production Standards

## 1. Application Factory Pattern
- Always construct Flask applications using the factory pattern: `create_app(test_config=None)`.
- Never use global app instances or module-level `app = Flask(__name__)` in production modules.
- Register all functional route groups using Flask Blueprints with explicit URL prefixes:
  ```python
  from flask import Flask

  def create_app(test_config=None):
      app = Flask(__name__, instance_relative_config=True)
      app.config.from_mapping(
          SECRET_KEY=os.environ.get("SECRET_KEY", "dev-insecure-key-change-me"),
          DATABASE=os.path.join(app.instance_path, "app.sqlite"),
          WTF_CSRF_TIME_LIMIT=3600,
      )
      if test_config:
          app.config.update(test_config)
      
      # Initialize extensions
      init_app(app)
      csrf.init_app(app)
      
      # Register blueprints
      from app.routes import main_bp
      app.register_blueprint(main_bp)
      
      return app
  ```

## 2. Directory Layout & Separation of Concerns
```
starter/
├── app/
│   ├── __init__.py        # Application factory & extension init
│   ├── db.py              # SQLite connection lifecycle & WAL pragma management
│   ├── routes.py          # HTTP handlers supporting full & HTMX partial views
│   ├── schema.sql         # DDL migrations & initial schema
│   ├── static/
│   │   ├── css/style.css  # Dark-mode styling tokens
│   │   └── js/htmx.min.js # Vendored or CDN fallback
│   └── templates/
│       ├── base.html      # Outer layout with CSRF token & htmx:configRequest
│       ├── index.html     # Full page container
│       └── partials/      # HTMX fragment targets (item_row.html, item_list.html)
├── tests/
│   └── test_app.py        # Pytest test client fixtures & fragment tests
├── Dockerfile             # Multi-stage rootless container (USER 10001:10001)
├── docker-compose.yml     # Standalone compose runner
└── requirements.txt       # Hardened dependency pins
```

## 3. ASGI/WSGI Production Server Invariants
- Deploy with Gunicorn using gevent, eventlet, or gthread workers for concurrent I/O:
  ```bash
  gunicorn -w 4 -k gthread --threads 4 -b 0.0.0.0:8080 "app:create_app()"
  ```
- Gracefully handle SIGTERM and SIGINT to flush WAL write transactions before process termination.


## 02 Htmx Reactivity And Jinja Rendering
﻿---
id: htmx-reactivity-and-jinja-rendering
title: HTMX Reactivity & Jinja2 Partial Rendering
globs: "**/*.{py,html}"
alwaysApply: true
---
# HTMX 2.0 Integration & Dual-Render View Architecture

## 1. Dual-Rendering Pattern via Request Headers
- Handlers MUST detect if an incoming request is driven by HTMX via `HX-Request`:
  ```python
  from flask import Blueprint, request, render_template

  main_bp = Blueprint("main", __name__)

  @main_bp.route("/items", methods=["GET"])
  def list_items():
      items = get_db_items(search=request.args.get("q", "").strip())
      if request.headers.get("HX-Request") == "true":
          return render_template("partials/item_list.html", items=items)
      return render_template("index.html", items=items)
  ```
- This guarantees direct deep-linking (full page navigation) and lightning-fast partial DOM swaps from the exact same URL.

## 2. HTMX 2.0 Attributes & Swapping Semantics
- Use explicit swap strategies:
  - `hx-swap="outerHTML"` for updating full table rows or cards.
  - `hx-swap="innerHTML"` for container updates or tab body switches.
  - `hx-swap="beforeend"` for append-only log feeds or paginated items.
- Always implement progressive enhancement:
  ```html
  <form hx-post="/items"
        hx-target="#items-tbody"
        hx-swap="afterbegin"
        hx-on::after-request="if(event.detail.successful) this.reset()">
      <input type="text" name="title" required placeholder="Item title..." />
      <button type="submit">Add Item</button>
  </form>
  ```

## 3. Inline Search with Debouncing
- For responsive filtering, utilize `hx-trigger="keyup changed delay:300ms, search"`:
  ```html
  <input type="search"
         name="q"
         placeholder="Filter records..."
         hx-get="/items"
         hx-trigger="keyup changed delay:300ms, search"
         hx-target="#items-tbody"
         hx-indicator="#search-spinner" />
  ```
- Always render loading indicators cleanly via `#search-spinner.htmx-indicator`.


## 03 Sqlite Wal Mode And Concurrency
﻿---
id: sqlite-wal-mode-and-concurrency
title: SQLite WAL Mode & Concurrency Architecture
globs: "**/*.{py,sql}"
alwaysApply: true
---
# SQLite Production Concurrency & WAL Performance Standards

## 1. Mandatory SQLite PRAGMA Configuration
- SQLite must always be initialized with Write-Ahead Logging (WAL) and explicit busy timeout limits on every new connection:
  ```python
  import sqlite3
  from flask import g, current_app

  def get_db():
      if "db" not in g:
          g.db = sqlite3.connect(
              current_app.config["DATABASE"],
              detect_types=sqlite3.PARSE_DECLTYPES
          )
          g.db.row_factory = sqlite3.Row
          
          # Enforce production concurrency pragmas
          cursor = g.db.cursor()
          cursor.execute("PRAGMA journal_mode = WAL;")
          cursor.execute("PRAGMA synchronous = NORMAL;")
          cursor.execute("PRAGMA foreign_keys = ON;")
          cursor.execute("PRAGMA busy_timeout = 5000;")  # 5-second lock queue
          cursor.close()
      return g.db
  ```

## 2. Request Lifecycle Connection Teardown
- Register automatic connection closure via Flask's teardown callback:
  ```python
  def close_db(e=None):
      db = g.pop("db", None)
      if db is not None:
          db.close()

  def init_app(app):
      app.teardown_appcontext(close_db)
      app.cli.add_command(init_db_command)
  ```

## 3. Atomic Transactions & Write Contention Defenses
- When performing mutations involving multiple statements, use explicit transaction contexts:
  ```python
  db = get_db()
  try:
      with db:
          db.execute("INSERT INTO audit_logs (action) VALUES (?)", ("create",))
          db.execute("INSERT INTO items (title, content) VALUES (?, ?)", (title, content))
  except sqlite3.OperationalError as exc:
      if "database is locked" in str(exc):
          current_app.logger.warning("SQLite write contention encountered: %s", exc)
          # Handled by busy_timeout, fallback to 503 retry-after
      raise
  ```


## 04 Csrf Security And Input Validation
﻿---
id: csrf-security-and-input-validation
title: CSRF Security & Input Sanitization
globs: "**/*.{py,html,js}"
alwaysApply: true
---
# CSRF Defenses, HTMX Security Headers & Input Sanitization

## 1. Flask-WTF CSRF with HTMX Headers
- All state-changing requests (POST, PUT, PATCH, DELETE) MUST validate CSRF tokens.
- Inject the token into the global HTML layout meta tag:
  ```html
  <meta name="csrf-token" content="{{ csrf_token() }}">
  ```
- Configure HTMX to automatically append `X-CSRFToken` to every outgoing AJAX request:
  ```html
  <body hx-headers='{"X-CSRFToken": "{{ csrf_token() }}"}'>
  ```
  Or via JavaScript event hook:
  ```javascript
  document.body.addEventListener('htmx:configRequest', function(evt) {
      evt.detail.headers['X-CSRFToken'] = document.querySelector('meta[name="csrf-token"]').content;
  });
  ```

## 2. SQL Injection Prevention & Strict Parameterization
- NEVER use Python f-strings, `%` formatting, or manual string concatenation in SQL queries.
- ALWAYS use parameter placeholders (`?` in sqlite3):
  ```python
  # SECURE:
  cursor.execute("SELECT * FROM items WHERE tenant_id = ? AND title LIKE ?", (tenant_id, f"%{query}%"))

  # FORBIDDEN (Vulnerable to SQLi):
  cursor.execute(f"SELECT * FROM items WHERE tenant_id = '{tenant_id}'")
  ```

## 3. Strict Content Security Policy (CSP) & Security Headers
- Set standard security headers on every response:
  ```python
  @app.after_request
  def set_security_headers(response):
      response.headers["X-Content-Type-Options"] = "nosniff"
      response.headers["X-Frame-Options"] = "DENY"
      response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
      response.headers["Content-Security-Policy"] = (
          "default-src 'self'; "
          "script-src 'self' 'unsafe-eval' https://unpkg.com; "
          "style-src 'self' 'unsafe-inline'; "
          "img-src 'self' data:; "
          "connect-src 'self';"
      )
      return response
  ```


## 05 Testing Verification And Ci
﻿---
id: testing-verification-and-ci
title: Testing, Verification & CI Invariants
globs: "**/*.py"
alwaysApply: true
---
# Testing Standards, HTML Fragment Assertions & CI Pipeline

## 1. Pytest Test Client & In-Memory Isolation
- Always configure an isolated temporary database in tests so unit runs never mutate real files:
  ```python
  import tempfile
  import os
  import pytest
  from app import create_app
  from app.db import init_db

  @pytest.fixture
  def app():
      db_fd, db_path = tempfile.mkstemp()
      app = create_app({
          "TESTING": True,
          "DATABASE": db_path,
          "WTF_CSRF_ENABLED": False,  # Simplified client testing, or enabled with test CSRF
      })
      with app.app_context():
          init_db()
      yield app
      os.close(db_fd)
      os.unlink(db_path)

  @pytest.fixture
  def client(app):
      return app.test_client()
  ```

## 2. Testing HTMX Fragment Swaps vs Full Page Navigation
- Assert that requests without `HX-Request` return full HTML shells (`<html`, `<head`, `<body>`).
- Assert that requests with `headers={"HX-Request": "true"}` return ONLY targeted HTML fragments:
  ```python
  def test_list_items_htmx_partial(client):
      res = client.get("/items", headers={"HX-Request": "true"})
      assert res.status_code == 200
      assert b"<tr" in res.data or b"<div class=\"item-row\"" in res.data
      assert b"<!DOCTYPE html>" not in res.data
  ```

## 3. Automated Security Audits in CI
- Code must pass:
  1. `gitleaks detect --no-git` with 0 secret leaks.
  2. `semgrep scan --config p/owasp-top-ten --config p/security-code-scan` with 0 blocking findings.
  3. `python tools/validate_manifest.py` ensuring complete physical manifest parity.
  4. `python tools/transpiler.py --check` guaranteeing 0 dialect drift.


