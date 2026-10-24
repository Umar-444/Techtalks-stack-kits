import os
import re
import hashlib
import math
from typing import Any, Optional

IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]{0,47}$")
FAITHFULNESS_THRESHOLD = 0.8

class VectorService:
    def __init__(
        self,
        host: Optional[str] = None,
        port: int = 5432,
        db_name: str = "rag_db",
        table_name: str = "data_rag_embeddings",
        vector_dim: int = 384
    ):
        if not IDENTIFIER_RE.match(os.getenv("TABLE_NAME", table_name)):
            raise ValueError("TABLE_NAME must be a plain SQL identifier ([A-Za-z_][A-Za-z0-9_]{0,47})")
        self.host = host or os.getenv("POSTGRES_HOST", "localhost")
        self.port = int(os.getenv("POSTGRES_PORT", str(port)))
        self.db_name = os.getenv("POSTGRES_DB", db_name)
        self.table_name = os.getenv("TABLE_NAME", table_name)
        self.vector_dim = int(os.getenv("EMBEDDING_DIM", str(vector_dim)))
        self._in_memory_nodes = []
        self._use_in_memory = os.getenv("PGVECTOR_IN_MEMORY", "1") == "1"

    def schema_statements(self) -> list[str]:
        """DDL for the table, HNSW cosine index and metadata GIN index.

        Only the validated identifier and an integer dimension are interpolated;
        no request data ever reaches this SQL.
        """
        t = self.table_name
        return [
            "CREATE EXTENSION IF NOT EXISTS vector;",
            f"CREATE TABLE IF NOT EXISTS {t} ("
            "id TEXT PRIMARY KEY, document_id TEXT NOT NULL, text TEXT NOT NULL, "
            f"metadata_ JSONB DEFAULT '{{}}', embedding vector({self.vector_dim}));",
            f"CREATE INDEX IF NOT EXISTS idx_{t}_hnsw ON {t} "
            "USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 100);",
            f"CREATE INDEX IF NOT EXISTS idx_{t}_metadata ON {t} USING gin (metadata_);",
        ]

    def _connect(self):
        import psycopg
        # The password comes only from the environment; there is no default.
        return psycopg.connect(
            host=self.host,
            port=self.port,
            dbname=self.db_name,
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD"),
            connect_timeout=5,
        )

    def initialize(self):
        """Initializes pgvector table, HNSW and GIN indexes if PostgreSQL is live."""
        if not self._use_in_memory:
            try:
                with self._connect() as conn:
                    with conn.cursor() as cur:
                        for statement in self.schema_statements():
                            cur.execute(statement)
                    conn.commit()
            except Exception:
                self._use_in_memory = True

    def is_connected(self) -> bool:
        if self._use_in_memory:
            return True
        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
            return True
        except Exception:
            return False

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
        if chunk_size < 1 or chunk_overlap < 0 or chunk_overlap >= chunk_size:
            # overlap >= size makes the window stop advancing: an infinite loop
            raise ValueError("chunk_overlap must be >= 0 and smaller than chunk_size")
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

    @staticmethod
    def _require_tenant(tenant: Any) -> str:
        if not isinstance(tenant, str) or not tenant.strip():
            raise ValueError("tenant_id is required")
        return tenant

    def ingest_document(self, document_id: str, title: Optional[str], text: str, metadata: dict[str, Any]) -> int:
        self._require_tenant(metadata.get("tenant_id"))
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
        score_threshold: float = 0.60,
        filters: Optional[dict[str, Any]] = None,
        *,
        tenant_id: str,
    ) -> list[dict]:
        self._require_tenant(tenant_id)
        # The trusted tenant overrides any tenant_id the caller put in the filters.
        scope = {**(filters or {}), "tenant_id": tenant_id}
        query_vec = self._generate_vector(query)
        candidates = []

        for node in self._in_memory_nodes:
            if any(node["metadata"].get(k) != v for k, v in scope.items()):
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
        """Lexical groundedness and relevancy (a heuristic, not an LLM judge)."""
        punctuation = '.,!?:;"' + "'"

        def words(text: str) -> list[str]:
            return [w.lower().strip(punctuation) for w in text.split() if len(w.strip(punctuation)) > 3]

        resp_words = words(response)
        context_text = " ".join(contexts).lower()
        if not contexts or not resp_words:
            grounded = 0.0
        else:
            grounded = sum(1 for w in resp_words if w in context_text) / len(resp_words)
        faithfulness = grounded >= FAITHFULNESS_THRESHOLD
        relevancy = bool(set(words(query)) & set(resp_words))

        score = round(grounded, 3) if relevancy else round(min(grounded, 0.5), 3)
        return {
            "faithfulness_passing": faithfulness,
            "relevancy_passing": relevancy,
            "score": score,
            "feedback": "Response is grounded in context." if faithfulness else "Response may lack direct context grounding."
        }

vector_service = VectorService()
