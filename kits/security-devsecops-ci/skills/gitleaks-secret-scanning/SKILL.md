---
name: gitleaks-secret-scanning
description: High-entropy string detection, API token regexes, and automated pre-commit secret scanning.
---

# Gitleaks Secret Scanning Skill

## Overview
Prevent API keys, private certificates, and authentication tokens from entering git history.

## Directives
1. **Local Pre-Commit Hook**:
   ```bash
   gitleaks protect --staged --verbose
   ```
2. **CI Historical Audit**:
   ```bash
   gitleaks detect --source . --report-path gitleaks-report.json --verbose
   ```
3. **Allowlisting**:
   Use `.gitleaksignore` with fingerprint hashes rather than broad regex exclusions.
