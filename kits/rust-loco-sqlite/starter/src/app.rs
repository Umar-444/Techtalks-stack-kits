use loco_rs::prelude::*;

pub struct App;
impl Hooks for App {
    fn app_name() -> &'static str {
        "loco_sqlite_app"
    }
}
