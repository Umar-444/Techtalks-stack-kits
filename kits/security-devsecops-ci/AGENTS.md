# DevSecOps CI Pipeline (Gitleaks + Semgrep + Trivy + GitHub Actions) — Agent Operating Rules (AGENTS.md)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Table of Contents
- [Architectural Standards for DevSecOps CI Pipeline (Gitleaks, Semgrep, CodeQL, Trivy, SBOM)](#architecture-guidelines)
- [DevSecOps CI Pipeline Architecture and Gating Standards](#01-pipeline-architecture-and-standards)
- [Secret Detection, Entropy Scanning, and Gitleaks Invariants](#02-secret-detection-and-gitleaks)
- [Security Invariants for DevSecOps CI Pipeline (Gitleaks, Semgrep, CodeQL, Trivy, SBOM)](#security-invariants)
- [Agent Coding Conventions for DevSecOps CI Pipeline (Gitleaks, Semgrep, CodeQL, Trivy, SBOM)](#agent-coding-conventions)
- [Static Application Security Testing (SAST) and Custom Semgrep Rules](#03-sast-and-semgrep-rules)
- [Container Hardening, CVE Scanning, and Trivy Invariants](#04-container-scanning-and-trivy)
- [Supply Chain Security, SBOM Generation, and Cosign Verification](#05-supply-chain-sbom-cosign)

---

<a id="architecture-guidelines"></a>
## Architectural Standards for DevSecOps CI Pipeline (Gitleaks, Semgrep, CodeQL, Trivy, SBOM)

# Architecture Standards: DevSecOps CI Pipeline (Gitleaks, Semgrep, CodeQL, Trivy, SBOM)
- Strictly adhere to modular component separation.
- Keep dependency surface minimal and auditable.
- Prefer explicit configuration over magic implicit defaults.

---

<a id="01-pipeline-architecture-and-standards"></a>
## DevSecOps CI Pipeline Architecture and Gating Standards

# DevSecOps CI Pipeline Architecture and Gating Standards

## 1. Pipeline Stages & Execution Flow
- Security pipelines execute across four synchronized stages:
  1. **Pre-Flight Secret Audit**: Detect plaintext credentials and tokens before running build steps (`gitleaks`).
  2. **Static Application Security Testing (SAST)**: AST-based vulnerability analysis with zero compiler dependence (`semgrep`).
  3. **Software Composition Analysis (SCA) & Container Scanning**: Filesystem package and base image CVE audits (`trivy`).
  4. **Supply Chain & Provenance**: Software Bill of Materials generation (`syft`) and cryptographic image signing (`cosign`).

## 2. Gating & Severity Thresholds
- **Blocking Gates (Exit Code 1)**: Any `CRITICAL` or `HIGH` severity finding with a known fix halts pull request merges.
- **Advisory Warnings**: Medium and low findings are logged as annotations in the GitHub Security tab without blocking developer velocity.
- Suppressions must be temporary and documented with expiration timestamps in `.trivyignore` or `.gitleaksignore`.

## 3. SARIF Standardization
- All scanners must emit Static Analysis Results Interchange Format (`SARIF 2.1.0`) reports.
- Upload reports to `github/codeql-action/upload-sarif` to centralize triaging directly within repository security dashboards.

---

<a id="02-secret-detection-and-gitleaks"></a>
## Secret Detection, Entropy Scanning, and Gitleaks Invariants

# Secret Detection, Entropy Scanning, and Gitleaks Invariants

## 1. Zero Plaintext Credentials
- No private keys, JWT secrets, database connection strings, cloud API keys, or Webhook tokens may be committed to version control.
- All secrets must be sourced from runtime secret managers (AWS Secrets Manager, HashiCorp Vault, GitHub Encrypted Secrets).

## 2. Gitleaks Configuration
- Maintain customized rules in `.gitleaks.toml`:
  ```toml
  [extend]
  useDefault = true

  [[rules]]
  id = "custom-jwt-secret"
  description = "Detected Hardcoded JWT Secret Key"
  regex = '''(?i)(jwt[_-]?secret|token[_-]?secret)\s*[:=]\s*["']([A-Za-z0-9_\-]{24,})["']'''
  keywords = ["jwt_secret", "token_secret"]
  ```
- Run full historical scans on pull requests using `--log-opts="--all"`.

## 3. Leaked Secret Remediation Protocol
- If a secret is committed:
  1. Revoke and rotate the compromised credential immediately.
  2. Invalidate active sessions tied to the secret.
  3. Purge the git commit history using `git-filter-repo` or BFG Repo-Cleaner.
  4. Never merely commit a "delete secret" patch—historical commits remain compromised.

---

<a id="security-invariants"></a>
## Security Invariants for DevSecOps CI Pipeline (Gitleaks, Semgrep, CodeQL, Trivy, SBOM)

# Security Invariants
- Verify tenant boundary before reading or writing any persistent state.
- Sanitize all external inputs using validated schemas.
- Reject requests with missing or expired bearer tokens.

---

<a id="agent-coding-conventions"></a>
## Agent Coding Conventions for DevSecOps CI Pipeline (Gitleaks, Semgrep, CodeQL, Trivy, SBOM)

# Agent Coding Conventions
- Maintain clean, minimal code changes with zero extraneous comments.
- Run typecheck and compile verification after every file modification.
- Never introduce undocumented third-party libraries without explicit instructions.

---

<a id="03-sast-and-semgrep-rules"></a>
## Static Application Security Testing (SAST) and Custom Semgrep Rules

# Static Application Security Testing (SAST) and Custom Semgrep Rules

## 1. AST Analysis over Regex
- Use Semgrep AST semantic pattern matching rather than brittle string regex:
  ```yaml
  rules:
    - id: unescaped-sql-query
      patterns:
        - pattern: "$DB.execute($QUERY)"
        - pattern-inside: |
            $QUERY = ... + ...
            ...
      message: "Detected potential SQL injection via string concatenation into database query."
      languages: [python, javascript]
      severity: ERROR
  ```

## 2. Taint Mode Tracking
- Trace unvalidated user input sources (`request.args`, `params[]`) into dangerous execution sinks (`exec`, `system`, SQL queries).
- Enforce sanitizers or type casting before data reaches external sinks.

## 3. False Positive Mitigation
- When an alert is an intentional, hardened pattern, use inline suppression:
  `# nosemgrep: custom-rule-id -- Reason: Input validated by upstream middleware`
- Review all inline suppressions periodically during security retrospectives.

---

<a id="04-container-scanning-and-trivy"></a>
## Container Hardening, CVE Scanning, and Trivy Invariants

# Container Hardening, CVE Scanning, and Trivy Invariants

## 1. Minimal Attack Surface Base Images
- Standardize on minimal Alpine (`alpine:3.20`) or Google Distroless base images.
- Prohibit generic `:latest` tags; pin explicit patch versions with SHA256 digests:
  `FROM alpine:3.20.3@sha256:beefdbd8a1da6d2915566fde36db9db0b524eb737fc57cd13675d29e64fc613b`

## 2. Non-Root Execution
- Containers must never execute as `root`.
- Always create a dedicated unprivileged user and group in the Dockerfile:
  ```dockerfile
  RUN addgroup -S appgroup && adduser -S appuser -G appgroup
  USER appuser
  ```

## 3. Trivy Scanning Discipline
- Scan both filesystem dependencies and built container images:
  ```bash
  trivy image --exit-code 1 --severity CRITICAL,HIGH --ignore-unfixed my-app:latest
  ```
- Suppress unfixed vulnerabilities lacking upstream vendor patches (`--ignore-unfixed`).

---

<a id="05-supply-chain-sbom-cosign"></a>
## Supply Chain Security, SBOM Generation, and Cosign Verification

# Supply Chain Security, SBOM Generation, and Cosign Verification

## 1. Software Bill of Materials (SBOM) Generation
- Automatically generate machine-readable SBOMs for every production release using Anchore Syft:
  ```bash
  syft packages dir:. -o cyclonedx-json=cyclonedx.json -o spdx-json=spdx.json
  ```
- Archive SBOM artifacts alongside container images for regulatory and audit compliance.

## 2. Container Signing with Sigstore Cosign
- Sign container images in GitHub Actions using keyless OIDC identity:
  ```bash
  cosign sign --yes "${IMAGE_NAME}@${IMAGE_DIGEST}"
  ```
- Enforce signature verification before deploying images to Kubernetes or production runtimes.

## 3. Automated Dependency Updates
- Maintain `.github/dependabot.yml` configured for weekly security version bump PRs with automated testing.

---

