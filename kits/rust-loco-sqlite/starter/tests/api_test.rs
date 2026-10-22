use rust_loco_sqlite_starter::controllers::health::HealthResponse;

#[tokio::test]
async fn test_health_response_schema() {
    let res = HealthResponse {
        status: "ok".to_string(),
        app: "rust-loco-sqlite".to_string(),
        version: "1.0.0".to_string(),
        framework: "loco.rs".to_string(),
    };

    assert_eq!(res.status, "ok");
    assert_eq!(res.app, "rust-loco-sqlite");
    assert_eq!(res.framework, "loco.rs");
}

#[test]
fn test_item_validation() {
    use rust_loco_sqlite_starter::controllers::items::CreateItemParams;
    use validator::Validate;

    let valid_params = CreateItemParams {
        title: "Valid Item".to_string(),
        description: Some("Description".to_string()),
    };
    assert!(valid_params.validate().is_ok());

    let invalid_params = CreateItemParams {
        title: "".to_string(),
        description: None,
    };
    assert!(invalid_params.validate().is_err());
}
