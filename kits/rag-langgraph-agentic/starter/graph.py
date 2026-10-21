from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    question: str
    documents: list[str]
    generation: str
    iterations: int

def retrieve_node(state: AgentState) -> AgentState:
    state["documents"] = ["Retrieved context matching query"]
    return state

def generate_node(state: AgentState) -> AgentState:
    state["generation"] = f"Answer grounded in {len(state['documents'])} documents"
    return state

builder = StateGraph(AgentState)
builder.add_node("retrieve", retrieve_node)
builder.add_node("generate", generate_node)
builder.set_entry_point("retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", END)
agent_graph = builder.compile()
