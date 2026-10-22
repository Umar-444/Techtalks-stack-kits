use actix_web::{web, HttpResponse, Responder};
use validator::Validate;

use crate::{
    dtos::{CreateItemRequest, HealthResponse, ItemResponse, PaginationParams},
    errors::AppError,
    state::AppState,
};

pub async fn health_check(state: web::Data<AppState>) -> impl Responder {
    HttpResponse::Ok().json(HealthResponse {
        status: "ok".to_string(),
        app: state.app_name.clone(),
        version: state.version.clone(),
        runtime: "actix-tokio".to_string(),
    })
}

pub async fn list_items(
    _state: web::Data<AppState>,
    params: web::Query<PaginationParams>,
) -> Result<impl Responder, AppError> {
    // Clamp pagination limit between 1 and 100 to prevent DoS
    let limit = params.limit.unwrap_or(20).clamp(1, 100);
    let offset = params.offset.unwrap_or(0);

    // Mock response demonstration
    let sample_items = vec![
        ItemResponse {
            id: 1,
            title: "Production Infrastructure Item".to_string(),
            description: Some("Configured with bounded connection pooling".to_string()),
            created_at: "2026-10-22T00:00:00Z".to_string(),
        },
    ];

    Ok(HttpResponse::Ok().json(serde_json::json!({
        "data": sample_items,
        "meta": {
            "limit": limit,
            "offset": offset,
            "total": 1
        }
    })))
}

pub async fn create_item(
    _state: web::Data<AppState>,
    body: web::Json<CreateItemRequest>,
) -> Result<impl Responder, AppError> {
    // Enforce validator crate bounds
    body.validate()
        .map_err(|err| AppError::ValidationError(err.to_string()))?;

    let created = ItemResponse {
        id: 101,
        title: body.title.clone(),
        description: body.description.clone(),
        created_at: "2026-10-22T14:00:00Z".to_string(),
    };

    Ok(HttpResponse::Created().json(serde_json::json!({
        "data": created,
        "status": "created"
    })))
}

pub async fn get_item(
    _state: web::Data<AppState>,
    path: web::Path<i32>,
) -> Result<impl Responder, AppError> {
    let item_id = path.into_inner();
    if item_id <= 0 {
        return Err(AppError::ValidationError("Item ID must be positive".to_string()));
    }

    if item_id != 1 {
        return Err(AppError::NotFound(format!("Item with id {} was not found", item_id)));
    }

    Ok(HttpResponse::Ok().json(serde_json::json!({
        "data": ItemResponse {
            id: 1,
            title: "Production Infrastructure Item".to_string(),
            description: Some("Configured with bounded connection pooling".to_string()),
            created_at: "2026-10-22T00:00:00Z".to_string(),
        }
    })))
}
