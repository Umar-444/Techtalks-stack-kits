import time
from typing import Dict, List

# Approximate pricing per 1,000,000 tokens
COST_PER_MILLION_INPUT = 2.50
COST_PER_MILLION_OUTPUT = 10.00

class InMemoryRateLimiter:
    """Sliding window in-memory rate limiter with fallback support."""
    def __init__(self, max_per_minute: int = 60):
        self.max_per_minute = max_per_minute
        self.history: Dict[str, List[float]] = {}
        self.spend_usd: Dict[str, float] = {}

    def is_rate_limited(self, tenant_id: str) -> bool:
        now = time.time()
        window_start = now - 60.0
        
        # Clean expired timestamps
        timestamps = self.history.get(tenant_id, [])
        timestamps = [t for t in timestamps if t > window_start]
        self.history[tenant_id] = timestamps
        
        if len(timestamps) >= self.max_per_minute:
            return True
            
        self.history[tenant_id].append(now)
        return False

    def record_cost(self, tenant_id: str, prompt_tokens: int, completion_tokens: int) -> float:
        cost = (prompt_tokens * COST_PER_MILLION_INPUT + completion_tokens * COST_PER_MILLION_OUTPUT) / 1_000_000.0
        self.spend_usd[tenant_id] = self.spend_usd.get(tenant_id, 0.0) + cost
        return cost

    def get_monthly_spend(self, tenant_id: str) -> float:
        return self.spend_usd.get(tenant_id, 0.0)

rate_limiter = InMemoryRateLimiter()
