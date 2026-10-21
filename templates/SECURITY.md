# SECURITY.md — {{ KIT_NAME }} Security Policy & Standards
# Reference: 06-Security-Standard.md & 09-Agent-Master-Brief.md

Security is an integrated baseline layer in every TechTalks Stack Kit, never an opt-in afterthought.

## 1. Security Invariants (Non-Negotiable)

1. **Zero Hardcoded Credentials:**
   No passwords, API tokens, encryption keys, or private certificates exist in this repository. All environment variables must be declared in `.env.example` with empty or mock values.

2. **Strict Query Parameterization:**
   Raw SQL string concatenation is strictly prohibited. All queries must use PDO bindings or ORM parameterization.

3. **Mandatory Authorization Gates:**
   Every controller endpoint, API route, and administrative action must verify user permissions via explicit Policy or Gate checks.

4. **Prompt Injection Boundary Protection:**
   When invoking external LLM models, untrusted input must be isolated with randomized cryptographic boundary nonces.

5. **Agent Rules Backdoor Prevention:**
   All rules files (`AGENTS.md`, `CLAUDE.md`, `.cursor/rules/`) are audited against prompt-injection overrides or unauthorized agent execution commands.

---

## 2. Automated Security Scans

Every kit is verified with the following automated pipeline:

### A. Secret Scanning (Gitleaks)
```bash
gitleaks detect --source . --verbose
```

### B. Static Application Security Testing (Semgrep)
```bash
semgrep scan --config auto --error
```

### C. Dependency Auditing
```bash
{{ DEPENDENCY_AUDIT_COMMAND }}
# e.g., composer audit --locked OR npm audit --audit-level=high
```

---

## 3. Reporting a Vulnerability

If you discover a security issue or vulnerability within this stack kit, please do NOT file a public issue.
Report it directly to Umar Farooq at:
- **Email:** [contact@itsumarfarooq.com](mailto:contact@itsumarfarooq.com)
- **Security SLA:** Acknowledgement within 24 hours, patch released within 48 hours.
