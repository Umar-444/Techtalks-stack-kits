# Flask + HTMX + SQLite

> **TechTalks Stack Kits — Token-Light line**
> **Efficiency Tier:** `A+` · **Median tokens to reference build:** `15,900`

A minimalist Python full-stack kit: an application-factory Flask 3 backend,
HTMX 2 for reactive DOM updates without a JavaScript bundle, and SQLite in WAL
mode for persistence. The smallest complete stack in the catalogue, and the one
an agent can finish in the fewest tokens.

## 1. Why this stack

**One process, no build step.** There is no bundler, no node_modules, and no
separate frontend service. HTMX ships as a single script tag and drives updates
by swapping server-rendered Jinja partials, so the agent writes one language and
one template layer instead of maintaining a client-side state mirror.

**SQLite is the right default more often than it looks.** With WAL mode enabled,
readers never block the writer, which removes the failure mode that usually
pushes small apps onto Postgres prematurely. `PRAGMA busy_timeout` absorbs write
contention instead of surfacing `database is locked` to users.

**Token efficiency is a design goal, not a side effect.** Fewer moving parts
means less context an agent must hold to make a correct change — which is why
this kit benchmarks at Tier A+.

### When to choose something else

| If you need | Use instead |
|---|---|
| Multi-writer concurrency at scale | `django-tailwind-postgresql` |
| A typed API surface with OpenAPI | `django-api-ninja` |
| A background job queue | `python-litestar-postgresql` |

## 2. Stack

| Layer | Component | Version |
|---|---|---|
| Language | Python | `>= 3.12` |
| Framework | Flask (application factory) | `>= 3.0.3` |
| Interactivity | HTMX | `>= 2.0.3` |
| Database | SQLite (WAL mode) | `>= 3.45` |
| Templating | Jinja2 server-rendered partials | bundled |

## 3. Layout

```text
kits/flask-htmx-sqlite/
├── kit.yaml                  # Machine-readable manifest
├── README.md                 # This guide
├── DESIGN.md                 # Design tokens, dark mode, WCAG AA
├── SECURITY.md               # Threat model and invariants
├── VERIFICATION.md           # How each claim in this kit is checked
├── starter/
│   ├── app/                  # Application factory, blueprints, templates
│   ├── instance/             # SQLite database file (git-ignored)
│   ├── tests/                # Pytest suite
│   ├── requirements.txt      # Pinned dependencies
│   ├── Dockerfile            # Rootless image, UID 10001
│   └── docker-compose.yml
├── rules/source/             # Single-source rules, 5 modules
├── skills/                   # 5 agent skills
├── steps/agent-build-steps.md  # 6 verified build steps
├── evals/tasks/              # 3 benchmark tasks
└── security/
    ├── checks.json           # 12 OWASP-mapped controls
    ├── gitleaks.toml
    └── semgrep.yml
```

## 4. Quickstart

```bash
git clone https://github.com/Umar-444/Techtalks-stack-kits.git --depth 1
cd Techtalks-stack-kits/kits/flask-htmx-sqlite/starter

cp .env.example .env
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

flask --app app run --debug
```

Or with Docker:

```bash
docker compose up --build
```

## 5. Point an agent at it

The kit ships rules in eight agent dialects, all generated from
`rules/source/*.md` by `tools/transpiler.py`. Your agent will pick up whichever
applies automatically — `CLAUDE.md` for Claude Code, `.cursor/rules/*.mdc` for
Cursor, `CODEX.md` for Codex, `.clinerules` for Cline, and so on.

Then give it the bootstrap prompt from `kit.yaml`, or simply:

> Read `AGENTS.md`, `DESIGN.md`, and `steps/agent-build-steps.md`, then work
> through the build steps in order. Run the verification command after each
> step and do not continue until it passes.

## 6. Security posture

12 enforced controls spanning 6 OWASP Top 10:2025 categories — A02
Misconfiguration, A03 Supply Chain, A04 Cryptographic Failures, A05 Injection,
A06 Insecure Design, and A10 Mishandling of Exceptional Conditions.

Highlights specific to this stack:

- **CSRF tokens on every mutating HTMX request**, including `hx-post` and
  `hx-delete`, which bypass normal form submission.
- **Jinja autoescaping left on.** Partial responses are HTML fragments
  injected directly into the DOM, so an unescaped value is an XSS sink.
- **Parameterized SQLite queries only.** No f-string SQL anywhere.
- **Secret key read from the environment**, never committed.
- **Rootless container** running as UID 10001.

Full control list with evidence pointers: [`security/checks.json`](security/checks.json).
Threat model and rationale: [`SECURITY.md`](SECURITY.md).

```bash
python tools/audit_kit.py flask-htmx-sqlite      # 18-checkpoint verification
python tools/validate_checks.py --kit flask-htmx-sqlite
```

## 7. Skills

| Skill | Purpose |
|---|---|
| `install-and-verify` | Bootstrap the environment and confirm a green baseline |
| `first-feature` | Add an end-to-end feature across route, template, and test |
| `flask-htmx-sqlite-core` | Core conventions for the application factory |
| `htmx-csrf-and-security` | Wire CSRF through HTMX request headers correctly |
| `sqlite-wal-and-concurrency` | WAL pragmas, busy timeouts, transaction scope |

## 8. Benchmarks

```bash
python evals/runner.py --kit flask-htmx-sqlite
```

Three tasks cover the application factory health endpoint, HTMX partial render
and swap, and the SQLite WAL transaction guard.

## 9. Maintainer

Maintained by **Umar Farooq** — [itsumarfarooq.com](https://itsumarfarooq.com)
· [Propose a kit](https://techtalks.itsumarfarooq.com/kits/propose/)
· [Contribute](../../CONTRIBUTING.md)
