---
name: 05-testing-and-verification
description: Pytest-Django Test Suites & OpenAPI Contract Verification
---
# Pytest-Django Testing Invariants
- Use @pytest.mark.django_db on all database-accessing test functions.
- Test endpoints using Django Ninja's TestClient(api) asserting status codes and response models.
- Verify OpenAPI schema generation: test that /api/openapi.json compiles with zero schema warnings.
- Keep test suite execution fast: use an in-memory SQLite database for local test runs.
