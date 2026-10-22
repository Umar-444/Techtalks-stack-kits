# FastAPI Architecture, LlamaIndex Settings & Async Lifespan

# Rule 1: FastAPI Architecture, LlamaIndex Settings & Async Lifespan

## Context & Principles
- Pair FastAPI 0.115+ with LlamaIndex 0.11+ using global `Settings` configuration rather than legacy `ServiceContext`.
- Manage persistent database connection pools and embedding models via FastAPI's `@asynccontextmanager` lifespan handler.
- Expose typed asynchronous REST endpoints backed by Pydantic v2 schemas and structured exception handlers.

## Standards
1. **Global LlamaIndex Configuration**:
   ```python
   from llama_index.core import Settings
   from llama_index.embeddings.fastembed import FastEmbedEmbedding

   Settings.embed_model = FastEmbedEmbedding(model_name="BAAI/bge-small-en-v1.5")
   Settings.chunk_size = 512
   Settings.chunk_overlap = 64
   ```
2. **Lifespan Management**:
   ```python
   @asynccontextmanager
   async def lifespan(app: FastAPI):
       await vector_service.initialize()
       yield
       await vector_service.close()
   ```
3. **Pydantic Validation**: All request and response payloads must subclass `pydantic.BaseModel` with explicit constraints (`Field(min_length=1, max_length=10000)`).
4. **Health Probe**: Provide a non-blocking `/healthz` endpoint verifying application health and PostgreSQL pgvector connectivity.
