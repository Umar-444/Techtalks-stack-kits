---
name: first-feature
description: Scaffold a new domain entity with SeaORM ActiveModel, input validation DTO, and Actix Web CRUD handlers.
---

# First Feature: Scaffolding Entity and Actix Handler

## Step 1: Define the SeaORM Entity
Create `src/entities/item.rs`:
```rust
use sea_orm::entity::prelude::*;
use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, PartialEq, DeriveEntityModel, Serialize, Deserialize)]
#[sea_orm(table_name = "items")]
pub struct Model {
    #[sea_orm(primary_key)]
    pub id: i32,
    pub title: String,
    pub description: Option<String>,
    pub created_at: DateTimeUtc,
}

#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {}

impl ActiveModelBehavior for ActiveModel {}
```

## Step 2: Define Request DTO with Validation
Create `src/dtos.rs`:
```rust
use serde::Deserialize;
use validator::Validate;

#[derive(Debug, Deserialize, Validate)]
pub struct CreateItemDto {
    #[validate(length(min = 1, max = 150))]
    pub title: String,
    #[validate(length(max = 1000))]
    pub description: Option<String>,
}
```

## Step 3: Implement Actix Web Handler
In `src/handlers.rs`:
```rust
use actix_web::{web, HttpResponse, Responder};
use sea_orm::*;
use validator::Validate;
use crate::{dtos::CreateItemDto, entities::item, errors::AppError, state::AppState};

pub async fn create_item(
    state: web::Data<AppState>,
    body: web::Json<CreateItemDto>,
) -> Result<impl Responder, AppError> {
    body.validate().map_err(|e| AppError::ValidationError(e.to_string()))?;

    let new_item = item::ActiveModel {
        title: Set(body.title.clone()),
        description: Set(body.description.clone()),
        ..Default::default()
    };

    let result = new_item.insert(&state.db).await
        .map_err(|e| AppError::DatabaseError(e.to_string()))?;

    Ok(HttpResponse::Created().json(serde_json::json!({
        "data": result,
        "status": "created"
    })))
}
```

## Step 4: Register in Actix Web Router
In `src/main.rs`:
```rust
App::new()
    .app_data(state.clone())
    .service(
        web::scope("/api/v1")
            .route("/items", web::post().to(handlers::create_item))
    )
```
