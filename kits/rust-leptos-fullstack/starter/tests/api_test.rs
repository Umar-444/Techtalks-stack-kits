use axum::{
    body::Body,
    http::{Request, StatusCode},
};
use http_body_util::BodyExt;
use rust_leptos_fullstack_starter::app::HealthResponse;
use tower::ServiceExt;

#[tokio::test]
async fn test_health_response_schema() {
    let resp = HealthResponse {
        status: "ok".to_string(),
        app: "rust-leptos-fullstack".to_string(),
        version: "1.0.0".to_string(),
        runtime: "axum-wasm".to_string(),
    };

    assert_eq!(resp.status, "ok");
    assert_eq!(resp.app, "rust-leptos-fullstack");
    assert_eq!(resp.runtime, "axum-wasm");
}
