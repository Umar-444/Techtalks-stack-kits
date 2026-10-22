from langgraph.graph import StateGraph, END
from app.state import AgentState
from app.tools import sandboxed_search

def research_node(state: AgentState) -> dict:
    query = state.get("query", "")
    info = sandboxed_search(query)
    current_iter = state.get("iteration_count", 0) + 1
    return {
        "research_notes": [info],
        "iteration_count": current_iter
    }

def synthesis_node(state: AgentState) -> dict:
    notes = state.get("research_notes", [])
    report = "Synthesized Intelligence Report:\n" + "\n".join(f"- {note}" for note in notes)
    return {
        "synthesized_report": report,
        "is_satisfactory": True
    }

def router_condition(state: AgentState) -> str:
    if state.get("iteration_count", 0) >= 3 or state.get("is_satisfactory", False):
        return "end"
    return "synthesize"

def create_agent_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("research", research_node)
    workflow.add_node("synthesize", synthesis_node)
    
    workflow.set_entry_point("research")
    workflow.add_conditional_edges(
        "research",
        router_condition,
        {"synthesize": "synthesize", "end": END}
    )
    workflow.add_edge("synthesize", END)
    
    return workflow.compile()
