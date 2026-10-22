# Step-by-Step Agent Build Guide

### Step 1: Environment & API Key Configuration
- Action: Copy `.env.example` to `.env` and set `AI_PROVIDER=mock` or valid API key.
- Command: `php artisan key:generate --ansi`
- Verification: `.env` contains valid `APP_KEY=base64:...`

### Step 2: PostgreSQL pgvector Extension & Migration Setup
- Action: Run database migrations creating vector extension, document table, and HNSW index.
- Command: `php artisan migrate --force`
- Verification: `SELECT * FROM pg_extension WHERE extname = 'vector';` returns 1 row.

### Step 3: Embeddings Service & Chunking Pipeline Verification
- Action: Test embedding generation service against sample text chunks.
- Command: `php artisan test --filter=VectorSearchTest`
- Verification: Cosine similarity returns score between 0.0 and 1.0.

### Step 4: Structured Output LLM Synthesis
- Action: Execute AI service structured extraction with strict JSON schema.
- Command: `php artisan test --filter=AiServiceTest`
- Verification: Output parses to typed PHP DTO.

### Step 5: Prompt Injection & Guardrail Assertion
- Action: Test adversarial prompts against injection screening filter.
- Command: `php artisan test --filter=test_it_blocks_prompt_injection`
- Verification: Injection attempts trigger `SecurityException` and return safe refusal.

### Step 6: Architecture & Static Security Scan
- Action: Execute Pest architecture tests and Semgrep scan.
- Command: `php artisan test --filter=ArchTest && semgrep scan`
- Verification: 0 violations, 0 SAST findings.
