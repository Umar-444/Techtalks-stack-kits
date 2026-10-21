---
name: {{ SKILL_NAME }}
description: {{ SKILL_DESCRIPTION_TRIGGER }}
# The description above MUST act as an explicit trigger: define WHAT it does and WHEN an agent must use it.
# Example: "Scaffold and customize Filament administration resources with form schemas, table actions, and policy authorization."
version: 1.0.0
author: Umar Farooq (https://itsumarfarooq.com)
stack: {{ STACK_IDENTIFIER }}
---

# {{ SKILL_NAME }}

## Quick Summary & When to Use
Use this skill when you need to {{ PRIMARY_USE_CASE }}. Follow the progressive disclosure sections below:

1. **Pre-flight Prerequisites:** Verify installed packages and database migrations.
2. **Implementation Protocol:** Deterministic step-by-step instructions.
3. **Hardened Code Example:** Complete, runnable implementation.
4. **Verification Step:** Exact terminal command to verify correctness.

---

## 1. Pre-flight Checklist
- [ ] Required composer/npm packages installed.
- [ ] Database migration executed and schema verified.
- [ ] Relevant model and policy created.

---

## 2. Step-by-Step Implementation

### Step 1: Scaffold Base File
Run the scaffolding command:
```bash
{{ SCAFFOLD_COMMAND }}
```

### Step 2: Implement Component
Apply domain rules and authorization checks:
- Enforce strict typing on all properties and arguments.
- Apply granular Gate/Policy checks before data mutation.

---

## 3. Production Hardened Code Example

```{{ CODE_LANGUAGE }}
// Complete, runnable code example adhering to production standards
{{ HARDENED_CODE_SNIPPET }}
```

---

## 4. Verification Check
Run this exact verification command to confirm success:
```bash
{{ VERIFICATION_COMMAND }}
```

Expected output:
```text
{{ EXPECTED_OUTPUT }}
```
