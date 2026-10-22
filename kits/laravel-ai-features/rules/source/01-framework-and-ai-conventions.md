---
id: 01-framework-and-ai-conventions
title: Framework and AI Architecture Conventions
description: Architecture standards for Laravel 12/13 AI integrations.
globs: ["app/**/*.php", "config/**/*.php"]
alwaysApply: true
---

# Framework and AI Architecture Conventions

## 1. Strict Typing and Contracts
- Always declare `declare(strict_types=1);` at the top of every PHP file.
- Code against abstract contracts (`AiServiceInterface`, `EmbeddingServiceInterface`) to enable swapping providers and mock testing.
- Return explicit types and typed DTOs from all service methods.

## 2. Directory Layout
- **AI Services**: `app/Services/Ai/` (LLM communication, prompt builders, tool executors).
- **Embeddings**: `app/Services/Embeddings/` (text chunking, vector generation).
- **DTOs**: `app/DTOs/` (typed request and response structures).
- **Jobs**: `app/Jobs/` (asynchronous embedding generation and index updates).

## 3. Never-List
- Never make synchronous LLM API calls during user-facing write mutations; dispatch to Redis queues.
- Never hardcode model names or API credentials in service code; read from `config/ai.php`.
- Never trust raw LLM output without validating against a typed schema.
