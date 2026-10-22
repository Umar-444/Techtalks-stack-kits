# Design Notes: OWASP API Security Top 10 (2023) Test Harness

## Architecture Rationale: API Test Harness & OpenAPI Portal
This kit is an **API security reference implementation and automated test harness**.
Unlike traditional frontend applications, its interfaces are:
1. **Interactive OpenAPI / Swagger Documentation**: Available at `/docs` and `/redoc` providing complete schema specifications, parameter definitions, and error responses.
2. **Automated Pytest Security Suite**: Comprehensive test suite (`starter/tests/test_owasp_top10.py`) verifying all 10 OWASP API vulnerability classes.
3. **Health Check Probe**: Route `/healthz` returning JSON status for container and Kubernetes liveness probes.
