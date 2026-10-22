---
name: llamaindex-rag-evals
description: Execute automated Faithfulness and Relevancy evaluations on LlamaIndex RAG pipeline query responses.
---

# LlamaIndex RAG Evals Skill: Faithfulness & Relevancy Validation

## Objective
Continuously measure the quality and groundedness of RAG responses using LlamaIndex's built-in evaluation framework to prevent hallucinations.

## Implementation Workflow

### 1. Faithfulness Evaluator
Measures whether the generated response is strictly grounded in the retrieved source context nodes:

```python
from llama_index.core.evaluation import FaithfulnessEvaluator

def evaluate_faithfulness(query_engine, query_str: str) -> dict:
    response = query_engine.query(query_str)
    evaluator = FaithfulnessEvaluator()
    eval_result = evaluator.evaluate_response(response=response)
    
    return {
        "query": query_str,
        "response": str(response),
        "passing": eval_result.passing,
        "feedback": eval_result.feedback,
        "score": eval_result.score
    }
```

### 2. Relevancy Evaluator
Measures whether the generated response directly answers the user's input query:

```python
from llama_index.core.evaluation import RelevancyEvaluator

def evaluate_relevancy(query_engine, query_str: str) -> dict:
    response = query_engine.query(query_str)
    evaluator = RelevancyEvaluator()
    eval_result = evaluator.evaluate_response(query=query_str, response=response)
    
    return {
        "query": query_str,
        "response": str(response),
        "passing": eval_result.passing,
        "feedback": eval_result.feedback,
        "score": eval_result.score
    }
```

## Done Means
Evaluation pipelines test queries against retrieved context, returning boolean `passing` flags and numerical scores validating that answers are strictly grounded in source documents without hallucinations.
