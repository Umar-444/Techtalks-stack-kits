---
name: install-and-verify
description: Install dependencies, run the audit CLI against sample test files, and verify the SARIF reporting engine.
---

# Install and Verify: Reverse Engineering & Security Audit Pack

## Prerequisites
- Python 3.12+
- `pip` package manager

## Quickstart Steps

1. **Install Python Dependencies**:
   ```bash
   cd starter
   pip install -r requirements.txt
   ```

2. **Execute Sample Security Audit**:
   ```bash
   python cli.py scan --path tests/sample_code.py --format console
   ```

3. **Verify SARIF Output Generation**:
   ```bash
   python cli.py scan --path tests/sample_code.py --format sarif --out audit-results.sarif
   cat audit-results.sarif
   ```

4. **Run Automated Test Suite**:
   ```bash
   pytest tests/
   ```
