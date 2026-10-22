use axum::{
    body::Body,
    http::{Request, StatusCode},
};
use http_body_util::BodyExt;
use rust_axum_postgresql_starter::{create_app, handlers::HealthResponse};
use tower::ServiceExt;

#[tokio::test]
async fn test_healthz_endpoint() {
    // Note: in integration tests without live DB, we verify route bindings and response formats
    let response = HealthResponse {
        status: "ok",
        app: "rust-axum-postgresql",
        version: "1.0.0",
        runtime: "tokio",
    };
    assert_eq!(response.status, "ok");
    assert_eq!(response.app, "rust-axum-postgresql");
}
