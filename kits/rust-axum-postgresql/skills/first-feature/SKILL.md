---
name: first-feature
description: Guide for scaffolding a new resourceful endpoint with SQLx migrations, domain model, handler, and integration test.
---

# First Feature Skill: Adding an Item Resource

## Overview
Step-by-step walkthrough for adding an `items` resource in Axum with PostgreSQL persistence and compile-time queries.

## Implementation Guide

### 1. Author SQL Migration in `migrations/0002_create_orders.sql`
```sql
CREATE TABLE IF NOT EXISTS orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_name VARCHAR(255) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### 2. Define Model and Handlers in `src/handlers.rs`
```rust
#[derive(Serialize, Deserialize, sqlx::FromRow)]
pub struct Order {
    pub id: Uuid,
    pub customer_name: String,
    pub amount: f64,
}

pub async fn list_orders(State(pool): State<PgPool>) -> Result<Json<Vec<Order>>, AppError> {
    let orders = sqlx::query_as!(Order, "SELECT id, customer_name, amount::float8 as amount FROM orders")
        .fetch_all(&pool)
        .await
        .map_err(AppError::Database)?;
    Ok(Json(orders))
}
```

### 3. Register Route in `src/main.rs`
```rust
let app = Router::new()
    .route("/api/orders", get(list_orders))
    .with_state(pool);
```

### 4. Integration Test in `tests/api_test.rs`
```rust
#[tokio::test]
async fn test_list_orders() {
    let app = create_app(pool).await;
    let res = app.oneshot(Request::builder().uri("/api/orders").body(Body::empty()).unwrap()).await.unwrap();
    assert_eq!(res.status(), StatusCode::OK);
}
```
