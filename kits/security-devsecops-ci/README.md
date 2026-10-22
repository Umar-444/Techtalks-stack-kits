# DevSecOps CI/CD Security Pipeline Stack Kit

A battle-tested, production-grade security automation harness for GitHub Actions and local developer pre-commit stages.
Enforces shift-left security with secret detection, SAST, container CVE scanning, SBOM generation, and SARIF integration.

## Architecture & Tools
- **Pipeline Automation**: GitHub Actions v4
- **Secret Scanning**: Gitleaks 8+ (`.gitleaks.toml`)
- **Static Analysis (SAST)**: Semgrep OSS with custom AST rules (`.semgrep.yml`)
- **Container & Dependency Scanning**: Aqua Security Trivy (`trivy.yaml`)
- **Supply Chain SBOM**: Anchore Syft (CycloneDX 1.5 & SPDX 2.3)
- **Local Runner**: Cross-platform Python pipeline (`starter/scripts/run_local_pipeline.py`)
- **Reporting**: Native SARIF 2.1.0 integration with GitHub Security tab

## Quickstart

### 1. Run Local Pipeline Simulation
```bash
python3 starter/scripts/run_local_pipeline.py
```

### 2. Run Pipeline Unit Tests
```bash
python3 starter/tests/pipeline_test.py
```

### 3. Run Mock Test Container & Health Check
```bash
docker compose -f starter/docker-compose.yml up -d
curl http://localhost:8080/healthz
```

### 4. Enable GitHub Actions
Copy `starter/.github/workflows/devsecops.yml` into your repository's `.github/workflows/` directory.

## Design Rationale
See [`DESIGN-NOTES.md`](DESIGN-NOTES.md) for detailed explanations on why this infrastructure kit focuses on CI automation and SARIF outputs rather than a web UI.
