---
id: ragas-groundedness-and-hallucination-evals
title: Ragas Groundedness & Hallucination Evals
globs: "**/*.py"
alwaysApply: true
---
# Ragas Groundedness Scoring & Hallucination Detection

## 1. Ragas Metric Triad
- Implement continuous scoring across three core Ragas metrics:
  1. **Faithfulness**: Are claims in the generated answer strictly derived from retrieved context?
  2. **Answer Relevance**: Does the generated answer directly address the user's inquiry?
  3. **Context Precision**: Did the retriever rank the most relevant chunks at the top?

## 2. Automated Self-Correction Loop
- The generation grader node inspects the generated output against the retrieved chunks:
  ```python
  def grade_generation(state: GraphState) -> str:
      if not verify_groundedness(state["generation"], state["documents"]):
          return "hallucination_detected"
      return "grounded"
  ```
- If hallucination is detected and iterations remain, route back to `generate` with a prompt warning: "Your previous answer included facts not supported by the context. Re-synthesize strictly using provided documents."
