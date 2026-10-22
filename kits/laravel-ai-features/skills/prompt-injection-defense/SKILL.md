---
name: prompt-injection-defense
description: Implement multi-layered prompt injection screening, delimiter bounding, and canary token leak detectors.
---

# Skill: Prompt Injection Defense

## Workflow
1. Intercept prompt in `AiGuardrailService`.
2. Check regex patterns for override instructions.
3. Wrap input in `<user_content>` delimiters.
4. Inject canary token and assert absence in response.

## Done Means
- Malicious prompts blocked with `SecurityException`.
