use axum::{
    extract::{Path, Query, State},
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use sqlx::PgPool;
use uuid::Uuid;

// Unified Error Handling
pub enum AppError {
    Database(sqlx::Error),
    NotFound(String),
    Validation(String),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, error_message) = match self {
            AppError::Database(err) => {
                tracing::error!("Database error: {:?}", err);
                (StatusCode::INTERNAL_SERVER_ERROR, "Internal server error".to_string())
            }
            AppError::NotFound(msg) => (StatusCode::NOT_FOUND, msg),
            AppError::Validation(msg) => (StatusCode::BAD_REQUEST, msg),
        };

        let body = Json(serde_json::json!({ "error": error_message, "status": status.as_u16() }));
        (status, body).into_response()
    }
}

impl From<sqlx::Error> for AppError {
    fn from(err: sqlx::Error) -> Self {
        AppError::Database(err)
    }
}

// Health Check Response
#[derive(Serialize)]
pub struct HealthResponse {
    pub status: &'static str,
    pub app: &'static str,
    pub version: &'static str,
    pub runtime: &'static str,
}

pub async fn health_check() -> impl IntoResponse {
    Json(HealthResponse {
        status: "ok",
        app: "rust-axum-postgresql",
        version: "1.0.0",
        runtime: "tokio",
    })
}

// Item Models & Schemas
#[derive(Serialize, Deserialize, sqlx::FromRow)]
pub struct Item {
    pub id: Uuid,
    pub name: String,
    pub description: Option<String>,
    pub created_at: DateTime<Utc>,
}

#[derive(Deserialize)]
pub struct CreateItemRequest {
    pub name: String,
    pub description: Option<String>,
}

#[derive(Deserialize)]
pub struct PaginationQuery {
    pub limit: Option<i64>,
    pub offset: Option<i64>,
}

pub async fn list_items(
    State(pool): State<PgPool>,
    Query(pagination): Query<PaginationQuery>,
) -> Result<Json<Vec<Item>>, AppError> {
    let limit = pagination.limit.unwrap_or(50).clamp(1, 100);
    let offset = pagination.offset.unwrap_or(0).max(0);

    let items = sqlx::query_as!(
        Item,
        "SELECT id, name, description, created_at FROM items ORDER BY created_at DESC LIMIT $1 OFFSET $2",
        limit,
        offset
    )
    .fetch_all(&pool)
    .await?;

    Ok(Json(items))
}

pub async fn get_item(
    State(pool): State<PgPool>,
    Path(id): Path<Uuid>,
) -> Result<Json<Item>, AppError> {
    let item = sqlx::query_as!(
        Item,
        "SELECT id, name, description, created_at FROM items WHERE id = $1",
        id
    )
    .fetch_optional(&pool)
    .await?;

    match item {
        Some(i) => Ok(Json(i)),
        None => Err(AppError::NotFound("Item not found".into())),
    }
}

pub async fn create_item(
    State(pool): State<PgPool>,
    Json(payload): Json<CreateItemRequest>,
) -> Result<(StatusCode, Json<Item>), AppError> {
    if payload.name.trim().is_empty() {
        return Err(AppError::Validation("Name cannot be empty".into()));
    }

    let item = sqlx::query_as!(
        Item,
        "INSERT INTO items (name, description) VALUES ($1, $2) RETURNING id, name, description, created_at",
        payload.name.trim(),
        payload.description
    )
    .fetch_one(&pool)
    .await?;

    Ok((StatusCode::CREATED, Json(item)))
}
