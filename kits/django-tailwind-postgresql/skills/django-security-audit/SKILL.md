---
name: django-security-audit
description: Harden Django production configuration, verify CSP headers, and execute automated security audits.
---

# Django Security Audit Skill

## Purpose
Automates security checklist audits and runs production deployment checks before release.

## Verification Checklist
1. **Run Django Security Check**:
   ```bash
   python manage.py check --deploy
   ```
2. **Verify Security Headers in settings.py**:
   - `SECURE_SSL_REDIRECT = True` (in production)
   - `SESSION_COOKIE_SECURE = True`
   - `CSRF_COOKIE_SECURE = True`
   - `SECURE_BROWSER_XSS_FILTER = True`
   - `SECURE_CONTENT_TYPE_NOSNIFF = True`
   - `X_FRAME_OPTIONS = 'DENY'`
3. **Run Automated Test Suite**:
   ```bash
   pytest
   ```
