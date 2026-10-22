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
