---
name: pest-arch-test
description: Execute Pest Architectural tests verifying strict layering, UUID usage, and zero debugging calls.
---

# Pest Architecture Test Skill

## Purpose
Runs automated static architectural assertions against the codebase before commit.

## Execution
```bash
./vendor/bin/pest tests/ArchTest.php
```

## Standards Enforced
- Controllers never call `DB::` facade directly.
- All Eloquent models use `HasUuids`.
- Zero residual `dd()`, `dump()`, or `ray()` calls.

## Done Means
Pest architecture test suite executes and passes 100% of architectural rules with zero warnings.
