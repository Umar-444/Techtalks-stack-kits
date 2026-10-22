use serde::Serialize;

#[derive(Serialize)]
pub struct ApiResponse<T> {
    pub data: T,
    pub status: String,
}
