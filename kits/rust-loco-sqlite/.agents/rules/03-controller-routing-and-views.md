# 03 Controller Routing And Views

# Controller Routing, Extractors, and Views

1. **Declarative Controller Routes**: Implement controller routing via `Routes::new()`. Register endpoint handlers using `.add("/", get(list))` and `.add("/:id", get(get_one))`, mounting them cleanly in `src/app.rs`.
2. **Type-Safe Extractors**: Extract parameters using Axum/Loco extractors: `State<AppContext>`, `Json<T>`, `Path<T>`, and `Query<T>`. Never access raw HTTP query strings or unstructured body streams.
3. **Standardized Response Formatting**: Return responses using Loco's `format::json(...)` and `format::empty(...)` helpers. Standardize envelopes (`{"data": ..., "meta": ...}`) across all collection endpoints.
4. **Unified Error Handling**: Return `Result<Response>` from all controller actions. Handle domain errors via Loco's `Error` enum or custom app error types, ensuring internal database errors are logged with `tracing::error!` and masked from clients.
5. **Separation of Presentation Views**: Keep JSON response formatting in `src/views/` modules to separate HTTP serializations from internal entity definitions and database models.

