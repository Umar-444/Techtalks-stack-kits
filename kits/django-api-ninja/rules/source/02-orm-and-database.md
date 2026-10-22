# Django ORM Invariants, Query Optimization & Migrations

# Django ORM & Database Invariants
- Prevent N+1 queries: ALWAYS use select_related() for foreign keys and prefetch_related() for many-to-many relationships.
- Add explicit db_index=True or indexes = [models.Index(...)] on frequently queried fields.
- Migrations MUST be backward-compatible; never drop or rename a column without a two-phase deploy.
- Scope all model queries by tenant or authenticated user ID to eliminate BOLA / IDOR vulnerabilities.
