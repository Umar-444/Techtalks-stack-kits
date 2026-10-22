# Pytest-Asyncio Test Suites and Evaluation Gates

# Testing and Evaluation Gates
- Every node function in the LangGraph workflow must have an isolated unit test in 	ests/test_graph.py.
- Mock external LLM API calls in CI using pytest fixtures to guarantee deterministic, fast test runs.
- Verify token budget consumption: total session tokens must not exceed 20,000 tokens per standard query.
- Assert API response contracts using FastAPI TestClient in 	ests/test_api.py.
