# 05 Security Guardrails And Testing

# Rule 5: Security Guardrails, Prompt Injection Defense & In-Memory Testing

## Context & Principles
- RAG applications are susceptible to indirect prompt injection through ingested untrusted documents.
- Isolate system instructions from retrieved context using strict delimiters (`<context>...</context>`).
- Enforce automated unit and integration tests using Qdrant's embedded in-memory mode (`QdrantClient(":memory:")`), eliminating the need for an external database during local test execution.

## Standards
1. **Delimited Context Formatting**:
   ```python
   prompt = f"""You are a helpful assistant. Answer the user query using ONLY the provided context. If the answer cannot be found in the context, say 'I cannot find that in the documentation.'
   
   <context>
   {assembled_context}
   </context>
   
   User Question: {user_query}"""
   ```
2. **Untrusted Payload Sanitization**: Strip dangerous control characters and markdown injection tokens from user documents prior to embedding generation.
3. **In-Memory Testing Harness**:
   ```python
   @pytest.fixture
   def in_memory_client():
       return QdrantClient(":memory:")
   ```
4. **Secret Scanning**: Never hardcode API keys or vector database passwords. Validate that environment variables are non-empty during startup using Pydantic `BaseSettings`.

