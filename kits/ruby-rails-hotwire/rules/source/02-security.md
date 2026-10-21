---
id: security-invariants
title: Security Invariants for Ruby on Rails 8 + Hotwire (Turbo + Stimulus) + SQLite/PostgreSQL
globs: "*"
alwaysApply: true
---

# Security Invariants
- Verify tenant boundary before reading or writing any persistent state.
- Sanitize all external inputs using validated schemas.
- Reject requests with missing or expired bearer tokens.
