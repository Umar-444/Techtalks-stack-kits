use axum::debug_handler;
use loco_rs::prelude::*;
use serde::Serialize;

#[derive(Serialize)]
pub struct HealthResponse {
    pub status: String,
    pub app: String,
    pub version: String,
    pub framework: String,
}

#[debug_handler]
pub async fn health_check() -> Result<Response> {
    format::json(HealthResponse {
        status: "ok".to_string(),
        app: "rust-loco-sqlite".to_string(),
        version: "1.0.0".to_string(),
        framework: "loco.rs".to_string(),
    })
}

pub fn routes() -> Routes {
    Routes::new()
        .add("/healthz", get(health_check))
        .add("/health", get(health_check))
}
