---
name: first-feature
description: Guide to adding a custom query rewriter node, web search fallback, or domain classifier to the LangGraph state machine.
---
# First Feature Skill: Adding a Query Rewrite Node to LangGraph

## 1. Implement Query Transformation Logic
In `app/graph.py`:
```python
def rewrite_query(state: GraphState) -> dict:
    original = state["question"]
    # Strip fillers and produce search keywords
    transformed = f"Detailed technical explanation of: {original}"
    return {
        "question": transformed,
        "iteration_count": state["iteration_count"] + 1
    }
```

## 2. Connect the Conditional Edge
```python
workflow.add_node("rewrite_query", rewrite_query)
workflow.add_edge("rewrite_query", "retrieve")

def decide_to_generate(state: GraphState):
    if not state["documents"]:
        if state["iteration_count"] >= 3:
            return "generate" # Terminate rewrite loop
        return "rewrite_query"
    return "generate"

workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {"rewrite_query": "rewrite_query", "generate": "generate"}
)
```
