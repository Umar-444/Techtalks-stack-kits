import re
import secrets
import uuid
from typing import Tuple, List

JAILBREAK_PATTERNS: List[re.Pattern] = [
    re.compile(r"\bignore\s+(all\s+)?(previous|prior)\s+(instructions|directives|prompts)\b", re.IGNORECASE),
    re.compile(r"\byou\s+are\s+now\s+(in\s+)?(dan|developer|unrestricted|jailbreak)\s+mode\b", re.IGNORECASE),
    re.compile(r"\bsystem\s+override\s+code\b", re.IGNORECASE),
    re.compile(r"\bpretend\s+you\s+have\s+no\s+(rules|limits|safety|filters)\b", re.IGNORECASE),
    re.compile(r"\boutput\s+the\s+(entire\s+)?(system\s+prompt|initial\s+instructions)\b", re.IGNORECASE),
    re.compile(r"\bprint\s+your\s+instructions\s+above\b", re.IGNORECASE),
    re.compile(r"\bbase64\s*:\s*[A-Za-z0-9+/=]{40,}", re.IGNORECASE),
]

def detect_prompt_injection(prompt: str) -> Tuple[bool, str]:
    """
    Fast-path deterministic screening for prompt injection and jailbreak signatures.
    Returns (True, '') if safe, or (False, reason) if blocked.
    """
    for pattern in JAILBREAK_PATTERNS:
        match = pattern.search(prompt)
        if match:
            return False, f"Prompt injection signature detected: {match.group(0)}"
    return True, ""

def sandbox_user_input(user_input: str) -> Tuple[str, str]:
    """
    Enclose untrusted user input within a cryptographically isolated XML tag.
    Returns (sandboxed_text, boundary_tag).
    """
    tag_id = uuid.uuid4().hex[:8]
    open_tag = f"<user_input_{tag_id}>"
    close_tag = f"</user_input_{tag_id}>"
    # Escape matching boundary tags inside user input
    cleaned = user_input.replace(open_tag, f"&lt;user_input_{tag_id}&gt;").replace(close_tag, f"&lt;/user_input_{tag_id}&gt;")
    return f"{open_tag}\n{cleaned}\n{close_tag}", tag_id

def generate_canary_token() -> str:
    """Generate a secret canary token to verify system prompt confidentiality."""
    return f"CANARY_{secrets.token_hex(8)}"

def detect_canary_leak(response_text: str, canary_token: str) -> bool:
    """Returns True if the response contains the secret canary token."""
    return canary_token in response_text
