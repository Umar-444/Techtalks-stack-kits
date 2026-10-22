# Assistant Guidelines for Ruby on Rails 8 + Hotwire Stack Kit

## Stack Overview
- Language: Ruby 3.3.6+
- Framework: Ruby on Rails 8.0.0+
- Front-End: Hotwire (Turbo 8 + Stimulus 3)
- Solid Stack: Solid Cache, Solid Queue, Solid Cable
- Database: SQLite 3.45+ (Development/Single-node) / PostgreSQL 16.4+ (Multi-node Production)
- Security: Brakeman, Strong Parameters, HttpOnly Cookies, CSRF verification

## Mandatory Rules
1. Maintain omakase Rails 8 architecture: RESTful controllers, domain logic in models, progressive enhancement via Stimulus.
2. Use Turbo Streams and Turbo 8 morphing for dynamic UI updates without client-side SPA frameworks.
3. Strict Strong Parameters on all mutating controller actions. Never call `params.permit!`.
4. Zero Brakeman warnings: Run `brakeman -q -z` before deploying or validating changes.
5. All database operations must be indexed and protected against N+1 queries.
