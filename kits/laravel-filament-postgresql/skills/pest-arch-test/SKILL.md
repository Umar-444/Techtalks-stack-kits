---
name: "pest-arch-test"
description: "Write Pest architecture regression tests protecting against unescaped SQL and architectural drift."
version: "1.0.0"
author: "TechTalks Stack Kits"
---

# Pest Architecture Test Skill

Use this skill whenever adding architectural guardrails in `tests/ArchTest.php`.

## Workflow

1. **DB Facade Isolation:**
   ```php
   test('controllers do not call DB facade directly')
       ->expect('App\Http\Controllers')
       ->not->toUse('Illuminate\Support\Facades\DB');
   ```

2. **Strict Model Conventions:**
   ```php
   test('all models implement UUIDs')
       ->expect('App\Models')
       ->toUse('Illuminate\Database\Eloquent\Concerns\HasUuids');
   ```

3. **No Leftover Debugging:**
   ```php
   test('no debug calls remain')
       ->expect(['dd', 'dump', 'ray'])
       ->not->toBeUsed();
   ```
