# Django 5 + Tailwind CSS + PostgreSQL 16+ Stack Kit

[![Stack Status: Ready to Ship](https://img.shields.io/badge/status-Ready%20to%20Ship-emerald?style=flat-square)](kit.yaml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue?style=flat-square)](https://www.python.org/)
[![Django 5.1](https://img.shields.io/badge/django-5.1-0C4B33?style=flat-square)](https://www.djangoproject.com/)
[![Tailwind CSS 3.4](https://img.shields.io/badge/tailwind-3.4-38B2AC?style=flat-square)](https://tailwindcss.com/)
[![PostgreSQL 16](https://img.shields.io/badge/postgresql-16-336791?style=flat-square)](https://www.postgresql.org/)

Batteries-included full-stack starter kit combining Django 5.1 MTV architecture, Tailwind CSS design system, and robust PostgreSQL 16+ persistence with connection pooling.

---

## Architecture Overview

```
                   +-----------------------------------+
                   |           Browser / Client        |
                   +-----------------+-----------------+
                                     |
                       HTTPS Requests (HTML + CSRF)
                                     v
                   +-----------------+-----------------+
                   |       Gunicorn / WhiteNoise       |
                   |   (Static Hash Caching + Assets)  |
                   +-----------------+-----------------+
                                     |
                                     v
                   +-----------------+-----------------+
                   |        Django 5.1 MTV Core        |
                   |  - Middleware (CSRF, Security)    |
                   |  - Views (ListView, CreateView)   |
                   |  - ModelForms (Tailwind Widgets)  |
                   |  - Templates (Tailwind UI Tokens) |
                   +-----------------+-----------------+
                                     |
                           Psycopg 3 Connection Pool
                                     v
                   +-----------------+-----------------+
                   |         PostgreSQL 16+ DB         |
                   |   (Atomic Transactions, Indexes)  |
                   +-----------------------------------+
```

---

## Key Features

1. **Django 5.1 & Python 3.12+**: Modern asynchronous-capable web framework with robust security middleware.
2. **Tailwind CSS 3.4+ Design System**: Clean typography, light/dark mode switching, responsive container cards, and accessible forms.
3. **PostgreSQL 16+ Integration**: Configured with Psycopg 3 connection pooling (`CONN_MAX_AGE=600`), health checks, and composite B-tree indexes.
4. **Zero-Trust Security**: Built-in CSRF validation, XSS protection, clickjacking prevention (`X-Frame-Options: DENY`), and secure cookies.
5. **Pre-Wired Docker Compose**: Automated PostgreSQL health checks, volume persistence, and one-command local orchestration.
6. **Automated Testing Suite**: Pre-configured `TestCase` and `pytest-django` tests verifying views, forms, and database isolation.

---

## Quickstart with Docker Compose

Run the entire stack with Docker:

```bash
# 1. Clone the repository
git clone https://github.com/Umar-444/Techtalks-stack-kits.git
cd Techtalks-stack-kits/kits/django-tailwind-postgresql/starter

# 2. Start services (web + PostgreSQL 16)
docker compose up --build
```

Access the application:
- **Main Web UI**: [http://localhost:8000/](http://localhost:8000/)
- **Health Check**: [http://localhost:8000/healthz](http://localhost:8000/healthz)
- **Django Admin**: [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## Native Local Setup

### 1. Prerequisites
- Python 3.12+
- PostgreSQL 16+ running locally (or SQLite fallback)

### 2. Virtual Environment & Dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Environment Configuration
```bash
cp .env.example .env
```
Update `.env` with your PostgreSQL database credentials if running PostgreSQL locally. If omitted, the starter automatically falls back to SQLite for instant local prototyping.

### 4. Database Migrations
```bash
python manage.py makemigrations app
python manage.py migrate
```

### 5. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver 127.0.0.1:8000
```

---

## Running Automated Tests

Run the full test suite with Django's native test runner:
```bash
python manage.py test
```

Or using `pytest`:
```bash
pytest
```

---

## Available Agent Skills

This kit exposes 4 standardized agent operations skills:
- `django-tailwind-theme`: Setup, compile, and configure Tailwind design tokens and dark mode.
- `django-model-form`: Secure model-backed forms styled with Tailwind CSS utility classes and CSRF validation.
- `postgres-connection-pooling`: PostgreSQL connection pooling configuration, JSONB queries, and index strategies.
- `django-security-audit`: Production deployment checklists, security headers, and automated security scanning.

---

## Production Deployment Checklist

1. Set `DEBUG=0` in `.env`.
2. Generate a secure, unique `SECRET_KEY`.
3. Configure `ALLOWED_HOSTS` with your production domain.
4. Run `python manage.py check --deploy` to verify all security headers.
5. Collect static assets: `python manage.py collectstatic --noinput`.
6. Start with Gunicorn:
   ```bash
   gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
   ```

---

## License & Maintenance
Maintained by **TechTalks Python Engineering Group** under the MIT License.
