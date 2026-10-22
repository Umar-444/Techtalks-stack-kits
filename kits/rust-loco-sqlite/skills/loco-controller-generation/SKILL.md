---
name: loco-controller-generation
description: Author Loco controllers with Axum extractors, strongly typed JSON views, and error envelopes.
---

# Loco Controller Generation and Routing

## Controller Structure
Loco controllers wrap Axum handlers into clean, testable units using the `Routes` builder:

```rust
use axum::debug_handler;
use loco_rs::prelude::*;

#[debug_handler]
pub async fn list(
    State(ctx): State<AppContext>,
    Query(params): Query<PaginationQuery>,
) -> Result<Response> {
    let limit = params.limit.unwrap_or(20).clamp(1, 100);
    let items = Entity::find()
        .limit(limit)
        .all(&ctx.db)
        .await?;
    format::json(items)
}

pub fn routes() -> Routes {
    Routes::new()
        .prefix("api/v1/records")
        .add("/", get(list))
}
```

## Response Envelopes and Presentation Views
Keep API contract serialization decoupled from SeaORM entities by defining presentation structs in `src/views/`:
```rust
#[derive(Serialize)]
pub struct ItemView {
    pub id: i32,
    pub title: String,
    pub description: Option<String>,
}

impl From<Model> for ItemView {
    fn from(m: Model) -> Self {
        Self {
            id: m.id,
            title: m.title,
            description: m.description,
        }
    }
}
```
