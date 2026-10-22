---
id: 05-testing-verification-and-ci
title: Testing Verification and CI Standards
description: Vitest unit testing, action integration tests, and CI checks.
globs: ["tests/**/*.ts"]
alwaysApply: true
---

# Testing Verification and CI Standards

## 1. Test Suite Coverage
- Test Zod validation schemas against both valid and adversarial payloads.
- Test Server Actions with mock Prisma clients or test database containers.
- Assert that cross-tenant mutations are rejected.

## 2. CI Verification
- Every PR must pass `npm run build`, `npm test`, `gitleaks`, and `semgrep`.
