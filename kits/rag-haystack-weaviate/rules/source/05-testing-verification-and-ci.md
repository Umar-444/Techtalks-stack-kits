# Testing, Verification, and CI Invariants

1. **Non-Root Container Security**: Dockerfiles must compile with a dedicated unprivileged user (`USER 10001:10001`). Never execute services as root inside production containers.
2. **Strict CORS Policy**: CORS middleware must parse allowed origins strictly from the `ALLOWED_ORIGINS` environment variable. Never configure `allow_origins=["*"]`.
3. **Deterministic Test Isolation**: Pytest test cases must run independently with mock or in-memory vector storage fallback, ensuring the entire test suite passes in under 3 seconds.
4. **Dependency Pinning**: All dependencies in `requirements.txt` must be pinned with exact or minimum bounded versions (`package>=X.Y.Z`).
5. **No Secret Invariants**: Zero credentials, API keys, or private certificates may be committed to version control. Verified via automated Gitleaks scans.
