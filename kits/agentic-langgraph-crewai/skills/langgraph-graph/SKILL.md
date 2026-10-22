---
name: langgraph-graph
description: Scaffold and compile cyclic StateGraph workflows with TypedDict state schemas.
---
# LangGraph Workflow Skill

## Usage
1. Define state schema in pp/state.py.
2. Implement workflow nodes in pp/graph.py.
3. Add conditional edge router function.
4. Compile graph with checkpointer.

`python
from langgraph.graph import StateGraph, END
from app.state import AgentState

workflow = StateGraph(AgentState)
workflow.add_node("researcher", research_node)
workflow.add_node("reviewer", review_node)
workflow.add_conditional_edges("researcher", router_fn, {"continue": "reviewer", "end": END})
`
