from llama_index.core.evaluation import FaithfulnessEvaluator, RelevancyEvaluator

def evaluate_response(query: str, response, service_context=None):
    faithfulness = FaithfulnessEvaluator()
    relevancy = RelevancyEvaluator()
    
    f_result = faithfulness.evaluate_response(response=response)
    r_result = relevancy.evaluate_response(query=query, response=response)
    
    return {
        "faithfulness_passing": f_result.passing,
        "relevancy_passing": r_result.passing,
        "score": (1.0 if f_result.passing and r_result.passing else 0.0)
    }
