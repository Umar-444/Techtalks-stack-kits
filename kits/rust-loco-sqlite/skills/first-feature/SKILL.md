---
name: first-feature
description: Scaffold a new model, migration, and controller using Loco generators and SeaORM ActiveModel.
---

# First Feature: Scaffolding Loco Model & Controller

## Step 1: Scaffold Model and Migration
Using the Loco CLI:
```bash
cargo loco generate scaffold item title:string description:string
```

This generates:
- Entity and model: `src/models/items.rs`
- Controller: `src/controllers/items.rs`
- Migration: `migration/src/m20261022_xxxxxx_items.rs`

## Step 2: Implement Controller Actions
In `src/controllers/items.rs`:
```rust
use axum::debug_handler;
use loco_rs::prelude::*;
use crate::models::_entities::items::{ActiveModel, Entity, Model};

#[derive(Clone, Debug, Serialize, Deserialize, Validate)]
pub struct CreateItemParams {
    #[validate(length(min = 1, max = 150))]
    pub title: String,
    pub description: Option<String>,
}

#[debug_handler]
pub async fn create(
    State(ctx): State<AppContext>,
    Json(params): Json<CreateItemParams>,
) -> Result<Response> {
    params.validate()?;
    let mut item = ActiveModel {
        title: Set(params.title),
        description: Set(params.description),
        ..Default::default()
    };
    let item = item.insert(&ctx.db).await?;
    format::json(item)
}

pub fn routes() -> Routes {
    Routes::new()
        .prefix("api/v1/items")
        .add("/", post(create))
}
```

## Step 3: Register in App Lifecycle
In `src/app.rs`:
```rust
impl Hooks for App {
    fn routes(_ctx: &AppContext) -> AppRoutes {
        AppRoutes::with_default_routes()
            .add_route(controllers::items::routes())
    }
}
```
