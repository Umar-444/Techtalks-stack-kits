from fastapi import FastAPI
app = FastAPI(title="Agentic CrewAI LangGraph")
@app.get("/health")
def health():
    return {"status": "ok", "multi_agent": True}
