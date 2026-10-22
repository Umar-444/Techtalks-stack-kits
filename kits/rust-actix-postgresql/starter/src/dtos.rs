use serde::{Deserialize, Serialize};
use validator::Validate;

#[derive(Debug, Serialize, Deserialize)]
pub struct HealthResponse {
    pub status: String,
    pub app: String,
    pub version: String,
    pub runtime: String,
}

#[derive(Debug, Deserialize, Validate)]
pub struct CreateItemRequest {
    #[validate(length(min = 1, max = 150, message = "Title must be between 1 and 150 characters"))]
    pub title: String,

    #[validate(length(max = 1000, message = "Description must not exceed 1000 characters"))]
    pub description: Option<String>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ItemResponse {
    pub id: i32,
    pub title: String,
    pub description: Option<String>,
    pub created_at: String,
}

#[derive(Debug, Deserialize)]
pub struct PaginationParams {
    pub limit: Option<usize>,
    pub offset: Option<usize>,
}
