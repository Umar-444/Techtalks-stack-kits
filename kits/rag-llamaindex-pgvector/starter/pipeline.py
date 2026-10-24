import os
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.postgres import PGVectorStore


def get_pgvector_index(table_name: str = "rag_embeddings"):
    # Every connection parameter comes from the environment; no credential is
    # hardcoded and POSTGRES_PASSWORD has no default.
    vector_store = PGVectorStore.from_params(
        database=os.environ.get("POSTGRES_DB", "rag_db"),
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        password=os.environ["POSTGRES_PASSWORD"],
        port=int(os.environ.get("POSTGRES_PORT", "5432")),
        user=os.environ.get("POSTGRES_USER", "postgres"),
        table_name=table_name,
        embed_dim=int(os.environ.get("EMBEDDING_DIM", "384")),
    )
    return VectorStoreIndex.from_vector_store(vector_store=vector_store)


def query_rag(index, query_str: str):
    query_engine = index.as_query_engine(similarity_top_k=5)
    return query_engine.query(query_str)
