use actix_web::{http::StatusCode, HttpResponse, ResponseError};
use serde::Serialize;
use std::fmt;

#[derive(Debug, Serialize)]
pub struct ErrorEnvelope {
    pub error: String,
    pub status: u16,
}

#[derive(Debug, thiserror::Error)]
pub enum AppError {
    #[error("Database error: {0}")]
    DatabaseError(String),

    #[error("Validation failed: {0}")]
    ValidationError(String),

    #[error("Resource not found: {0}")]
    NotFound(String),

    #[error("Internal server error")]
    InternalError,
}

impl ResponseError for AppError {
    fn status_code(&self) -> StatusCode {
        match self {
            AppError::ValidationError(_) => StatusCode::BAD_REQUEST,
            AppError::NotFound(_) => StatusCode::NOT_FOUND,
            AppError::DatabaseError(_) => StatusCode::INTERNAL_SERVER_ERROR,
            AppError::InternalError => StatusCode::INTERNAL_SERVER_ERROR,
        }
    }

    fn error_response(&self) -> HttpResponse {
        let status = self.status_code();
        let error_message = match self {
            AppError::ValidationError(msg) => msg.clone(),
            AppError::NotFound(msg) => msg.clone(),
            // Mask internal database details from end users
            AppError::DatabaseError(_) => "A database error occurred. Please try again later.".to_string(),
            AppError::InternalError => "Internal server error".to_string(),
        };

        HttpResponse::build(status).json(ErrorEnvelope {
            error: error_message,
            status: status.as_u16(),
        })
    }
}
