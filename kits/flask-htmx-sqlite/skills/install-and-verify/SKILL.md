---
name: install-and-verify
description: Comprehensive preflight verification, virtual environment setup, and test runner execution for Flask + HTMX + SQLite.
---
# Install and Verify Skill: Flask + HTMX + SQLite

## 1. Environment Initialization
Create an isolated Python 3.12+ virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Configuration Setup
Generate the instance directory and local environment configuration:
```bash
mkdir -p instance
cp .env.example .env
```

## 3. Database Schema Initialization & WAL Verification
Run the database CLI initialization command and check WAL mode:
```bash
flask --app "app:create_app()" init-db
sqlite3 instance/app.sqlite "PRAGMA journal_mode;"
# Output must be: wal
```

## 4. Run Test Suite
Verify that all unit and fragment tests pass:
```bash
pytest -v tests/
```

## 5. Local Development Server
Boot the development server with live reload:
```bash
flask --app "app:create_app()" run --port 8080 --debug
```
Open `http://localhost:8080/` in the browser or check `curl http://localhost:8080/health`.
