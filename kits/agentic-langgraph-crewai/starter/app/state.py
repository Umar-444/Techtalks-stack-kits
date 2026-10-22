from typing import TypedDict, List, Annotated
import operator

class AgentState(TypedDict):
    """Immutable state schema passed between LangGraph nodes."""
    query: str
    research_notes: Annotated[List[str], operator.add]
    synthesized_report: str
    iteration_count: int
    is_satisfactory: bool
