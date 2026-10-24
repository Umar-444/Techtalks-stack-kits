import os
from typing import List, Dict, Any, Optional

# Hybrid candidates whose fused score falls below this are rejected.
MIN_FUSED_SCORE = 0.40


class WeaviateVectorService:
    def __init__(self, url: Optional[str] = None):
        self.url = url or os.getenv("WEAVIATE_URL", "http://localhost:8085")
        # In-memory document storage for high-speed, zero-dependency testing
        self._memory_store: List[Dict[str, Any]] = []

    @staticmethod
    def _require_tenant(doc: Dict[str, Any]) -> str:
        tenant = doc.get("tenant_id")
        if not tenant or not str(tenant).strip():
            raise ValueError("every indexed document needs a tenant_id")
        return str(tenant)

    def index_documents(self, documents: List[Dict[str, Any]]) -> int:
        count = 0
        for doc in documents:
            entry = {
                "id": str(doc.get("id", count)),
                "content": str(doc.get("content", "")),
                "tenant_id": self._require_tenant(doc),
                "metadata": doc.get("metadata", {})
            }
            # Deduplicate by id and tenant_id
            self._memory_store = [
                d for d in self._memory_store 
                if not (d["id"] == entry["id"] and d["tenant_id"] == entry["tenant_id"])
            ]
            self._memory_store.append(entry)
            count += 1
        return count

    def hybrid_search(self, query: str, tenant_id: str, alpha: float = 0.65, limit: int = 5, min_score: float = MIN_FUSED_SCORE) -> List[Dict[str, Any]]:
        if not tenant_id:
            raise ValueError("tenant_id is required for every search")
        query_words = set(query.lower().split())
        scored = []
        for doc in self._memory_store:
            # Enforce strict multi-tenant partition
            if doc["tenant_id"] != tenant_id:
                continue
            doc_words = set(doc["content"].lower().split())
            bm25_sparse = len(query_words.intersection(doc_words)) / max(1, len(query_words))
            dense_semantic = 1.0 if bm25_sparse > 0 else 0.0
            
            # Hybrid fused score: (1 - alpha) * sparse + alpha * dense
            fused_score = ((1.0 - alpha) * bm25_sparse) + (alpha * dense_semantic)
            if fused_score >= min_score:
                scored.append((fused_score, doc))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [d for _, d in scored[:limit]]

    def is_healthy(self) -> bool:
        return True

weaviate_service = WeaviateVectorService()
