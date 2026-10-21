# Community Starter Issues (Good First Issues)

These 5 issues are pre-scoped tasks from our platform roadmap. They are ideal for community contributors looking to help build the TechTalks Stack Kits ecosystem.

---

### Issue 1: [Kit #2] Laravel 12 + Livewire 4 + Flux UI: Rules & Design System
- **Kit Directory:** `kits/laravel-livewire-postgresql/`
- **Objective:** Author single-source rules in `rules/source/` covering Volt single-file components, Folio page routing, and Flux UI design tokens in `DESIGN.md`.
- **Files to Deliver:**
  - `rules/source/01-livewire-volt-folio.md`
  - `rules/source/02-flux-ui-tokens.md`
  - `DESIGN.md`
- **Verification:** `python tools/transpiler.py --kit kits/laravel-livewire-postgresql --check`

---

### Issue 2: [Kit #3] Laravel + MongoDB (NoSQL): Eloquent Query Pattern Skills
- **Kit Directory:** `kits/laravel-mongodb/`
- **Objective:** Create a specialized `SKILL.md` under `skills/mongodb-aggregation/` teaching agents how to construct high-performance MongoDB aggregation pipelines and embedded document updates using `mongodb/laravel-mongodb`.
- **Files to Deliver:**
  - `skills/mongodb-aggregation/SKILL.md`
  - `rules/source/01-mongodb-eloquent.md`
- **Verification:** `python tools/validate_manifest.py kits/laravel-mongodb/kit.yaml`

---

### Issue 3: [Kit #4] Laravel + MySQL Enterprise: Larastan Level 8 Guardrails
- **Kit Directory:** `kits/laravel-mysql/`
- **Objective:** Author architectural testing rules in `rules/source/01-enterprise-boundaries.md` and pre-configure `phpstan.neon` at Level 8 in the starter directory.
- **Files to Deliver:**
  - `starter/phpstan.neon`
  - `rules/source/01-enterprise-boundaries.md`
  - `starter/tests/ArchTest.php`
- **Verification:** `python tools/transpiler.py --kit kits/laravel-mysql --check`

---

### Issue 4: [Kit #5] Next.js 15+ + Supabase: Server Actions Security Standard
- **Kit Directory:** `kits/nextjs-approuter-supabase/`
- **Objective:** Author single-source rules enforcing Zod payload validation on every Server Action, and create a `skills/supabase-rls/SKILL.md` workflow for PostgreSQL Row-Level Security policies.
- **Files to Deliver:**
  - `rules/source/01-server-actions-zod.md`
  - `skills/supabase-rls/SKILL.md`
  - `SECURITY.md`
- **Verification:** `python tools/transpiler.py --kit kits/nextjs-approuter-supabase --check`

---

### Issue 5: [Kit #6] Django 5+ + Tailwind: Celery Queue & Custom Auth Starter
- **Kit Directory:** `kits/django-tailwind-postgresql/`
- **Objective:** Configure the starter Docker Compose and environment for Celery background tasks with Redis and a custom user model authentication system.
- **Files to Deliver:**
  - `starter/docker-compose.yml`
  - `starter/Dockerfile`
  - `starter/.env.example`
  - `rules/source/01-django-conventions.md`
- **Verification:** `python tools/validate_manifest.py kits/django-tailwind-postgresql/kit.yaml`
