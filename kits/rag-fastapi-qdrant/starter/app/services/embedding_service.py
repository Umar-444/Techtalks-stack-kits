import hashlib
import math
from typing import Optional

class EmbeddingService:
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5", vector_dim: int = 384):
        self.model_name = model_name
        self.vector_dim = vector_dim
        self._model = None

    def _get_model(self):
        if self._model is None:
            try:
                from fastembed import TextEmbedding
                self._model = TextEmbedding(model_name=self.model_name)
            except Exception:
                self._model = "fallback"
        return self._model

    def chunk_text(self, text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[dict]:
        """Partitions text into overlapping sliding-window chunks with char offsets."""
        if chunk_size < 1 or chunk_overlap < 0 or chunk_overlap >= chunk_size:
            # overlap >= size makes the window stop advancing: an infinite loop
            raise ValueError("chunk_overlap must be >= 0 and smaller than chunk_size")
        chunks = []
        start = 0
        idx = 0
        text_len = len(text)

        while start < text_len:
            end = min(start + chunk_size, text_len)
            chunk_str = text[start:end].strip()
            if chunk_str:
                chunks.append({
                    "chunk_index": idx,
                    "text": chunk_str,
                    "start_char": start,
                    "end_char": end
                })
                idx += 1
            if end == text_len:
                break
            start += chunk_size - chunk_overlap
        return chunks

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Generates normalized dense vectors."""
        model = self._get_model()
        if model != "fallback":
            try:
                embeddings = list(model.embed(texts))
                return [e.tolist() for e in embeddings]
            except Exception:
                pass

        # Deterministic offline unit-normalized vector generator for fast reliable local tests
        results = []
        for text in texts:
            vector = []
            seed = hashlib.sha256(text.encode("utf-8")).digest()
            for i in range(self.vector_dim):
                byte_val = seed[i % len(seed)]
                val = ((byte_val + i * 7) % 200) / 100.0 - 1.0
                vector.append(val)
            norm = math.sqrt(sum(x * x for x in vector)) or 1.0
            results.append([x / norm for x in vector])
        return results

    def embed_query(self, query: str) -> list[float]:
        return self.embed_texts([query])[0]

embedding_service = EmbeddingService()
