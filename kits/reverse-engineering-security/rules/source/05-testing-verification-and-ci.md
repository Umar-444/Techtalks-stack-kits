# Testing, Verification, and CI Security Standards

1. **Pytest Regression Test Suite**: Maintain a comprehensive test suite in `tests/test_audit.py` with synthetic test files containing known secure and insecure code patterns to ensure 100% detector accuracy and zero regressions.
2. **Zero False Positive Threshold**: Rigorously tune analyzer rules to avoid developer alert fatigue. Every reported finding must have a confidence rating (`HIGH`, `MEDIUM`, `LOW`) and actionable remediation steps.
3. **Automated CI Security Gating**: Integrate the security audit CLI into GitHub Actions and GitLab CI. Set non-zero exit codes on any `HIGH` severity finding to prevent merging vulnerable code.
4. **Supply Chain Hardening**: Lock all tool dependencies via pinned hashes in `requirements.txt`. Execute `gitleaks` and `pip-audit` during development to protect the audit suite itself.
5. **Transpiler Zero-Drift**: Validate that all 6 agent dialects match source rules using `python tools/transpiler.py --check` in continuous integration.
