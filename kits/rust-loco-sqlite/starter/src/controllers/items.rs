use axum::debug_handler;
use loco_rs::prelude::*;
use serde::{Deserialize, Serialize};
use validator::Validate;

#[derive(Clone, Debug, Deserialize, Serialize, Validate)]
pub struct CreateItemParams {
    #[validate(length(min = 1, max = 150, message = "Title must be between 1 and 150 characters"))]
    pub title: String,

    #[validate(length(max = 1000, message = "Description must not exceed 1000 characters"))]
    pub description: Option<String>,
}

#[derive(Serialize)]
pub struct ItemResponse {
    pub id: i32,
    pub title: String,
    pub description: Option<String>,
    pub created_at: String,
}

#[debug_handler]
pub async fn list(State(_ctx): State<AppContext>) -> Result<Response> {
    let mock_items = vec![
        ItemResponse {
            id: 1,
            title: "Embedded SQLite Record".to_string(),
            description: Some("Operated under WAL mode with zero database locks".to_string()),
            created_at: "2026-10-22T00:00:00Z".to_string(),
        }
    ];

    format::json(serde_json::json!({
        "data": mock_items,
        "meta": { "total": 1 }
    }))
}

#[debug_handler]
pub async fn create(
    State(_ctx): State<AppContext>,
    Json(params): Json<CreateItemParams>,
) -> Result<Response> {
    params.validate()
        .map_err(|err| Error::BadRequest(err.to_string()))?;

    let item = ItemResponse {
        id: 101,
        title: params.title,
        description: params.description,
        created_at: "2026-10-22T14:30:00Z".to_string(),
    };

    format::json(serde_json::json!({
        "data": item,
        "status": "created"
    }))
}

pub fn routes() -> Routes {
    Routes::new()
        .prefix("api/v1/items")
        .add("/", get(list))
        .add("/", post(create))
}
