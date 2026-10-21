---
title: "NoSQL Security & Injection Defense"
description: "Preventing operator injection, $where execution, and unauthorized collection access."
globs: ["app/**/*.php"]
---

# NoSQL Security & Injection Defense

1. **Operator Injection Defense:**
   - Never pass unfiltered `$request->all()` into `where()` clauses.
   - MongoDB interprets array inputs as operators (e.g. `['$gt' => '']`). Cast all inputs to scalar types.

2. **Prohibited Features:**
   - Usage of `$where` with JavaScript execution is strictly prohibited.
