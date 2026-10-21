---
name: security-devsecops-ci-core
description: Scaffolding and execution skill for DevSecOps CI Pipeline (Gitleaks, Semgrep, CodeQL, Trivy, SBOM)
---

# DevSecOps CI Pipeline (Gitleaks, Semgrep, CodeQL, Trivy, SBOM) Core Skill

## Workflow
1. Initialize environment from `starter/`.
2. Inspect `DESIGN.md` for visual token specifications.
3. Apply single-source rules from `rules/source/`.
4. Validate build correctness using `evals/runner.py --kit security-devsecops-ci`.
