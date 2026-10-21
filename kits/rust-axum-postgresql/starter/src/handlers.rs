use axum::{extract::{State, Json}, http::StatusCode, response::IntoResponse};
use serde::{Deserialize, Serialize};
use sqlx::PgPool;
use uuid::Uuid;

#[derive(Serialize)]
pub struct HealthResponse {
    pub status: &'static str,
    pub service: &'static str,
}

pub async fn health_check() -> impl IntoResponse {
    Json(HealthResponse { status: "ok", service: "rust-axum-postgresql" })
}

#[derive(Serialize, sqlx::FromRow)]
pub struct Item {
    pub id: Uuid,
    pub name: String,
    pub description: Option<String>,
}

#[derive(Deserialize)]
pub struct CreateItemRequest {
    pub name: String,
    pub description: Option<String>,
}

pub async fn list_items(State(pool): State<PgPool>) -> Result<Json<Vec<Item>>, (StatusCode, String)> {
    let items = sqlx::query_as!(Item, "SELECT id, name, description FROM items ORDER BY id DESC LIMIT 50")
        .fetch_all(&pool)
        .await
        .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()))?;
    Ok(Json(items))
}

pub async fn create_item(
    State(pool): State<PgPool>,
    Json(payload): Json<CreateItemRequest>,
) -> Result<(StatusCode, Json<Item>), (StatusCode, String)> {
    let id = Uuid::new_v4();
    let item = sqlx::query_as!(
        Item,
        "INSERT INTO items (id, name, description) VALUES ($1, $2, $3) RETURNING id, name, description",
        id, payload.name, payload.description
    )
    .fetch_one(&pool)
    .await
    .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()))?;

    Ok((StatusCode::CREATED, Json(item)))
}
