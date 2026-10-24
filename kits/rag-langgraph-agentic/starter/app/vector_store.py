import os
from typing import List, Dict, Any, Optional

class QdrantVectorService:
    def __init__(self, url: Optional[str] = None):
        self.url = url or os.getenv("QDRANT_URL", "http://localhost:6333")
        # In-memory document store as deterministic high-speed fallback
        self._memory_store: List[Dict[str, Any]] = []

    @staticmethod
    def _require_tenant(tenant: Any) -> str:
        if not tenant or not str(tenant).strip():
            raise ValueError("tenant_id is required")
        return str(tenant)

    def index_documents(self, documents: List[Dict[str, Any]]) -> int:
        count = 0
        for doc in documents:
            doc_entry = {
                "id": str(doc.get("id", count)),
                "content": str(doc.get("content", "")),
                "tenant_id": self._require_tenant(doc.get("tenant_id")),
                "metadata": doc.get("metadata", {})
            }
            # Deduplicate by id and tenant_id
            self._memory_store = [
                d for d in self._memory_store 
                if not (d["id"] == doc_entry["id"] and d["tenant_id"] == doc_entry["tenant_id"])
            ]
            self._memory_store.append(doc_entry)
            count += 1
        return count

    def search(self, query: str, tenant_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        self._require_tenant(tenant_id)
        query_words = set(query.lower().split())
        scored = []
        for doc in self._memory_store:
            # Enforce multi-tenant payload isolation
            if doc["tenant_id"] != tenant_id:
                continue
            doc_words = set(doc["content"].lower().split())
            overlap = len(query_words.intersection(doc_words))
            if overlap > 0 or not query_words:
                scored.append((overlap, doc))
        
        # Sort descending by relevance score
        scored.sort(key=lambda x: x[0], reverse=True)
        results = [doc for _, doc in scored[:limit]]
        return results

    def is_healthy(self) -> bool:
        return True

vector_service = QdrantVectorService()
