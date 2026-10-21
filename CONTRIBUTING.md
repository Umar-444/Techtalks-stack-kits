# Contributing to TechTalks Stack Kits

Thank you for your interest in contributing to **TechTalks Stack Kits**! Our mission is to provide developers and AI agents with tested, reproducible, production-grade project foundations that eliminate rule drift and configuration hallucination.

- **Repository:** [github.com/Umar-444/Techtalks-stack-kits](https://github.com/Umar-444/Techtalks-stack-kits)
- **Web Catalog:** [techtalks.itsumarfarooq.com/kits/](https://techtalks.itsumarfarooq.com/kits/)
- **License:** MIT

---

## 1. Ground Rules & Platform Standards

Before submitting a kit or modifying existing code, ensure your contribution meets our platform invariants:

1. **Accuracy & Real Versions:**
   - Use only verified, current versions from official registries (Packagist, npm, PyPI).
   - Never invent configuration keys, methods, or framework APIs.
   - If a version is unverified, verify it against official documentation first.

2. **Zero Invented Metrics:**
   - Do not claim unverified benchmarks, fake star counts, or marketing claims.
   - Plain, direct, technical documentation only.

3. **Non-Negotiable Security:**
   - Never commit real credentials, passwords, or private keys.
   - Every kit must include a `SECURITY.md` defining authorization on every resource, parameterized SQL, and secret scanning.

4. **Single Source of Truth for Rules:**
   - Agent rules are written **once** in `rules/source/*.md`.
   - Never manually edit generated dialect files (`AGENTS.md`, `CLAUDE.md`, `.cursor/rules/*.mdc`, `.github/copilot-instructions.md`, `.agents/rules/*.md`, `.windsurfrules`).
   - Run `python tools/transpiler.py --kit kits/<slug>` to generate dialects.

---

## 2. Anatomy of a Stack Kit

Every kit inside `kits/<slug>/` must adhere to the 6-layer architecture:

```text
kits/<slug>/
├── kit.yaml                     # Machine-readable manifest (validated via tools/validate_manifest.py)
├── README.md                    # Quickstart, stack summary, agent kickoff prompt
├── DESIGN.md                    # Design tokens, typography, dark mode, component standards
├── SECURITY.md                  # Non-negotiable security controls and threat model
├── starter/                     # Working skeleton (Dockerfile, docker-compose.yml, .env.example)
├── rules/
│   └── source/                  # Numbered Markdown source rules (01-*.md, 02-*.md...)
├── skills/                      # Reusable SKILL.md agent workflows (Anthropics spec)
│   └── <skill-name>/SKILL.md
└── steps/
    └── agent-build-steps.md     # Linear, step-by-step agent prompts with verification commands
```

---

## 3. Contribution Workflow

### Step 1: Open an Issue or Choose a Blueprint
Before writing a full kit, open a **New Kit Proposal** issue or pick an issue labeled `good first issue` from our [Starter Issues](docs/starter-issues.md).

### Step 2: Scaffold Your Kit
Use our starter template:
```bash
cp -r templates kits/<your-kit-slug>
```

### Step 3: Populate and Validate Manifest
Edit `kits/<your-kit-slug>/kit.yaml` and validate it:
```bash
python tools/validate_manifest.py kits/<your-kit-slug>/kit.yaml
```

### Step 4: Write Rules and Transpile Dialects
Write your topic-focused rules in `kits/<your-kit-slug>/rules/source/`:
```bash
python tools/transpiler.py --kit kits/<your-kit-slug>
python tools/transpiler.py --kit kits/<your-kit-slug> --check
```

### Step 5: Test Starter & Security
1. Verify Docker Compose runs cleanly.
2. Verify `.env.example` has zero real secrets.
3. Verify all primary keys and model policies conform to your stack's standards.

### Step 6: Regenerate Web Pages & Submit PR
```bash
python tools/build_kit_pages.py
git checkout -b feature/kit-<slug>
git commit -m "feat(kits): add <slug> stack kit"
git push origin feature/kit-<slug>
```

---

## 4. Code of Conduct

We are committed to providing a welcoming, constructive, and inclusive environment. Please communicate professionally in all issues and pull requests.
