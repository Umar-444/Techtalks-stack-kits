---
name: first-feature
description: Guide to adding a custom guardrail rule, domain-specific classifier, or policy filter to the AI Gateway pipeline.
---
# First Feature Skill: Adding a Custom Guardrail Policy to the Gateway

## 1. Define the Custom Policy Checker
Create a new filter in `app/guardrails/competitor.py` to prevent data leakage regarding unreleased products or competitor endorsements:
```python
import re
from typing import Tuple

BLOCKED_COMPETITORS = ["AcmeCorpInternal", "SecretProjectX", "ProjectTitan"]

def check_confidential_terms(text: str) -> Tuple[bool, str]:
    """Check text for confidential internal code words."""
    for term in BLOCKED_COMPETITORS:
        if re.search(r"\b" + re.escape(term) + r"\b", text, re.IGNORECASE):
            return False, f"Confidential keyword detected: {term}"
    return True, ""
```

## 2. Register into the Gateway Pipeline
In `app/main.py`, hook the policy filter before dispatching to upstream LLMs:
```python
from app.guardrails.competitor import check_confidential_terms

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    # 1. Check prompt injection
    # 2. Check PII
    
    # 3. Custom Confidential Policy
    passed, reason = check_confidential_terms(request.user_prompt)
    if not passed:
        raise HTTPException(
            status_code=400,
            detail={"error": "PolicyViolation", "message": reason}
        )
        
    # Forward to upstream LLM...
```

## 3. Write Unit Test Assertions
In `tests/test_gateway.py`:
```python
def test_confidential_keyword_blocked(client):
    res = client.post("/v1/chat/completions", json={
        "messages": [{"role": "user", "content": "Tell me about SecretProjectX architecture"}]
    })
    assert res.status_code == 400
    assert "Confidential keyword detected" in res.json()["detail"]["message"]
```
