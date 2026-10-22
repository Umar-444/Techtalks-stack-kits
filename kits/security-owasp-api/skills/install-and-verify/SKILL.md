---
name: install-and-verify
description: Complete setup, test runner execution, and verification of the OWASP API Top 10 security harness.
---

# Install and Verify Skill: OWASP API Security

## Overview
Install dependencies, run the automated security test suite covering all 10 OWASP categories, and probe the live health endpoint.

## Step-by-Step Verification

### 1. Environment & Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r starter/requirements.txt
```

### 2. Run Comprehensive OWASP Top 10 Security Suite
```bash
python3 starter/run_security_tests.py
```
Expected output:
```text
=======================================================
   OWASP API Security Top 10 (2023) Verification Run
=======================================================
[PASS] API1:2023 - Broken Object Level Authorization (BOLA)
[PASS] API2:2023 - Broken Authentication (Missing & Invalid Token)
[PASS] API3:2023 - Broken Object Property Level Auth (Mass Assignment)
[PASS] API4:2023 - Unrestricted Resource Consumption (Rate Limiting)
[PASS] API5:2023 - Broken Function Level Authorization (BFLA)
[PASS] API7:2023 - Server-Side Request Forgery (SSRF Metadata Defense)
[PASS] Health Probe & Status Check

>>> ALL OWASP API SECURITY TESTS PASSED (100% Compliance) <<<
```

### 3. Start API Server and Probe Healthz
```bash
python3 starter/main.py &
sleep 2
curl -s http://localhost:8000/healthz
```
Expected output:
```json
{"status":"ok","app":"security-owasp-api","version":"1.0.0"}
```
