---
name: rag-haystack-weaviate-core
description: Core operational workflows, DAG pipeline inspection, Weaviate hybrid vector storage, and automated evaluation.
---
# Haystack Pipelines + Weaviate Core Skill

## 1. Architecture Overview
This kit provides an inspectable, deterministic production RAG platform combining Deepset Haystack 2.5+ with Weaviate vector database. Rather than opaque agent loops, execution is defined as an explicit Directed Acyclic Graph (DAG) with full component introspection and built-in faithfulness evaluators.

```
[User Request] 
      |
      v
[FastAPI /api/v1/rag/query]
      |
      v
[Haystack Pipeline DAG]
      +--> [WeaviateHybridRetriever] (BM25 + Dense, alpha=0.65)
      |          |
      |          v
      +--> [PromptBuilder] (Jinja2 context injection)
                 |
                 v
           [Generator] (OpenAI / Ollama / Local Fallback)
                 |
                 v
           [FaithfulnessEvaluator] (Groundedness check >= 0.85)
                 |
                 v
           [QueryResponse JSON]
```

## 2. Core Service Components
- **`WeaviateService`**: Manages v4 client connection, collection schema creation, multi-tenant scoping, and in-memory test fallback.
- **`HaystackRAGPipeline`**: Manages DAG lifecycle, component connections, and execution profiling.
- **`FaithfulnessEvaluator`**: Validates generated claims against retrieved context to prevent hallucinations.

## 3. Verification Commands
```bash
# Run complete test suite
pytest starter/tests/test_haystack_rag.py -v

# Verify hybrid search recall
pytest starter/tests/test_haystack_rag.py -k test_weaviate_hybrid_search
```

## 4. Done Means
- DAG executes cleanly with zero unhandled pipeline graph errors.
- Weaviate searches isolate multi-tenant document partitions.
- Output adheres to strict OpenAPI specifications with non-root Docker security.
