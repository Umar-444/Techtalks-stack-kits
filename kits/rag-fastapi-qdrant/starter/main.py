from fastapi import FastAPI
app = FastAPI(title="Qdrant RAG Service")
@app.get("/health")
def health():
    return {"status": "ok", "vector_db": "qdrant"}
