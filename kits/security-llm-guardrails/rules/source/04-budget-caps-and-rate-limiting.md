---
id: budget-caps-and-rate-limiting
title: Budget Caps & Rate Limiting
globs: "**/*.py"
alwaysApply: true
---
# Token Bucket Rate Limiting, Dollar Quotas & DoW Mitigation

## 1. Denial of Wallet (DoW) Defenses
- LLM endpoints are financially vulnerable to Denial of Wallet attacks where adversaries generate runaway token costs.
- The gateway must enforce:
  1. **Maximum Input Tokens**: Hard cap input prompt size (e.g., maximum 8,192 tokens or 32,000 characters) before forwarding to LLM.
  2. **Maximum Output Tokens**: Request must set explicit `max_tokens` (default 2,048) preventing endless generation loops.
  3. **Daily / Monthly Dollar Quota**: Track accumulated USD costs per tenant using pricing calculators:
     ```python
     COST_PER_MILLION_INPUT = 2.50   # e.g., GPT-4o
     COST_PER_MILLION_OUTPUT = 10.00
     cost = (prompt_tokens * COST_PER_MILLION_INPUT + completion_tokens * COST_PER_MILLION_OUTPUT) / 1_000_000
     ```

## 2. Sliding Window Rate Limiting with Redis
- Enforce token bucket rate limiting per client API key using Redis sorted sets:
  ```python
  current_time = time.time()
  pipeline = redis_client.pipeline()
  pipeline.zremrangebyscore(rate_limit_key, 0, current_time - 60)
  pipeline.zcard(rate_limit_key)
  pipeline.zadd(rate_limit_key, {str(uuid.uuid4()): current_time})
  pipeline.expire(rate_limit_key, 60)
  _, request_count, _, _ = await pipeline.execute()
  if request_count > MAX_REQUESTS_PER_MINUTE:
      raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again in 60s.")
  ```

## 3. Quota Exceeded Behavior
- When a tenant reaches 90% of their dollar quota: send warning header `X-AI-Quota-Warning: 90% consumed`.
- When quota is reached (100%): block immediately with HTTP 402 Payment Required or HTTP 429 Too Many Requests.
