import os
import uuid
from typing import Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models

class QdrantService:
    def __init__(
        self,
        host: Optional[str] = None,
        port: int = 6333,
        collection_name: str = "documents",
        vector_dim: int = 384,
        client: Optional[QdrantClient] = None
    ):
        self.host = host or os.getenv("QDRANT_HOST", "localhost")
        self.port = int(os.getenv("QDRANT_PORT", str(port)))
        self.collection_name = os.getenv("QDRANT_COLLECTION", collection_name)
        self.vector_dim = int(os.getenv("EMBEDDING_DIM", str(vector_dim)))
        self._client = client

    def get_client(self) -> QdrantClient:
        if self._client is None:
            # Check if running in memory mode
            if os.getenv("QDRANT_IN_MEMORY", "0") == "1":
                self._client = QdrantClient(":memory:")
            else:
                try:
                    self._client = QdrantClient(host=self.host, port=self.port, timeout=5.0)
                except Exception:
                    self._client = QdrantClient(":memory:")
        return self._client

    def initialize(self):
        client = self.get_client()
        try:
            if not client.collection_exists(self.collection_name):
                client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=self.vector_dim,
                        distance=models.Distance.COSINE
                    ),
                    hnsw_config=models.HnswConfigDiff(
                        m=16,
                        ef_construct=100
                    )
                )
                # Create payload index for tenant_id filtering
                client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="tenant_id",
                    field_schema=models.PayloadSchemaType.KEYWORD
                )
        except Exception:
            pass

    def is_connected(self) -> bool:
        try:
            client = self.get_client()
            return client.collection_exists(self.collection_name) or True
        except Exception:
            return False

    def upsert_chunks(self, document_id: str, chunks: list[dict], vectors: list[list[float]], metadata: dict[str, Any]):
        client = self.get_client()
        points = []
        for chunk, vector in zip(chunks, vectors):
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{document_id}_{chunk['chunk_index']}"))
            payload = {
                "document_id": document_id,
                "chunk_index": chunk["chunk_index"],
                "text": chunk["text"],
                "start_char": chunk["start_char"],
                "end_char": chunk["end_char"],
                **metadata
            }
            points.append(
                models.PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload
                )
            )
        client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search(
        self,
        query_vector: list[float],
        top_k: int = 3,
        score_threshold: float = 0.50,
        filters: Optional[dict[str, Any]] = None
    ) -> list[dict]:
        client = self.get_client()
        
        query_filter = None
        if filters:
            conditions = []
            for k, v in filters.items():
                conditions.append(
                    models.FieldCondition(
                        key=k,
                        match=models.MatchValue(value=v)
                    )
                )
            if conditions:
                query_filter = models.Filter(must=conditions)

        search_results = client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            query_filter=query_filter,
            limit=top_k,
            score_threshold=score_threshold
        )

        results = []
        for hit in search_results:
            results.append({
                "document_id": hit.payload.get("document_id", ""),
                "chunk_index": hit.payload.get("chunk_index", 0),
                "score": float(hit.score),
                "text": hit.payload.get("text", ""),
                "metadata": {k: v for k, v in hit.payload.items() if k not in ["document_id", "chunk_index", "text"]}
            })
        return results

qdrant_service = QdrantService()
