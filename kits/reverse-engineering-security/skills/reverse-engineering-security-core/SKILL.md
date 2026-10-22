---
name: reverse-engineering-security-core
description: Core operations, SARIF export, CLI flags, GitHub Actions CI integration, and audit workflows.
---

# Core Operations: Reverse Engineering & Security Audit Pack

## Stack Highlights
- **Python 3.12+**: Modern typed Python with zero heavy C-extension dependencies.
- **AST Visitor Engine**: Static AST scanning for dangerous sinks, SQL injection, and hardcoded secrets.
- **Binary Hardening Auditor**: Pure-Python structural parser for ELF and PE security headers.
- **OASIS SARIF 2.1.0**: Standardized security reporting format for GitHub & GitLab CI integration.

## Project Structure
```text
starter/
├── cli.py                  # Command-line interface
├── requirements.txt        # Pinned Python dependencies
├── analyzers/
│   ├── ast_analyzer.py     # Source code AST scanner
│   └── binary_checker.py   # ELF/PE binary mitigation verifier
├── reporting/
│   ├── sarif_report.py     # SARIF 2.1.0 generator
│   └── console_report.py   # Formatted terminal output
└── tests/
    └── test_audit.py       # Pytest test suite
```

## Essential Commands
- Scan Python source code: `python cli.py scan --path src/`
- Audit compiled binary headers: `python cli.py checksec --binary app`
- Export SARIF report: `python cli.py scan --path src/ --format sarif --out report.sarif`
- Run test suite: `pytest tests/`
