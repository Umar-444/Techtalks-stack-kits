# 03 Redis Caching And Rate Limiting

# Redis Caching and Rate Limiting

1. **Cache-Aside Pattern**: Implement cache-aside for high-read entities. Check Redis before querying PostgreSQL; on cache miss, populate Redis with an explicit TTL. Never set keys with indefinite expiration.
2. **Cache Key Namespacing**: Format Redis keys predictably: `entity:{tenant_id}:{id}` (e.g. `user:org-alpha:1001`). Never use un-namespaced generic keys.
3. **Sliding Window Rate Limiter**: Guard public and authenticated endpoints with Redis-backed rate limiting. Rate limit headers (`X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`) must be set on every response.
4. **Connection Resiliency**: Redis client connection errors must gracefully degrade to database fallback rather than halting the entire HTTP request lifecycle.
5. **Serialization Safety**: Store cached payloads in compact JSON or Protobuf. Always handle unmarshaling errors defensively.

