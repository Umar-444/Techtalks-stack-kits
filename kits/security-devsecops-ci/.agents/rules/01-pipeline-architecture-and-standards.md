# DevSecOps CI Pipeline Architecture and Gating Standards

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
