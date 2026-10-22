---
name: install-and-verify
description: Complete setup, tool verification, local pipeline simulation run, and SARIF output validation.
---

# Install and Verify Skill: DevSecOps CI Pipeline

## Overview
Verify all required DevSecOps CLI tools, validate rule definitions, execute local pipeline simulation, and inspect SARIF outputs.

## Execution Steps

### 1. Verify Security Tools
Verify installed command-line utilities:
```bash
git --version
python3 --version
docker --version
```

### 2. Run Local Security Pipeline Simulation
Execute the local runner script to scan secrets, AST rules, and container configs:
```bash
python3 starter/scripts/run_local_pipeline.py
```
Expected output:
```text
[PASS] Secret Scan (Gitleaks): 0 secrets detected
[PASS] SAST Analysis (Semgrep): 0 policy violations
[PASS] Container Audit (Hadolint/Trivy): Passed non-root & pinned tag checks
[SUCCESS] Pipeline simulation completed with 0 errors!
```

### 3. Validate Configuration Files
Lint workflow syntax and scanner configs:
```bash
python3 -c "import yaml; yaml.safe_load(open('starter/.github/workflows/devsecops.yml'))"
python3 -c "import yaml; yaml.safe_load(open('starter/.semgrep.yml'))"
python3 -c "import yaml; yaml.safe_load(open('starter/trivy.yaml'))"
```

### 4. Health Check Probe
Start the mock microservice container and probe `/healthz`:
```bash
python3 starter/app/main.py &
sleep 2
curl -s http://localhost:8080/healthz
```
Expected output:
```json
{"status":"ok","app":"security-devsecops-ci","version":"1.0.0"}
```
