---
name: rate-limit-mitigation
description: Implementing token-bucket and sliding-window rate limiting to counter resource exhaustion.
---

# Rate Limit Mitigation Skill

## Overview
Protect APIs from brute-force attacks, scraping, and denial-of-service through sliding-window throttling.

## Implementation Pattern
```python
import time
from collections import defaultdict

RATE_LIMITS = defaultdict(list)
WINDOW_SECONDS = 60
MAX_REQUESTS = 30

def check_rate_limit(client_id: str):
    now = time.time()
    requests = [t for t in RATE_LIMITS[client_id] if now - t < WINDOW_SECONDS]
    if len(requests) >= MAX_REQUESTS:
        raise HTTPException(
            status_code=429,
            detail="API4:2023 - Rate limit exceeded. Please retry later.",
            headers={"Retry-After": "60"}
        )
    requests.append(now)
    RATE_LIMITS[client_id] = requests
```
