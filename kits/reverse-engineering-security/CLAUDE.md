# Reverse Engineering & Security Audit Pack — Claude Code Guidelines (CLAUDE.md)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Quick Reference & Non-Negotiable Standards
### 01 Framework Architecture And Standards
# Framework Architecture and Standards: Security Audit & Analysis Pack

1. **Defensive Audit Architecture**: Structure code into modular analyzer packages: `cli.py` (CLI runner and argument parsing), `analyzers/ast_analyzer.py` (AST visitor-based source code audits), `analyzers/binary_checker.py` (ELF/PE header security verification), and `reporting/` (SARIF and JSON report generators).
2. **Strict Typing and Python 3.12+ Standards**: Use modern Python type hints (`dataclass`, `typing.Protocol`, pipe unions `X | Y`). Validate analyzer configurations using Pydantic or dataclasses with zero reliance on untyped dictionaries.
3. **Deterministic Scan Execution**: Analyzers must operate deterministically without side effects. Scanners must read files in read-only mode (`O_RDONLY`), calculate SHA-256 hashes of targets, and generate reproducible vulnerability findings.
4. **Standard SARIF 2.1.0 Export**: Standardize all security findings into OASIS SARIF (Static Analysis Results Interchange Format) JSON format, enabling direct ingestion into GitHub Code Scanning, GitLab Security Dashboard, and DefectDojo.
5. **No External Attack Code**: All tools and rules in this pack are strictly defensive and diagnostic. Rules identify weaknesses, insecure compiler flags, and misconfigurations; they do not generate offensive payloads, exploits, or weaponized bypasses.


### 02 Ast Static Analysis And Pattern Matching
# AST Static Analysis and Semantic Pattern Matching

1. **Python AST NodeVisitor Pattern**: Author code vulnerability analyzers by subclassing `ast.NodeVisitor`. Traverse code syntax trees to locate dangerous functions, unsafe sinks, and insecure coding anti-patterns without executing untrusted code.
2. **Dangerous Sink Detection**: Enforce checks that flag invocations of dangerous dynamic evaluation functions (`eval`, `exec`, `subprocess.Popen(..., shell=True)`, `os.system`) where arguments are not static literals.
3. **SQL Injection String Interpolation**: Inspect database query calls to verify that arguments are not formed via f-strings, `format()`, or `%` modulo concatenation. Require bound parameterized queries across all database drivers.
4. **Hardcoded Secrets Detection**: Scan string literals using entropy analysis (Shannon entropy > 4.5) and regex heuristics to detect hardcoded API keys, JWT tokens, AWS access credentials, and private keys.
5. **Precise AST Source Mapping**: Every AST finding must report the exact file path, starting line number, column offset, and offending source code snippet to facilitate automated remediation.


### 03 Binary Hardening And Exploit Mitigation Verification
# Binary Hardening and Exploit Mitigation Verification

1. **Defensive Binary Flag Inspection**: Verify compiled executable headers (ELF and PE) to ensure modern compiler security protections are enabled. Parse headers safely using pure-Python structural readers without executing target binaries.
2. **ELF Exploit Mitigation Invariants**: Check Linux ELF binaries for mandatory mitigations:
   - **NX/DEP**: Non-Executable Stack (`GNU_STACK` flag set to `RW`, not `RWE`).
   - **PIE/ASLR**: Position Independent Executable (`ET_DYN` type and dynamic symbols enabled).
   - **Stack Canaries**: Presence of `__stack_chk_fail` or `__stack_chk_guard` in the symbol table.
   - **Full RELRO**: Relocation Read-Only (`BIND_NOW` flag set and `PT_GNU_RELRO` segment present).
3. **PE Exploit Mitigation Invariants**: Check Windows PE binaries for `IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE` (ASLR), `IMAGE_DLLCHARACTERISTICS_NX_COMPAT` (DEP), and `IMAGE_DLLCHARACTERISTICS_GUARD_CF` (Control Flow Guard).
4. **Diagnostic Remediation Guidance**: For any binary missing required hardening flags, output specific compiler flags (`-fstack-protector-strong`, `-Wl,-z,relro,-z,now`, `-fPIE -pie`) to guide engineering teams in re-compiling securely.
5. **Non-Destructive Static Inspection**: Binary analysis must perform static structural parsing exclusively. Never execute or dynamically trace untrusted binaries.


### 04 Software Supply Chain And Sbom Validation
# Software Supply Chain and SBOM Validation

1. **CycloneDX and SPDX Parsing**: Ingest and validate Software Bill of Materials (SBOM) documents in CycloneDX 1.5+ and SPDX 2.3+ JSON formats to maintain complete inventory of software dependencies.
2. **Cryptographic Hash Pinning**: Verify that all package dependencies declared in requirements, lockfiles, or SBOMs have associated SHA-256 integrity hashes to prevent dependency substitution and supply-chain tampering.
3. **Vulnerability Advisory Correlation**: Correlate package names and pinned versions against the OSV (Open Source Vulnerabilities) database and CVE feeds to detect known disclosed vulnerabilities.
4. **License Compliance Verification**: Inspect declared dependency licenses against organizational whitelist policies (e.g. MIT, Apache-2.0, BSD-3-Clause) and flag copyleft licenses (GPL, AGPL) that may pose compliance concerns.
5. **Zero Outdated Packages Policy**: Require automated checks for unmaintained or deprecated upstream packages, generating alerts for dependencies with unresolved security advisories.


### 05 Testing Verification And Ci
# Testing, Verification, and CI Security Standards

1. **Pytest Regression Test Suite**: Maintain a comprehensive test suite in `tests/test_audit.py` with synthetic test files containing known secure and insecure code patterns to ensure 100% detector accuracy and zero regressions.
2. **Zero False Positive Threshold**: Rigorously tune analyzer rules to avoid developer alert fatigue. Every reported finding must have a confidence rating (`HIGH`, `MEDIUM`, `LOW`) and actionable remediation steps.
3. **Automated CI Security Gating**: Integrate the security audit CLI into GitHub Actions and GitLab CI. Set non-zero exit codes on any `HIGH` severity finding to prevent merging vulnerable code.
4. **Supply Chain Hardening**: Lock all tool dependencies via pinned hashes in `requirements.txt`. Execute `gitleaks` and `pip-audit` during development to protect the audit suite itself.
5. **Transpiler Zero-Drift**: Validate that all 6 agent dialects match source rules using `python tools/transpiler.py --check` in continuous integration.


