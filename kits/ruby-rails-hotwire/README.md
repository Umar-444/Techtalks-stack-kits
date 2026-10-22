# Ruby on Rails 8 + Hotwire (Turbo 8 + Stimulus 3) Stack Kit

A production-grade, highly optimized Rails 8 stack featuring the complete **Solid Suite** (Solid Cache, Solid Queue, Solid Cable), Hotwire Turbo 8 page morphing, and zero-external-dependency infrastructure.

## Stack Overview
- **Language**: Ruby 3.3.6+
- **Framework**: Ruby on Rails 8.0.0+
- **Frontend Reactive Engine**: Hotwire (Turbo 8 + Stimulus 3)
- **Background & Real-time**: Solid Cache, Solid Queue, Solid Cable
- **Database**: SQLite 3.45+ (Development/Single-node) / PostgreSQL 16.4+ (Production)
- **Asset Pipeline**: Propshaft & Importmaps
- **Security**: Brakeman, Strong Parameters, HttpOnly Session Protection

## Quickstart

### 1. Local Development
```bash
bundle install
bin/rails db:prepare
bin/rails server
```
Visit `http://localhost:3000` to interact with real-time posts.

### 2. Run with Docker Compose
```bash
docker compose up --build
```

### 3. Run Tests & Security Analysis
```bash
bin/rails test
bundle exec brakeman -q -z
```

### 4. Health Probe
```bash
curl -s http://localhost:3000/healthz
# Returns: {"status":"ok","app":"ruby-rails-hotwire","version":"1.0.0"}
```

## Security & Verification Standards
- Zero Brakeman warning policy in CI (`brakeman -q -z`).
- Strict Strong Parameters mass-assignment protection.
- Database foreign key constraints and compound index coverage.
- Fully documented in [`VERIFICATION.md`](VERIFICATION.md).
