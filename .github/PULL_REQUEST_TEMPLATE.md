## Description
<!-- Brief summary of changes (e.g. Added Kit #2: Laravel + Livewire + PostgreSQL) -->

## Kit Checklist
- [ ] `kit.yaml` conforms to spec (`python tools/validate_manifest.py kits/<slug>/kit.yaml`)
- [ ] Single-source rules transpiled with zero drift (`python tools/transpiler.py --kit kits/<slug> --check`)
- [ ] All 6 agent formats present:
  - `AGENTS.md`
  - `CLAUDE.md`
  - `.cursor/rules/*.mdc`
  - `.github/copilot-instructions.md`
  - `.agents/rules/*.md`
  - `.windsurfrules`
- [ ] `DESIGN.md` includes color tokens, WCAG AA compliance, and dark mode standards
- [ ] `SECURITY.md` enforces authorization on every resource and parameterization
- [ ] `starter/` includes clean `Dockerfile`, `docker-compose.yml`, and `.env.example`
- [ ] `steps/agent-build-steps.md` verified with sequential commands
- [ ] Secret audit: Zero API keys, passwords, or private certificates committed

## Local Verification Output
```text
<!-- Paste output of: python tools/validate_manifest.py kits/<slug>/kit.yaml -->
```
