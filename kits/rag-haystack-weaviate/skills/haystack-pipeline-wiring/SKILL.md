---
name: haystack-pipeline-wiring
description: Construct explicit Haystack 2.5+ DAG pipelines connecting text embedders, retrievers, prompt builders, and generators.
---
# Haystack Pipeline Wiring Skill

## 1. Assemble Component DAG
```python
from haystack import Pipeline
from haystack.components.builders import PromptBuilder

def build_rag_pipeline(retriever, generator):
    pipeline = Pipeline()
    
    template = """Given the following source documents, provide a factual answer.
Context:
{% for doc in documents %}
- {{ doc.content }}
{% endfor %}

Question: {{ question }}
Answer:"""

    prompt_builder = PromptBuilder(template=template)
    
    pipeline.add_component("retriever", retriever)
    pipeline.add_component("prompt_builder", prompt_builder)
    pipeline.add_component("generator", generator)
    
    pipeline.connect("retriever.documents", "prompt_builder.documents")
    pipeline.connect("prompt_builder.prompt", "generator.prompt")
    
    return pipeline
```

## 2. Execute Pipeline
```python
results = pipeline.run({
    "retriever": {"query": user_question, "tenant_id": current_tenant},
    "prompt_builder": {"question": user_question}
})
answer = results["generator"]["replies"][0]
```

## 3. Done Means
- Connections are directional and explicit.
- Template handles variable document lists cleanly via Jinja2 iteration.
- Pipeline returns typed dictionary output matching OpenAPI responses.
