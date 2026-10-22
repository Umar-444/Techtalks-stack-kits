# Framework Architecture and Standards: Haystack 2.5+ and Weaviate

1. **Explicit DAG Component Wiring**: Haystack 2.x uses explicit, directional DAG connections via `pipeline.connect("component_a.output", "component_b.input")`. Never use implicit or hidden execution flow.
2. **Component Isolation**: Every pipeline component must implement the `@component` decorator with typed inputs and outputs. Do not mutate global state inside components.
3. **Async FastAPI Layer**: Expose pipeline executions through FastAPI endpoints with typed Pydantic models. All blocking pipeline calls must execute asynchronously or in a worker thread pool.
4. **Environment Invariant**: All external service hosts (`WEAVIATE_URL`, `OPENAI_API_BASE`) must be injected through environment variables. Zero hardcoded localhost URLs in production code.
5. **Python 3.12+ Typing**: Use standard type annotations (`list[str]`, `dict[str, Any]`, `str | None`). Do not use legacy typing imports (`typing.List`, `typing.Optional`).
