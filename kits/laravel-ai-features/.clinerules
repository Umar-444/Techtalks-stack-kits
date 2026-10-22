# Laravel 12/13 + AI Features (LLM Orchestration, Embeddings & RAG) — Agent Operating Rules (AGENTS.md)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Table of Contents
- [Framework and AI Architecture Conventions](#01-framework-and-ai-conventions)
- [Structured Output and Tool Calling Standards](#02-llm-structured-output-and-tools)
- [pgvector Embeddings and RAG Architecture](#03-pgvector-embeddings-and-rag)
- [AI Security Guardrails and Sanitization](#04-security-guardrails-and-sanitization)
- [Testing Verification and CI Standards](#05-testing-verification-and-ci)

---

<a id="01-framework-and-ai-conventions"></a>
## Framework and AI Architecture Conventions

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

---

<a id="02-llm-structured-output-and-tools"></a>
## Structured Output and Tool Calling Standards

# Structured Output and Tool Calling Standards

## 1. JSON Schema Enforcement
- Always pass explicit JSON schemas using `response_format` or structured output APIs.
- Validate parsed JSON using Laravel `Validator::make($data, $rules)->validate()`.
- Implement fallback retry mechanisms if the model returns malformed JSON.

## 2. Tool / Function Calling Protocol
- Implement each tool as an isolated class implementing `AiToolInterface`.
- Verify user authorization inside tool execution methods before mutating state.
- Sanitize tool arguments to prevent argument injection attacks.

---

<a id="03-pgvector-embeddings-and-rag"></a>
## pgvector Embeddings and RAG Architecture

# pgvector Embeddings and RAG Architecture

## 1. Database Migrations with pgvector
- Always check and activate extension: `CREATE EXTENSION IF NOT EXISTS vector;`.
- Define vector columns explicitly: `$table->vector('embedding', 1536);`.
- Create HNSW index for sub-linear search:
  ```sql
  CREATE INDEX documents_embedding_hnsw_idx ON documents USING hnsw (embedding vector_cosine_ops);
  ```

## 2. Parameterized Cosine Queries
- Execute semantic search using the `<=>` cosine distance operator:
  ```php
  $query->orderByRaw('embedding <=> ?', [json_encode($embedding)])
        ->where('tenant_id', $tenantId)
        ->limit($limit);
  ```

---

<a id="04-security-guardrails-and-sanitization"></a>
## AI Security Guardrails and Sanitization

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

---

<a id="05-testing-verification-and-ci"></a>
## Testing Verification and CI Standards

# Testing Verification and CI Standards

## 1. Mocking AI Providers
- Never make outbound HTTP requests to paid APIs during automated tests.
- Use `MockAiProvider` returning deterministic responses for feature tests.

## 2. Pest Feature Assertions
- Assert that prompt injection attempts trigger `SecurityException`.
- Assert that cosine similarity correctly ranks relevant documents highest.

## 3. CI Pipeline
- Every commit must pass Pest test suite, Gitleaks, and Semgrep SAST scans.

---

