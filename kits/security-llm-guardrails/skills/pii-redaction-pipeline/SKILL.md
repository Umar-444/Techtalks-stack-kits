---
name: pii-redaction-pipeline
description: Configuring automated PII redaction, reversible tokenization mapping, and custom entity recognizers.
---
# PII Redaction Pipeline Skill

## 1. Automated Detection and Redaction
Detect sensitive personal identifiers and mask them before prompting third-party foundation models:
```python
import re
from typing import Dict, Tuple

PII_PATTERNS = {
    "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    "PHONE": r"\b(?:\+?1[-. ]?)?\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})\b",
    "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
    "CREDIT_CARD": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
    "API_KEY": r"\b(?:sk-[a-zA-Z0-9_-]{20,}|ghp_[a-zA-Z0-9]{36})\b",
}

def redact_pii(text: str) -> Tuple[str, Dict[str, str]]:
    """Redact PII with reversible placeholder tokens."""
    deanonymize_map = {}
    counter = 1
    
    anonymized = text
    for entity_type, pattern in PII_PATTERNS.items():
        matches = list(re.finditer(pattern, anonymized))
        # Replace in reverse order to preserve string offsets
        for match in reversed(matches):
            original_val = match.group(0)
            placeholder = f"<{entity_type}_{counter}>"
            deanonymize_map[placeholder] = original_val
            anonymized = anonymized[:match.start()] + placeholder + anonymized[match.end():]
            counter += 1
            
    return anonymized, deanonymize_map

def restore_pii(response_text: str, deanonymize_map: Dict[str, str]) -> str:
    """Restore original entities back into the LLM output."""
    restored = response_text
    for placeholder, original in deanonymize_map.items():
        restored = restored.replace(placeholder, original)
    return restored
```

## 2. Presidio NLP Custom Recognizer
To add enterprise-specific entities (e.g. Employee ID or Medical Record Number):
```python
from presidio_analyzer import PatternRecognizer, Pattern

emp_id_pattern = Pattern(name="emp_id_pattern", regex=r"\bEMP-[0-9]{6}\b", score=0.85)
emp_recognizer = PatternRecognizer(supported_entity="EMPLOYEE_ID", patterns=[emp_id_pattern])
analyzer.registry.add_recognizer(emp_recognizer)
```
