use axum::{response::Json, routing::get, Router};
use rust_leptos_fullstack_starter::app::{App, HealthResponse};
use std::env;

async fn health_check() -> Json<HealthResponse> {
    Json(HealthResponse {
        status: "ok".to_string(),
        app: "rust-leptos-fullstack".to_string(),
        version: "1.0.0".to_string(),
        runtime: "axum-wasm".to_string(),
    })
}

pub fn create_app() -> Router {
    Router::new()
        .route("/healthz", get(health_check))
        .route("/health", get(health_check))
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    dotenvy::dotenv().ok();
    tracing_subscriber::fmt::init();

    let host = env::var("HOST").unwrap_or_else(|_| "0.0.0.0".to_string());
    let port = env::var("PORT").unwrap_or_else(|_| "3000".to_string());
    let addr = format!("{}:{}", host, port);

    let app = create_app();

    tracing::info!("Starting Leptos Axum SSR server on {}", addr);
    let listener = tokio::net::TcpListener::bind(&addr).await?;
    axum::serve(listener, app).await?;

    Ok(())
}
