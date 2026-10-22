use actix_web::{middleware::Logger, web, App, HttpServer};
use dotenvy::dotenv;
use rust_actix_postgresql_starter::{configure_app, configure_cors, state::AppState};
use std::env;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    dotenv().ok();
    env_logger::init_from_env(env_logger::Env::new().default_filter_or("info"));

    let host = env::var("HOST").unwrap_or_else(|_| "0.0.0.0".to_string());
    let port = env::var("PORT")
        .unwrap_or_else(|_| "8080".to_string())
        .parse::<u16>()
        .expect("PORT must be a valid u16 integer");

    let allowed_origins = env::var("ALLOWED_ORIGINS")
        .unwrap_or_else(|_| "http://localhost:3000,http://localhost:8080".to_string());

    let state = web::Data::new(AppState {
        db: None,
        app_name: "rust-actix-postgresql".to_string(),
        version: "1.0.0".to_string(),
    });

    log::info!("Starting Actix Web server on {}:{}", host, port);

    HttpServer::new(move || {
        App::new()
            .app_data(state.clone())
            .wrap(Logger::default())
            .wrap(configure_cors(&allowed_origins))
            .configure(configure_app)
    })
    .bind((host, port))?
    .run()
    .await
}
