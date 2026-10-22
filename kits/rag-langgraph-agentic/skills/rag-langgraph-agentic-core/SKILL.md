---
name: rag-langgraph-agentic-core
description: Core operational workflows, cyclic graphs, Qdrant payload indexing, and Token-Light evaluation for LangGraph + LangChain + Qdrant + Ragas.
---
# LangGraph + Qdrant + Ragas Agentic RAG Core Skill

## 1. Architecture Overview
This kit provides a production-grade cyclical state machine for agentic retrieval-augmented generation. Instead of naive linear RAG (retrieve -> prompt -> generate), the LangGraph engine dynamically evaluates document relevance, executes query reformulation cycles, enforces tenant payload isolation in Qdrant, and runs Ragas groundedness audits before returning responses.

```
[Start] --> [retrieve_node] 
                 |
                 v
        [grade_documents_node]
           /                (relevant)                 (not relevant & iter < max)
       v                            v
[generate_node]             [rewrite_query_node]
       |                            |
       v                            +--> [retrieve_node]
[eval_groundedness_node]
   /               (pass >= 0.85)     (fail < 0.85 & iter < max)
   v                       v
 [END]              [rewrite_query_node]
```

## 2. Cyclic State Machine (AgentState)
The core state dictionary is typed and immutable per node transition:
```python
class AgentState(TypedDict):
    question: str
    documents: list[dict]
    generation: str
    iterations: int
    max_iterations: int
    groundedness_score: float
    tenant_id: str
    status: str
```

## 3. Node Responsibilities
1. **`retrieve_node`**: Executes payload-filtered search against Qdrant vector database (`tenant_id`, `access_tier`, `created_at`).
2. **`grade_documents_node`**: Assesses keyword overlap and semantic relevance of retrieved chunks.
3. **`rewrite_query_node`**: Reformulates the input question into targeted semantic search vectors, stripping colloquialisms.
4. **`generate_node`**: Produces a structured synthesis strictly conditioned on approved documents.
5. **`eval_groundedness_node`**: Runs Ragas evaluation metric to detect hallucinated statements.

## 4. Verification Workflow
```bash
# Unit & integration tests
pytest starter/tests/test_agentic_rag.py -v

# Verification of cyclical recursion limit
pytest starter/tests/test_agentic_rag.py -k test_graph_recursion_limit
```

## 5. Done Means
- Graph executes cycles up to `max_iterations` without unhandled recursion errors.
- Document filtering isolates multi-tenant data in Qdrant payloads.
- All endpoints conform to FastAPI OpenAPI schemas with strict CORS and non-root execution.
