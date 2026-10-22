---
name: llm-structured-output
description: Orchestrate LLMs with strict JSON Schema output enforcement, fallback retries, and typed DTO parsing.
---

# Skill: LLM Structured Output

## Workflow
1. Define JSON Schema in `AiService`.
2. Request structured completion:
```php
$response = $aiService->structuredCompletion($prompt, $schema);
```
3. Hydrate into typed DTO.

## Done Means
- Schema validated with 0 type coercion failures.
