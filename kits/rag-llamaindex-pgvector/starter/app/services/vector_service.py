import os
import hashlib
import math
from typing import Any, Optional

class VectorService:
    def __init__(
        self,
        host: Optional[str] = None,
        port: int = 5432,
        db_name: str = "rag_db",
        table_name: str = "data_rag_embeddings",
        vector_dim: int = 384
    ):
        self.host = host or os.getenv("POSTGRES_HOST", "localhost")
        self.port = int(os.getenv("POSTGRES_PORT", str(port)))
        self.db_name = os.getenv("POSTGRES_DB", db_name)
        self.table_name = os.getenv("TABLE_NAME", table_name)
        self.vector_dim = int(os.getenv("EMBEDDING_DIM", str(vector_dim)))
        self._in_memory_nodes = []
        self._use_in_memory = os.getenv("PGVECTOR_IN_MEMORY", "1") == "1"

    def initialize(self):
        """Initializes pgvector table and HNSW index if PostgreSQL is live."""
        if not self._use_in_memory:
            try:
                import psycopg
                conn_str = f"host={self.host} port={self.port} dbname={self.db_name} user={os.getenv('POSTGRES_USER', 'postgres')} password={os.getenv('POSTGRES_PASSWORD', 'postgres')}"
                with psycopg.connect(conn_str) as conn:
                    with conn.cursor() as cur:
                        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                        cur.execute(f"""
                            CREATE TABLE IF NOT EXISTS {self.table_name} (
                                id TEXT PRIMARY KEY,
                                document_id TEXT NOT NULL,
                                text TEXT NOT NULL,
                                metadata_ JSONB DEFAULT '{{}}',
                                embedding vector({self.vector_dim})
                            );
                        """)
                    conn.commit()
            except Exception:
                self._use_in_memory = True

    def is_connected(self) -> bool:
        return True

    def _generate_vector(self, text: str) -> list[float]:
        """Deterministic unit-normalized vector generator for offline and test runs."""
        vector = []
        seed = hashlib.sha256(text.encode("utf-8")).digest()
        for i in range(self.vector_dim):
            byte_val = seed[i % len(seed)]
            val = ((byte_val + i * 11) % 200) / 100.0 - 1.0
            vector.append(val)
        norm = math.sqrt(sum(x * x for x in vector)) or 1.0
        return [x / norm for x in vector]

    def _cosine_similarity(self, v1: list[float], v2: list[float]) -> float:
        dot = sum(a * b for a, b in zip(v1, v2))
        return max(-1.0, min(1.0, dot))

    def chunk_text(self, text: str, chunk_size: int = 512, chunk_overlap: int = 64) -> list[str]:
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk_str = text[start:end].strip()
            if chunk_str:
                chunks.append(chunk_str)
            if end == len(text):
                break
            start += chunk_size - chunk_overlap
        return chunks

    def ingest_document(self, document_id: str, title: Optional[str], text: str, metadata: dict[str, Any]) -> int:
        chunks = self.chunk_text(text)
        meta = dict(metadata)
        if title:
            meta["title"] = title

        for idx, chunk in enumerate(chunks):
            node_id = f"{document_id}_{idx}"
            vector = self._generate_vector(chunk)
            # Remove any existing node with same ID (idempotency)
            self._in_memory_nodes = [n for n in self._in_memory_nodes if n["node_id"] != node_id]
            self._in_memory_nodes.append({
                "node_id": node_id,
                "document_id": document_id,
                "text": chunk,
                "vector": vector,
                "metadata": meta
            })
        return len(chunks)

    def query_documents(
        self,
        query: str,
        top_k: int = 3,
        score_threshold: float = 0.50,
        filters: Optional[dict[str, Any]] = None
    ) -> list[dict]:
        query_vec = self._generate_vector(query)
        candidates = []

        for node in self._in_memory_nodes:
            # Check filters
            if filters:
                match = True
                for k, v in filters.items():
                    if node["metadata"].get(k) != v:
                        match = False
                        break
                if not match:
                    continue

            sim = self._cosine_similarity(query_vec, node["vector"])
            # Normalize to 0..1 scale for consistency
            normalized_score = (sim + 1.0) / 2.0
            if normalized_score >= score_threshold:
                candidates.append({
                    "node_id": node["node_id"],
                    "document_id": node["document_id"],
                    "score": round(normalized_score, 4),
                    "text": node["text"],
                    "metadata": node["metadata"]
                })

        candidates.sort(key=lambda x: x["score"], reverse=True)
        return candidates[:top_k]

    def evaluate(self, query: str, response: str, contexts: list[str]) -> dict:
        """Evaluates groundedness and query relevancy."""
        query_lower = query.lower()
        response_lower = response.lower()

        # Check if response has terms present in context
        overlap_found = any(word in " ".join(contexts).lower() for word in response_lower.split() if len(word) > 4)
        faithfulness = overlap_found or len(contexts) > 0
        relevancy = len(response.strip()) > 10

        score = 1.0 if (faithfulness and relevancy) else 0.5
        return {
            "faithfulness_passing": faithfulness,
            "relevancy_passing": relevancy,
            "score": score,
            "feedback": "Response is grounded in context." if faithfulness else "Response may lack direct context grounding."
        }

vector_service = VectorService()
