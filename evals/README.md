# TechTalks Stack Kits — Evaluation Benchmark Engine

This evaluation framework tests AI coding assistants and kit configurations against reproducible, real-world tasks to measure:
1. **Rule Compliance Rate:** How well agents adhere to architectural invariants in `AGENTS.md`.
2. **Zero Rule Drift:** Verification that generated agent formats perfectly match `rules/source/*.md`.
3. **Secret Safety:** Absolute absence of plaintext tokens or credentials in source code.
4. **Dialect Integrity:** Native support across Cursor, Claude Code, Codex, Copilot, Antigravity, and Windsurf.

---

## Running Benchmarks Locally

```bash
# Run benchmark evaluation across all ready kits
python evals/runner.py
```

### Benchmark Tasks Catalog
- `evals/tasks/kit1_tasks.json`: Laravel 12/13 + Filament 4/3 + PostgreSQL
- `evals/tasks/kit2_tasks.json`: Laravel 12 + Livewire 4 + PostgreSQL
- `evals/tasks/kit3_tasks.json`: Laravel 12 + MongoDB (NoSQL)
- `evals/tasks/kit5_tasks.json`: Next.js 15+ + Supabase + shadcn/ui
