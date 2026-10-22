---
name: redis-cache-layer
description: Implement resilient cache-aside and sliding window rate limiting in Go using go-redis.
---
# Redis Cache Layer Skill

## 1. Initialize Redis Client
```go
import "github.com/redis/go-redis/v9"

func NewRedisClient(addr string) *redis.Client {
    return redis.NewClient(&redis.Options{
        Addr:         addr,
        Password:     "", // from env in production
        DB:           0,
        PoolSize:     20,
        MinIdleConns: 5,
    })
}
```

## 2. Cache-Aside Implementation
```go
func (s *Service) GetUser(ctx context.Context, id int64) (*User, error) {
    key := fmt.Sprintf("user:%d", id)
    cached, err := s.redis.Get(ctx, key).Result()
    if err == nil {
        var u User
        if json.Unmarshal([]byte(cached), &u) == nil {
            return &u, nil
        }
    }
    
    // DB Fallback on cache miss
    user, err := s.repo.GetUser(ctx, id)
    if err != nil {
        return nil, err
    }
    
    // Asynchronous or defensive cache set with TTL
    if data, err := json.Marshal(user); err == nil {
        _ = s.redis.Set(ctx, key, data, 15*time.Minute).Err()
    }
    return user, nil
}
```

## 3. Done Means
- Redis errors degrade gracefully to database fallback.
- All keys declare an explicit TTL (never 0 / infinite).
