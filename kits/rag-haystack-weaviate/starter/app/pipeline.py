import time
from typing import Dict, Any, List
from app.weaviate_service import weaviate_service

class FaithfulnessEvaluator:
    def evaluate(self, answer: str, documents: List[Dict[str, Any]]) -> float:
        if not documents or not answer:
            return 0.0
        
        punctuation = '.,!?:;"' + "'"
        words = [w.lower().strip(punctuation) for w in answer.split() if len(w) > 3]
        if not words:
            return 1.0

        all_text = " ".join([d.get("content", "").lower() for d in documents])
        matches = sum(1 for w in words if w in all_text)
        score = min(1.0, max(0.0, matches / len(words)))
        return round(score, 3)

faithfulness_evaluator = FaithfulnessEvaluator()

class HaystackRAGPipeline:
    def __init__(self):
        self.is_ready = True

    def run(self, question: str, tenant_id: str = "default-tenant", alpha: float = 0.65) -> Dict[str, Any]:
        start_time = time.perf_counter()
        
        # 1. Hybrid Retrieval from Weaviate
        docs = weaviate_service.hybrid_search(query=question, tenant_id=tenant_id, alpha=alpha, limit=5)
        
        # 2. Prompt Assembly & Generation
        if not docs:
            answer = f"No documents found matching query: '{question}'."
            score = 0.0
        else:
            context_summary = " ".join([d.get("content", "") for d in docs])
            answer = context_summary
            score = faithfulness_evaluator.evaluate(answer=answer, documents=docs)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        
        return {
            "question": question,
            "answer": answer,
            "documents": docs,
            "faithfulness": score,
            "latency_ms": round(elapsed_ms, 2)
        }

rag_pipeline = HaystackRAGPipeline()
