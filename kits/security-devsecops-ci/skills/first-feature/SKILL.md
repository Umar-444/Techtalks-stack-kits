---
name: first-feature
description: Guide for authoring and adding a new security guardrail or custom rule into the DevSecOps CI pipeline.
---

# First Feature Skill: Adding a Custom Security Guardrail

## Overview
Walkthrough for creating a new custom Semgrep security rule, configuring its SARIF output, testing it against positive and negative test cases, and integrating it into the CI pipeline.

## Step-by-Step Implementation

### 1. Define the Security Requirement
Target: Prevent dangerous shell command execution with shell=True in Python code.

### 2. Add Custom Semgrep Rule to `.semgrep.yml`
```yaml
rules:
  - id: python-subprocess-shell-true
    patterns:
      - pattern: subprocess.$FUNC(..., shell=True, ...)
    message: "Found subprocess call with shell=True. This introduces command injection risks."
    languages: [python]
    severity: ERROR
```

### 3. Create Unit Test Targets
In `starter/tests/test_target_vulnerable.py`:
```python
import subprocess
def unsafe_call(user_input):
    subprocess.run(f"echo {user_input}", shell=True)  # Should trigger rule
```

In `starter/tests/test_target_hardened.py`:
```python
import subprocess
def safe_call(user_input):
    subprocess.run(["echo", user_input], shell=False)  # Should pass
```

### 4. Execute Rule Verification
```bash
semgrep --config starter/.semgrep.yml starter/tests/
```
Verify that only the vulnerable pattern is flagged and exits with code 1.
