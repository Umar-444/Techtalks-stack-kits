import httpx
import chromadb

class LocalPrivateRAG:
    def __init__(self, ollama_url: str = "http://localhost:11434", collection_name: str = "private_knowledge"):
        self.ollama_url = ollama_url
        self.chroma_client = chromadb.PersistentClient(path="./local_chroma_data")
        self.collection = self.chroma_client.get_or_create_collection(name=collection_name)

    async def generate_response(self, prompt: str, model: str = "llama3.2") -> str:
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                f"{self.ollama_url}/api/generate",
                json={"model": model, "prompt": prompt, "stream": False}
            )
            return resp.json().get("response", "")
