---
name: first-feature
description: Author a custom AST security detector to identify dangerous string concatenation in database queries.
---

# First Feature: Authoring an AST SQL Injection Detector

## Step 1: Subclass `ast.NodeVisitor`
In `analyzers/rules/sql_injection.py`:
```python
import ast
from dataclasses import dataclass
from typing import List

@dataclass
class Finding:
    rule_id: str
    message: str
    line: int
    col: int
    severity: str

class SqlInjectionVisitor(ast.NodeVisitor):
    def __init__(self, filename: str):
        self.filename = filename
        self.findings: List[Finding] = []

    def visit_Call(self, node: ast.Call):
        # Look for calls to .execute() or .raw()
        func_name = ""
        if isinstance(node.func, ast.Attribute):
            func_name = node.func.attr
        elif isinstance(node.func, ast.Name):
            func_name = node.func.id

        if func_name in ("execute", "raw", "raw_query"):
            if node.args and isinstance(node.args[0], (ast.JoinedStr, ast.BinOp)):
                self.findings.append(Finding(
                    rule_id="SEC-SQL-001",
                    message="Detected dynamic string concatenation/f-string in database query execute call. Use parameterized queries.",
                    line=node.lineno,
                    col=node.col_offset,
                    severity="HIGH"
                ))
        self.generic_visit(node)
```

## Step 2: Register Detector with Analyzer
In `analyzers/ast_analyzer.py`:
```python
def audit_source_file(filepath: str) -> list[Finding]:
    with open(filepath, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=filepath)
    visitor = SqlInjectionVisitor(filepath)
    visitor.visit(tree)
    return visitor.findings
```
