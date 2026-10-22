---
name: ast-security-rule-authoring
description: Deep dive into writing semantic AST visitors for dangerous functions (eval, exec, subprocess, yaml.load).
---

# AST Security Rule Authoring & Pattern Matching

## Detecting Dangerous Execution Sinks
The AST visitor pattern allows inspecting Python syntax trees safely without runtime execution:

```python
import ast

class DangerousSinkVisitor(ast.NodeVisitor):
    DANGEROUS_FUNCS = {"eval", "exec"}

    def __init__(self):
        self.issues = []

    def visit_Call(self, node: ast.Call):
        # Check direct calls like eval(user_input)
        if isinstance(node.func, ast.Name) and node.func.id in self.DANGEROUS_FUNCS:
            self.issues.append({
                "rule": "DANGEROUS_EVAL",
                "line": node.lineno,
                "msg": f"Call to dangerous sink {node.func.id}() detected."
            })

        # Check subprocess.Popen(..., shell=True)
        if isinstance(node.func, ast.Attribute) and node.func.attr in ("Popen", "run", "call"):
            for kw in node.keywords:
                if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                    self.issues.append({
                        "rule": "SHELL_TRUE",
                        "line": node.lineno,
                        "msg": "subprocess call with shell=True detected."
                    })
        self.generic_visit(node)
```
