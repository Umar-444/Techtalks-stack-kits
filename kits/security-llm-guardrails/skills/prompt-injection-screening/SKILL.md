---
name: prompt-injection-screening
description: Implementing heuristic pattern detection, system prompt delimiter sandboxing, and canary token leakage guards.
---
# Prompt Injection & Jailbreak Screening Skill

## 1. High-Performance Heuristic Screening
Inspect user inputs for known jailbreak patterns before any model invocation:
```python
import re

JAILBREAK_PATTERNS = [
    r"(?i)\bignore\s+(all\s+)?(previous|prior)\s+(instructions|directives|prompts)\b",
    r"(?i)\byou\s+are\s+now\s+(in\s+)?(DAN|developer|unrestricted|jailbreak)\s+mode\b",
    r"(?i)\bsystem\s+override\s+code\b",
    r"(?i)\bpretend\s+you\s+have\s+no\s+(rules|limits|safety|filters)\b",
    r"(?i)\boutput\s+the\s+(entire\s+)?(system\s+prompt|initial\s+instructions)\b",
    r"(?i)\bbegin\s+your\s+response\s+with\s*:\s*\"?sure,\s*i\s+can\s+help\b",
]

def detect_prompt_injection(prompt: str) -> bool:
    for pattern in JAILBREAK_PATTERNS:
        if re.search(pattern, prompt):
            return True
    return False
```

## 2. Delimiter Sandboxing & XML Boundary Wrapping
Wrap user inputs in dynamic XML tags so the LLM treats input as inert data rather than active instructions:
```python
def sandbox_input(user_input: str) -> str:
    # Escape internal matching tags to prevent XML injection
    cleaned = user_input.replace("<user_input>", "&lt;user_input&gt;").replace("</user_input>", "&lt;/user_input&gt;")
    return f"<user_input>\n{cleaned}\n</user_input>"
```

## 3. Canary Token Verification
Embed a secret token into the system prompt and verify the completion does not leak it:
```python
import secrets

def generate_canary() -> str:
    return f"CANARY_{secrets.token_hex(8)}"

def verify_canary_leak(response_text: str, canary: str) -> bool:
    """Returns True if the response contains the secret canary token (leak detected)."""
    return canary in response_text
```
