pub mod dtos;
pub mod errors;
pub mod handlers;
pub mod state;

use actix_cors::Cors;
use actix_web::web;

pub fn configure_cors(allowed_origins: &str) -> Cors {
    let mut cors = Cors::default()
        .allowed_methods(vec!["GET", "POST", "PUT", "DELETE"])
        .allowed_headers(vec![
            actix_web::http::header::AUTHORIZATION,
            actix_web::http::header::ACCEPT,
            actix_web::http::header::CONTENT_TYPE,
        ])
        .max_age(3600);

    for origin in allowed_origins.split(',') {
        let trimmed = origin.trim();
        if !trimmed.is_empty() {
            cors = cors.allowed_origin(trimmed);
        }
    }
    cors
}

pub fn configure_app(cfg: &mut web::ServiceConfig) {
    cfg.service(
        web::resource("/healthz").route(web::get().to(handlers::health_check)),
    )
    .service(
        web::resource("/health").route(web::get().to(handlers::health_check)),
    )
    .service(
        web::scope("/api/v1")
            .service(
                web::resource("/items")
                    .route(web::get().to(handlers::list_items))
                    .route(web::post().to(handlers::create_item)),
            )
            .service(
                web::resource("/items/{id}")
                    .route(web::get().to(handlers::get_item)),
            ),
    );
}
