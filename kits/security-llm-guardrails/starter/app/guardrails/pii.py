import re
from typing import Dict, Tuple

PII_PATTERNS = {
    "EMAIL": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
    "PHONE": re.compile(r"\b(?:\+?1[-. ]?)?\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})\b"),
    "SSN": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "CREDIT_CARD": re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b"),
    "SECRET_KEY": re.compile(r"\b(?:sk-[a-zA-Z0-9_-]{20,}|ghp_[a-zA-Z0-9]{36})\b"),
}

def anonymize_pii(text: str) -> Tuple[str, Dict[str, str]]:
    """
    Scans text for sensitive PII entities and replaces them with numbered placeholders.
    Returns (anonymized_text, deanonymize_mapping).
    """
    deanonymize_map: Dict[str, str] = {}
    anonymized = text
    counter = 1
    
    for entity_type, pattern in PII_PATTERNS.items():
        matches = list(pattern.finditer(anonymized))
        for match in reversed(matches):
            original_val = match.group(0)
            placeholder = f"<{entity_type}_{counter}>"
            deanonymize_map[placeholder] = original_val
            anonymized = anonymized[:match.start()] + placeholder + anonymized[match.end():]
            counter += 1
            
    return anonymized, deanonymize_map

def deanonymize_pii(text: str, deanonymize_map: Dict[str, str]) -> str:
    """Restores original PII values back into the model completion."""
    restored = text
    for placeholder, original in deanonymize_map.items():
        restored = restored.replace(placeholder, original)
    return restored
