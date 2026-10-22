---
name: brakeman-security-audit
description: Static code analysis, vulnerability mitigation, and security compliance with Brakeman.
---

# Brakeman Security Audit Skill

## Overview
Enforce automated security compliance across Rails controllers, models, and views using Brakeman.

## Execution
```bash
bundle exec brakeman --no-pager --exit-on-warn --exit-on-error
```

## Critical Checks
1. **SQL Injection (SQLi)**: Prohibit string interpolation in `.where()`, `.order()`, `.select()`.
2. **Mass Assignment**: Prohibit `.permit!` on user input.
3. **Cross-Site Scripting (XSS)**: Prohibit unescaped `raw()` or `html_safe` on user-supplied strings.
4. **Remote Code Execution**: Prohibit `eval`, `send` with dynamic symbols, or unvalidated `constantize`.
5. **Session Hijacking**: Verify cookie session configuration specifies `SameSite=Lax` and `Secure=true`.
