# Assistant Guidelines for DevSecOps CI/CD Stack Kit

## Stack Overview
- Pipeline Engine: GitHub Actions v4
- Secret Scanner: Gitleaks 8+
- SAST Scanner: Semgrep OSS (OWASP Top 10 + Custom Rules)
- Container & Vulnerability Scanner: Aqua Security Trivy
- SBOM Generator: Anchore Syft (SPDX 2.3 & CycloneDX 1.5)
- Image Signing: Sigstore Cosign (SLSA Provenance)
- Local Runner: Cross-platform Python/Bash local security pipeline

## Mandatory Rules
1. Zero plaintext secrets in code or git history. Enforce Gitleaks pre-commit and in CI.
2. SAST rules in `.semgrep.yml` must use AST pattern matching. Prohibit raw regex for code analysis.
3. Containers must execute under unprivileged non-root users and pin immutable image digests.
4. Block CI merges on CRITICAL and HIGH severity CVEs with available upstream patches.
5. All security tools must emit SARIF 2.1.0 formatted reports for GitHub Code Scanning integration.
