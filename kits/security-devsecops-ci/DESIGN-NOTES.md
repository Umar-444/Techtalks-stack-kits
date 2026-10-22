# Design Notes: Security DevSecOps CI/CD Stack Kit

## Architecture Rationale: Why No Web UI?
This kit is an **infrastructure and automation harness** designed to execute across continuous integration (GitHub Actions) and local developer pre-commit stages.
Unlike user-facing web applications, its outputs are:
1. **SARIF Reports** (`sarif-2.1.0`) ingested directly by GitHub's Code Scanning and Security tabs.
2. **Software Bill of Materials (SBOM)** artifacts in SPDX and CycloneDX specifications for regulatory compliance.
3. **Local CLI Output** via `starter/scripts/run_local_pipeline.py` providing instant feedback before developers commit.

To provide seamless testing and container validation, the kit includes a hardened mock microservice (`starter/app/main.py`) running inside a non-root Alpine container with an automated `/healthz` endpoint.
