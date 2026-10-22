# 02 Ast Static Analysis And Pattern Matching

﻿# AST Static Analysis and Semantic Pattern Matching

1. **Python AST NodeVisitor Pattern**: Author code vulnerability analyzers by subclassing `ast.NodeVisitor`. Traverse code syntax trees to locate dangerous functions, unsafe sinks, and insecure coding anti-patterns without executing untrusted code.
2. **Dangerous Sink Detection**: Enforce checks that flag invocations of dangerous dynamic evaluation functions (`eval`, `exec`, `subprocess.Popen(..., shell=True)`, `os.system`) where arguments are not static literals.
3. **SQL Injection String Interpolation**: Inspect database query calls to verify that arguments are not formed via f-strings, `format()`, or `%` modulo concatenation. Require bound parameterized queries across all database drivers.
4. **Hardcoded Secrets Detection**: Scan string literals using entropy analysis (Shannon entropy > 4.5) and regex heuristics to detect hardcoded API keys, JWT tokens, AWS access credentials, and private keys.
5. **Precise AST Source Mapping**: Every AST finding must report the exact file path, starting line number, column offset, and offending source code snippet to facilitate automated remediation.

