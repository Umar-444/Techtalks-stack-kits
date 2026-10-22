from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.graph import create_agent_graph

app = FastAPI(
    title="Agentic LangGraph + CrewAI API",
    version="1.0.0",
    description="Production multi-agent execution pipeline with cyclic state verification."
)

class AgentQueryRequest(BaseModel):
    query: str = Field(min_length=3, max_length=500, description="Goal prompt for the agent squad")

class AgentExecutionResponse(BaseModel):
    query: str
    report: str
    iterations: int
    status: str

graph_app = create_agent_graph()

@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "healthy", "service": "agentic-langgraph-crewai", "version": "1.0.0"}

@app.post("/api/v1/run-agent", response_model=AgentExecutionResponse, tags=["Agents"])
async def run_agent_workflow(payload: AgentQueryRequest):
    try:
        initial_state = {
            "query": payload.query,
            "research_notes": [],
            "synthesized_report": "",
            "iteration_count": 0,
            "is_satisfactory": False
        }
        result = graph_app.invoke(initial_state, {"recursion_limit": 25})
        return AgentExecutionResponse(
            query=payload.query,
            report=result.get("synthesized_report", "Execution finished without report"),
            iterations=result.get("iteration_count", 1),
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
