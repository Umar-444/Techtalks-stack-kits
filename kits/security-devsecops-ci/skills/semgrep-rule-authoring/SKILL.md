---
name: semgrep-rule-authoring
description: Advanced AST pattern matching, taint tracking, and metavariable regex tuning with Semgrep.
---

# Semgrep Rule Authoring Skill

## Overview
Author high-precision static analysis rules using abstract syntax tree (AST) matching, taint mode, and metavariables.

## Core Patterns

### 1. Generic Pattern Syntax
- `...` (Ellipsis): Matches zero or more arguments, statements, or expressions.
- `$VAR` (Metavariable): Binds to any atomic AST element (variable, function, class name).

### 2. Taint Mode
Trace data from untrusted sources to sensitive sinks:
```yaml
rules:
  - id: sql-injection-taint
    mode: taint
    pattern-sources:
      - pattern: request.args.get(...)
      - pattern: request.form[...]
    pattern-sinks:
      - pattern: db.session.execute(...)
    pattern-sanitizers:
      - pattern: int(...)
    message: "Unsanitized user input flowed into SQL query execution."
    languages: [python]
    severity: ERROR
```
