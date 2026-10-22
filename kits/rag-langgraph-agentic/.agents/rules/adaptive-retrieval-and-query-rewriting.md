# Adaptive Retrieval & Query Rewriting

# Adaptive Retrieval, Self-RAG & Query Rewriting

## 1. Document Relevance Grading
- Use a fast, specialized prompt or compact LLM to binary-grade document relevance:
  - Output strictly `{"score": "yes"}` or `{"score": "no"}` using structured schemas.
  - Filter out noisy or irrelevant chunks before context injection to minimize hallucination risk.

## 2. Query Transformation Logic
- When retrieved documents do not address the core query, the rewrite node inspects the original question and prior search failures:
  ```python
  def rewrite_query(state: GraphState) -> dict:
      better_question = transform_query_with_llm(state["question"])
      return {
          "question": better_question,
          "iteration_count": state["iteration_count"] + 1
      }
  ```
- Strips conversational fillers, expands domain-specific acronyms, and generates alternative keyword combinations.
