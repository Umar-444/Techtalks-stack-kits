"""Convenience entry point: the same explicit DAG the API uses."""
from app.pipeline import build_rag_pipeline

pipeline = build_rag_pipeline()
