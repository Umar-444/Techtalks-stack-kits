# Django 5 + Tailwind CSS + PostgreSQL — Claude Code Guidelines (CLAUDE.md)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Quick Reference & Non-Negotiable Standards
### Architecture for Django 5 + Tailwind CSS + PostgreSQL
# Architecture
Modular structure.

### 01 Framework Conventions
# Rule 1: Django 5 Framework Conventions & Architecture

## Context & Principles
- Follow the classic Django MTV (Model-Template-View) pattern with clean separation of domain concerns.
- Use Python 3.12+ type hints across models, forms, and view functions.
- Keep business logic encapsulated in domain managers or service layers, keeping views lean and focused on HTTP request/response orchestration.

## Standards
1. **App Structure**: Modularize features into dedicated apps inside `app/` or app root (e.g. `items`, `accounts`).
2. **Settings**: Never hardcode credentials. Load configuration via `environ` or `python-decouple` from `.env`.
3. **URL Namespacing**: Always register `app_name` in app `urls.py` and use `reverse()` or `{% url 'app_name:view_name' %}` in templates.
4. **Static Files**: Serve assets via WhiteNoise in production with storage hash caching (`CompressedManifestStaticFilesStorage`).


### Security for Django 5 + Tailwind CSS + PostgreSQL
# Security
Zero credential leaks.

### 02 Tailwind Design System
# Rule 2: Tailwind CSS Design System & Template Standards

## Context & Principles
- Use Tailwind CSS 3.4+ utility classes directly in Django templates without ad-hoc inline styles.
- Support both light and dark mode using the `dark:` variant and class-based theme switching.
- Standardize layout structure using a base template with reusable partials.

## Standards
1. **Base Layout**: All pages must extend `base.html` which includes responsive navigation, theme toggle, flash messages, and main content slot.
2. **Color Palette**: Use curated semantic colors (`brand-500`, `slate-900`, `emerald-500`) with high-contrast accessibility (WCAG AA compliant).
3. **Widget Styling**: Style form inputs with consistent Tailwind classes: `rounded-lg border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 focus:ring-2 focus:ring-brand-500`.
4. **Asset Build**: Compile Tailwind assets via the standalone CLI or node watcher into `static/css/dist/styles.css`.


### 03 Postgresql Orm
# Rule 3: PostgreSQL 16+ ORM & Query Performance

## Context & Principles
- Exploit PostgreSQL capabilities through Django's ORM: connection pooling (Psycopg 3), JSONB querying, and native full-text search.
- Eliminate N+1 query bottlenecks on all read views.

## Standards
1. **Eager Loading**: Always use `select_related()` for ForeignKey/OneToOne and `prefetch_related()` for ManyToMany/Reverse relationships.
2. **Atomic Transactions**: Wrap multi-model write operations inside `with transaction.atomic():` to guarantee database integrity.
3. **Indexes**: Define explicit `indexes = [models.Index(fields=[...])]` on frequently queried, filtered, or sorted columns.
4. **Psycopg 3 Pooling**: Use `CONN_MAX_AGE` and `psycopg_pool` settings to avoid per-request connection overhead.


### 04 Security And Csrf
# Rule 4: Security, Authentication & CSRF Protection

## Context & Principles
- Maintain zero-trust web application hygiene in compliance with OWASP Top 10 guidelines.
- Never bypass Django's built-in CSRF, clickjacking, or authentication defenses.

## Standards
1. **CSRF Tokens**: Every form POST request must include `{% csrf_token %}`. Never use `@csrf_exempt` unless integrating verified webhook signatures.
2. **Session Hardening**: Set `SESSION_COOKIE_SECURE=True`, `SESSION_COOKIE_HTTPONLY=True`, and `SESSION_COOKIE_SAMESITE='Lax'`.
3. **Password Validation**: Enforce standard Django password validators (`UserAttributeSimilarityValidator`, `MinimumLengthValidator`, `CommonPasswordValidator`, `NumericPasswordValidator`).
4. **Security Headers**: Enable `SECURE_BROWSER_XSS_FILTER`, `SECURE_CONTENT_TYPE_NOSNIFF`, `X_FRAME_OPTIONS = 'DENY'`, and strict Content-Security-Policy (CSP).


### 05 Testing And Arch
# Rule 5: Automated Testing & Architecture Verification

## Context & Principles
- Guarantee that all views, forms, and database mutations are covered by automated unit and integration tests.
- Run tests in isolated test databases using Django's `TestCase` or `pytest-django`.

## Standards
1. **View Tests**: Assert HTTP 200 responses, correct template rendering, and contextual query counts via `assertNumQueries()`.
2. **Form Tests**: Test valid submissions, missing required fields, and malicious input handling.
3. **Database Isolation**: Keep tests idempotent without residual side effects across test runs.
4. **CI Integration**: Ensure `python manage.py test --parallel` runs cleanly with zero warnings.


