---
id: 05-testing-verification-and-ci
title: Testing Verification and CI Standards
description: Pest feature testing, architectural rules, and CI assertions.
globs: ["tests/**/*.php"]
alwaysApply: true
---

# Testing Verification and CI Standards

## 1. Feature Testing with Pest
- Test all Filament table rendering and form submission workflows.
- Assert that unauthorized users receive HTTP 403 Forbidden.
- Assert that MySQL full-text search returns exact matching records.

## 2. Architectural Invariants
- Assert that no `dd()`, `dump()`, or `var_dump()` calls exist in `app/`.
- Assert that all models use strict fillable properties.

## 3. CI Pipeline
- Every pull request must pass `php artisan test`, `gitleaks`, and `semgrep`.
