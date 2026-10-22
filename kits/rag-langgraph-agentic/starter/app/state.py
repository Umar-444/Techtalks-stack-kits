from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    question: str
    tenant_id: str
    documents: List[Dict[str, Any]]
    generation: str
    iterations: int
    max_iterations: int
    groundedness_score: float
    status: str
