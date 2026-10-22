use actix_web::{test, web, App};
use rust_actix_postgresql_starter::{
    configure_app,
    dtos::HealthResponse,
    state::AppState,
};

#[actix_rt::test]
async fn test_healthz_endpoint() {
    let state = web::Data::new(AppState {
        db: None,
        app_name: "rust-actix-postgresql".to_string(),
        version: "1.0.0".to_string(),
    });

    let app = test::init_service(
        App::new()
            .app_data(state.clone())
            .configure(configure_app),
    )
    .await;

    let req = test::TestRequest::get().uri("/healthz").to_request();
    let resp: HealthResponse = test::call_and_read_body_json(&app, req).await;

    assert_eq!(resp.status, "ok");
    assert_eq!(resp.app, "rust-actix-postgresql");
    assert_eq!(resp.runtime, "actix-tokio");
}

#[actix_rt::test]
async fn test_validation_error_on_empty_title() {
    let state = web::Data::new(AppState {
        db: None,
        app_name: "rust-actix-postgresql".to_string(),
        version: "1.0.0".to_string(),
    });

    let app = test::init_service(
        App::new()
            .app_data(state.clone())
            .configure(configure_app),
    )
    .await;

    let req = test::TestRequest::post()
        .uri("/api/v1/items")
        .set_json(serde_json::json!({
            "title": "",
            "description": "Invalid empty title"
        }))
        .to_request();

    let resp = test::call_service(&app, req).await;
    assert_eq!(resp.status(), actix_web::http::StatusCode::BAD_REQUEST);
}
