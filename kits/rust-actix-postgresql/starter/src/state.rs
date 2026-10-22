use sea_orm::DatabaseConnection;

#[derive(Clone)]
pub struct AppState {
    pub db: Option<DatabaseConnection>,
    pub app_name: String,
    pub version: String,
}
