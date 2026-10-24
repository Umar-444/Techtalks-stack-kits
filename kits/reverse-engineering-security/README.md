# Reverse Engineering & Security Audit Pack

> **TechTalks Stack Kits — Security line**
> **Efficiency Tier:** `A` · **Median tokens to reference build:** `20,998`

A defensive security auditing suite. It analyses artifacts you already own —
your source tree, your compiled binaries, your dependency manifest — and
reports what it finds as SARIF that GitHub Code Scanning can ingest.

This kit builds **analysis tooling**, not exploits. Every component inspects a
build output and reports on it; none of them attack a running system.

## 1. What it does

Three independent analysers behind one CLI:

**Python AST static analysis.** Walks the abstract syntax tree looking for
dangerous dynamic-execution sinks — `eval`, `exec`, `pickle.loads`,
`subprocess` with `shell=True`, `yaml.load` without a safe loader. Working on
the AST rather than regex means `# eval(` in a comment is not a finding, and
`getattr(builtins, "ev" + "al")` still is.

**Binary exploit-mitigation verification.** Parses ELF and PE structural
headers to confirm the mitigations the toolchain was supposed to apply are
actually present in the shipped artifact: NX/DEP, PIE/ASLR, stack canaries,
and RELRO. A release build with mitigations silently disabled is a common and
near-invisible regression.

**Supply chain and SBOM validation.** Generates and validates CycloneDX and
SPDX bills of material, then correlates components against known CVE
advisories.

Findings from all three normalise into **OASIS SARIF 2.1.0**, so they surface
in the GitHub Security tab alongside first-party scanners instead of living in
CI logs nobody reads.

## 2. Stack

| Layer | Component | Version |
|---|---|---|
| Language | Python | `>= 3.12` |
| Interface | Security Audit CLI | `^1.0` |
| AST analysis | Python standard-library `ast` visitor engine | stdlib |
| Binary analysis | ELF/PE structural mitigation checker | bundled |
| Reporting | OASIS SARIF | `2.1.0` |

Using the standard library's `ast` module rather than a third-party parser
keeps the dependency surface minimal — appropriate for a tool whose job is
auditing dependency surfaces.

## 3. Layout

```text
kits/reverse-engineering-security/
├── kit.yaml                  # Machine-readable manifest
├── README.md                 # This guide
├── DESIGN.md                 # CLI output design, severity colouring
├── SECURITY.md               # Threat model and tool-safety invariants
├── VERIFICATION.md           # How each claim in this kit is checked
├── starter/
│   ├── cli.py                # Command-line entry point
│   ├── audit.py              # Orchestrates analysers, aggregates findings
│   ├── analyzers/            # AST, binary, and SBOM analysers
│   ├── reporting/            # SARIF 2.1.0 serialisation
│   ├── tests/                # Pytest suite with fixture binaries
│   ├── requirements.txt
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
cd Techtalks-stack-kits/kits/reverse-engineering-security/starter

cp .env.example .env
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python cli.py --help
python cli.py scan ../../../kits --format sarif --out findings.sarif
```

Or with Docker:

```bash
docker compose up --build
```

## 5. Wiring it into CI

SARIF output is the point — it turns findings into reviewable GitHub alerts:

```yaml
- name: Run security audit
  run: python starter/cli.py scan . --format sarif --out findings.sarif

- name: Upload to GitHub Code Scanning
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: findings.sarif
```

Gate the build with a non-zero exit on HIGH severity so a regression blocks the
merge rather than generating a notification.

## 6. Point an agent at it

Rules ship in eight agent dialects, all generated from `rules/source/*.md` by
`tools/transpiler.py`. Your agent picks up whichever applies — `CLAUDE.md`,
`CODEX.md`, `.cursor/rules/*.mdc`, `.clinerules`, and the rest.

> Read `AGENTS.md` and `steps/agent-build-steps.md`, then work through the
> build steps in order. Run the verification command after each step and do
> not continue until it passes.

## 7. Security posture

12 enforced controls spanning 5 OWASP Top 10:2025 categories — A02
Misconfiguration, A03 Supply Chain Failures, A04 Cryptographic Failures, A05
Injection, and A09 Security Logging & Alerting Failures.

A tool that parses untrusted binaries is itself an attack surface, so this kit
holds a stricter line than most:

- **Analysers never execute what they inspect.** Binaries are parsed
  structurally; sample code is walked as an AST. Nothing is imported or run.
- **Rootless container** running as UID 10001, with no network egress required
  for a scan.
- **Findings are sanitised before serialisation** so a crafted filename or
  symbol cannot inject content into the SARIF report.

Full control list with evidence pointers: [`security/checks.json`](security/checks.json).
Threat model and rationale: [`SECURITY.md`](SECURITY.md).

```bash
python tools/audit_kit.py reverse-engineering-security
python tools/validate_checks.py --kit reverse-engineering-security
```

## 8. Skills

| Skill | Purpose |
|---|---|
| `install-and-verify` | Bootstrap the environment and confirm a green baseline |
| `first-feature` | Add an analyser end to end, with fixtures and tests |
| `reverse-engineering-security-core` | Core CLI and aggregation conventions |
| `ast-security-rule-authoring` | Write a new AST sink-detection rule |
| `binary-mitigation-auditing` | Extend ELF/PE mitigation verification |

## 9. Benchmarks

```bash
python evals/runner.py --kit reverse-engineering-security
```

Three tasks cover AST dangerous-sink detection, binary hardening checks, and
SARIF report export.

## 10. Scope and intended use

This kit is for auditing software **you are authorised to audit** — your own
projects, your employer's codebase, or a target covered by an engagement. The
analysers are read-only and non-exploitative by design.

## 11. Maintainer

Maintained by **Umar Farooq** — [itsumarfarooq.com](https://itsumarfarooq.com)
· [Propose a kit](https://techtalks.itsumarfarooq.com/kits/propose/)
· [Contribute](../../CONTRIBUTING.md)
