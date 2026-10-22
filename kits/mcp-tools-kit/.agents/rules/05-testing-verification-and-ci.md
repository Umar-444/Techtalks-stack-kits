# Testing Verification and CI Standards

# Testing Verification and CI Standards

## 1. Unit Testing Tools
- Test tool execution directly by invoking registered handler functions.
- Test that invalid payloads fail Zod validation with code `-32602`.
- Test that path traversal attempts throw `SecurityError`.

## 2. CI Pipeline
- Every PR must pass `npm test`, `npm run build`, `gitleaks`, and `semgrep`.
