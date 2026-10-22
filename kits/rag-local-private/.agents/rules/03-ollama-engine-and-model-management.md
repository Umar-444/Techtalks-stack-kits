# Ollama Local LLM Engine & Model Management

# 03 - Ollama Local LLM Engine & Model Management

## 1. Engine Integration & Async HTTP
- **Client Protocol:** Communicate with Ollama via asynchronous HTTP client (`httpx.AsyncClient`) targeting `http://localhost:11434` or Docker container service `http://ollama:11434`.
- **Reuse Persistent Client:** Never instantiate a new `AsyncClient` on every request. Maintain a single client instance within the FastAPI application lifespan or service singleton to enable HTTP connection pooling and keepalive sockets.
- **Configurable Timeouts:** Local LLM generation can experience prompt-processing latency depending on context size and GPU hardware. Set default client timeouts to `60.0s` for generation and `15.0s` for embeddings.

## 2. Model Selection & Quantization Guidelines
- **Generation LLMs:**
  - `llama3.2:3b` / `llama3.2:1b`: Recommended for lightweight edge/CPU deployment (4GB - 8GB system RAM).
  - `qwen2.5:7b` / `mistral:7b`: Recommended for enterprise reasoning and complex multilingual (Arabic & English) retrieval (16GB RAM or 8GB VRAM).
- **Embedding Models:**
  - `nomic-embed-text`: 8192 token context window, 768-dimensional dense vectors, optimized for local RAG retrieval.
  - Prefix invariant: Follow Nomic standards by prefixing documents with `search_document: ` and query strings with `search_query: ` for maximum retrieval accuracy.

## 3. Streaming & Non-Streaming Generation
- **Non-Streaming Endpoint:**
  ```python
  resp = await client.post(
      f"{self.ollama_url}/api/generate",
      json={
          "model": self.model_name,
          "prompt": formatted_prompt,
          "stream": False,
          "options": {
              "temperature": 0.1,
              "top_p": 0.9,
              "num_ctx": 4096
          }
      }
  )
  ```
- **Temperature Rule:** Set `temperature: 0.1` for RAG workloads. Grounded factual question-answering requires deterministic output to minimize hallucination.
- **Context Window Invariant:** Explicitly configure `num_ctx: 4096` to prevent silent prompt truncation when injecting multi-chunk document contexts.

## 4. Cold-Start & In-Memory Test Mode Fallback
- In CI/CD pipelines and automated testing where Ollama daemon is not running, the vector service must activate `TEST_MODE=true`.
- In test mode, embedding generation produces deterministic normalized synthetic vectors (e.g. 384-dimensional unit vectors) and generation returns deterministic grounded responses based on context tokens. This ensures all tests and CI checks pass reliably in headless runners without requiring a GPU or running Ollama daemon.
