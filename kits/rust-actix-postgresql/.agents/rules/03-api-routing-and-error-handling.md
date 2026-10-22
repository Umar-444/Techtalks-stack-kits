# 03 Api Routing And Error Handling

# API Routing and Unified Error Handling

1. **Modular Scope Routing**: Group API endpoints logically under `web::scope("/api/v1")`. Bind route handlers with explicit HTTP verb macros (`web::get()`, `web::post()`, `web::put()`, `web::delete()`).
2. **Type-Safe State Extraction**: Inject database connections and configuration using Actix `web::Data<AppState>`. Never rely on global mutable singletons or static variables.
3. **Unified ResponseError Enum**: Define a centralized `AppError` enum implementing `actix_web::ResponseError`. Override `error_response(&self) -> HttpResponse` to output uniform JSON envelopes (`{"error": {"code": ..., "message": ...}}`).
4. **Information Disclosure Prevention**: Capture underlying `sea_orm::DbErr` or I/O errors and log details internally with `tracing::error!()`. Return safe, generic HTTP 500 error messages to API consumers to prevent schema exposure.
5. **Structured JSON Responses**: Standardize all successful API responses into predictable JSON structures (`{"data": ..., "meta": ...}`) with appropriate HTTP status codes (200, 201, 204).

