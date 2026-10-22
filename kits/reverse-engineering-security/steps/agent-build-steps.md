# Agent Step-by-Step Build Order: Reverse Engineering & Security Audit Pack

1. **Step 1: Environment & Toolchain Setup**: Initialize Python 3.12 virtual environment and install dependencies from `requirements.txt`.
2. **Step 2: AST Security Visitor Engine**: Subclass `ast.NodeVisitor` in `analyzers/ast_analyzer.py` to inspect syntax trees for dangerous sinks (`eval`, `exec`, `shell=True`, and unparameterized SQL).
3. **Step 3: Binary Hardening Verifier**: Implement structural executable header readers in `analyzers/binary_checker.py` to audit NX/DEP, ASLR/PIE, Stack Canaries, and RELRO.
4. **Step 4: SARIF Reporting Pipeline**: Implement OASIS SARIF 2.1.0 exporter in `reporting/sarif_report.py` for integration with GitHub Code Scanning.
5. **Step 5: CLI Runner & Security Gating**: Build `cli.py` with `argparse`, enforcing non-zero exit codes on HIGH severity findings for CI gating.
6. **Step 6: Evaluation, Testing & Containerization**: Execute `pytest tests/` and package into multi-stage rootless Alpine Docker container.
