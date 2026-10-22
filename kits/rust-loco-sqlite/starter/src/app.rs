use async_trait::async_trait;
use loco_rs::{
    app::{AppContext, Hooks, Initializer},
    boot::{create_app, BootResult, StartMode},
    controller::AppRoutes,
    environment::Environment,
    task::Tasks,
    Result,
};

use crate::controllers;

pub struct App;

#[async_trait]
impl Hooks for App {
    fn app_name() -> &'static str {
        "rust-loco-sqlite"
    }

    fn app_version() -> &'static str {
        "1.0.0"
    }

    fn routes(_ctx: &AppContext) -> AppRoutes {
        AppRoutes::with_default_routes()
            .add_route(controllers::health::routes())
            .add_route(controllers::items::routes())
    }

    async fn initializers(_ctx: &AppContext) -> Result<Vec<Box<dyn Initializer>>> {
        Ok(vec![])
    }

    fn register_tasks(_tasks: &mut Tasks) {}
}
