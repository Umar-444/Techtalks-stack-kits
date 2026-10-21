import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.postgres import PGVectorStore

def get_pgvector_index(connection_string: str, table_name: str = "rag_embeddings"):
    vector_store = PGVectorStore.from_params(
        database="rag_db",
        host="localhost",
        password="password",
        port=5432,
        user="postgres",
        table_name=table_name,
        embed_dim=1536,
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return VectorStoreIndex.from_vector_store(vector_store=vector_store)

def query_rag(index, query_str: str):
    query_engine = index.as_query_engine(similarity_top_k=5)
    return query_engine.query(query_str)
