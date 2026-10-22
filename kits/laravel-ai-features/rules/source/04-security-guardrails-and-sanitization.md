---
id: 04-security-guardrails-and-sanitization
title: AI Security Guardrails and Sanitization
description: Defenses against prompt injection, canary leaks, and denial-of-wallet.
globs: ["app/Services/Ai/**/*.php", "app/Http/Controllers/**/*.php"]
alwaysApply: true
---

# AI Security Guardrails and Sanitization

## 1. Prompt Injection Defense
- Screen incoming user prompts against adversarial patterns:
  - System prompt overrides (`Ignore previous instructions`, `You are now DAN`).
  - Base64 / Unicode obfuscation attempts.
- Enclose untrusted inputs within strict boundary delimiters: `<user_input>...</user_input>`.

## 2. Token Budgeting & Rate Limiting
- Enforce per-user sliding window limits on AI endpoints: 10 requests / minute.
- Cap completion tokens (`max_tokens`) on every call to prevent runaway generation.

## 3. Output Sanitization
- Escape AI-generated text before rendering in Blade or HTML responses to prevent stored XSS.
