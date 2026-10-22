# Framework Architecture and Standards: Security Audit & Analysis Pack

1. **Defensive Audit Architecture**: Structure code into modular analyzer packages: `cli.py` (CLI runner and argument parsing), `analyzers/ast_analyzer.py` (AST visitor-based source code audits), `analyzers/binary_checker.py` (ELF/PE header security verification), and `reporting/` (SARIF and JSON report generators).
2. **Strict Typing and Python 3.12+ Standards**: Use modern Python type hints (`dataclass`, `typing.Protocol`, pipe unions `X | Y`). Validate analyzer configurations using Pydantic or dataclasses with zero reliance on untyped dictionaries.
3. **Deterministic Scan Execution**: Analyzers must operate deterministically without side effects. Scanners must read files in read-only mode (`O_RDONLY`), calculate SHA-256 hashes of targets, and generate reproducible vulnerability findings.
4. **Standard SARIF 2.1.0 Export**: Standardize all security findings into OASIS SARIF (Static Analysis Results Interchange Format) JSON format, enabling direct ingestion into GitHub Code Scanning, GitLab Security Dashboard, and DefectDojo.
5. **No External Attack Code**: All tools and rules in this pack are strictly defensive and diagnostic. Rules identify weaknesses, insecure compiler flags, and misconfigurations; they do not generate offensive payloads, exploits, or weaponized bypasses.
