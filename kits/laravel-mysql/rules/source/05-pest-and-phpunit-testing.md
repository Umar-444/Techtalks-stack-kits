---
id: 05-pest-and-phpunit-testing
title: Pest & PHPUnit Testing with MySQL Database Transactions
globs: "starter/tests/**/*.php"
alwaysApply: true
---

# Pest & PHPUnit Testing with MySQL Database Transactions

## 1. Test Isolation with RefreshDatabase
- Test classes must use `Illuminate\Foundation\Testing\RefreshDatabase`.
- Enforces database transactions rolling back after each test case, preserving database cleanliness.

## 2. Feature & Policy Authorization Assertions
- Verify authorization policies by testing unauthorized users receive HTTP 403 Forbidden.
- Assert validation errors return HTTP 422 Unprocessable Entity with named error keys.

## 3. Live Health & Smoke Verification
- Maintain automated smoke tests asserting `/healthz` returns HTTP 200 OK with valid JSON structure.
