import pytest
from app.graph import create_agent_graph

def test_graph_execution_terminates():
    graph = create_agent_graph()
    initial_state = {
        "query": "Evaluate cloud security architecture",
        "research_notes": [],
        "synthesized_report": "",
        "iteration_count": 0,
        "is_satisfactory": False
    }
    result = graph.invoke(initial_state, {"recursion_limit": 10})
    assert "Synthesized Intelligence Report" in result["synthesized_report"]
    assert result["iteration_count"] >= 1
    assert result["is_satisfactory"] is True
