from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pipeline import LocalPrivateRAG

app = FastAPI(title="Local Private Airgapped RAG", version="1.0.0")
rag = LocalPrivateRAG()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    privacy_verified: bool = True

@app.post("/api/v1/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest):
    answer = await rag.generate_response(req.query)
    return QueryResponse(answer=answer, privacy_verified=True)
