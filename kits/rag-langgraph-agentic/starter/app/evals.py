from typing import List, Dict, Any

class RagasEvaluator:
    def evaluate_groundedness(self, question: str, documents: List[Dict[str, Any]], answer: str) -> float:
        if not documents or not answer:
            return 0.0
        
        punctuation = '.,!?:;"' + "'"
        answer_words = [w.lower().strip(punctuation) for w in answer.split() if len(w) > 3]
        if not answer_words:
            return 1.0

        all_doc_text = " ".join([d.get("content", "").lower() for d in documents])
        matches = sum(1 for w in answer_words if w in all_doc_text)
        
        score = min(1.0, max(0.0, matches / len(answer_words)))
        return round(score, 3)

    def evaluate_context_precision(self, question: str, documents: List[Dict[str, Any]]) -> float:
        if not documents:
            return 0.0
        q_words = set(question.lower().split())
        first_doc = documents[0].get("content", "").lower().split()
        overlap = len(q_words.intersection(set(first_doc)))
        return round(min(1.0, overlap / max(1, len(q_words))), 3)

ragas_evaluator = RagasEvaluator()
