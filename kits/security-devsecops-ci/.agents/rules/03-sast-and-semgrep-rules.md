# Static Application Security Testing (SAST) and Custom Semgrep Rules

# Static Application Security Testing (SAST) and Custom Semgrep Rules

## 1. AST Analysis over Regex
- Use Semgrep AST semantic pattern matching rather than brittle string regex:
  ```yaml
  rules:
    - id: unescaped-sql-query
      patterns:
        - pattern: "$DB.execute($QUERY)"
        - pattern-inside: |
            $QUERY = ... + ...
            ...
      message: "Detected potential SQL injection via string concatenation into database query."
      languages: [python, javascript]
      severity: ERROR
  ```

## 2. Taint Mode Tracking
- Trace unvalidated user input sources (`request.args`, `params[]`) into dangerous execution sinks (`exec`, `system`, SQL queries).
- Enforce sanitizers or type casting before data reaches external sinks.

## 3. False Positive Mitigation
- When an alert is an intentional, hardened pattern, use inline suppression:
  `# nosemgrep: custom-rule-id -- Reason: Input validated by upstream middleware`
- Review all inline suppressions periodically during security retrospectives.
