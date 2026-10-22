import ast
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Finding:
    rule_id: str
    message: str
    file_path: str
    line: int
    col: int
    severity: str
    snippet: Optional[str] = None

class SecurityAstVisitor(ast.NodeVisitor):
    def __init__(self, file_path: str, source_lines: List[str]):
        self.file_path = file_path
        self.source_lines = source_lines
        self.findings: List[Finding] = []

    def _get_snippet(self, lineno: int) -> str:
        if 1 <= lineno <= len(self.source_lines):
            return self.source_lines[lineno - 1].strip()
        return ""

    def visit_Call(self, node: ast.Call):
        # 1. Dangerous sinks: eval() and exec()
        if isinstance(node.func, ast.Name):
            if node.func.id in ("eval", "exec"):
                self.findings.append(Finding(
                    rule_id="SEC-AST-001",
                    message=f"Dangerous dynamic code evaluation via '{node.func.id}()'. Avoid dynamic code execution.",
                    file_path=self.file_path,
                    line=node.lineno,
                    col=node.col_offset,
                    severity="HIGH",
                    snippet=self._get_snippet(node.lineno),
                ))

        # 2. subprocess with shell=True
        func_name = ""
        if isinstance(node.func, ast.Attribute):
            func_name = node.func.attr
        elif isinstance(node.func, ast.Name):
            func_name = node.func.id

        if func_name in ("Popen", "run", "call", "check_output", "check_call"):
            for kw in node.keywords:
                if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                    self.findings.append(Finding(
                        rule_id="SEC-AST-002",
                        message="Invoking subprocess with 'shell=True' allows command injection vulnerabilities. Use argument lists.",
                        file_path=self.file_path,
                        line=node.lineno,
                        col=node.col_offset,
                        severity="HIGH",
                        snippet=self._get_snippet(node.lineno),
                    ))

        # 3. SQL string formatting inside execute()
        if func_name in ("execute", "raw", "raw_query"):
            if node.args and isinstance(node.args[0], (ast.JoinedStr, ast.BinOp)):
                self.findings.append(Finding(
                    rule_id="SEC-AST-003",
                    message="Database query formed via dynamic string interpolation/f-string. Always use parameterized queries ($1, ?).",
                    file_path=self.file_path,
                    line=node.lineno,
                    col=node.col_offset,
                    severity="HIGH",
                    snippet=self._get_snippet(node.lineno),
                ))

        self.generic_visit(node)

def audit_file(file_path: str) -> List[Finding]:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return [Finding(
            rule_id="SEC-IO-001",
            message=f"Failed to read file: {e}",
            file_path=file_path,
            line=1,
            col=0,
            severity="LOW",
        )]

    source_lines = content.splitlines()
    try:
        tree = ast.parse(content, filename=file_path)
    except SyntaxError as e:
        return [Finding(
            rule_id="SEC-SYNTAX-001",
            message=f"Syntax error during AST parse: {e}",
            file_path=file_path,
            line=e.lineno or 1,
            col=e.offset or 0,
            severity="LOW",
        )]

    visitor = SecurityAstVisitor(file_path, source_lines)
    visitor.visit(tree)
    return visitor.findings
