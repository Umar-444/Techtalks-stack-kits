from haystack import Pipeline
from haystack.components.builders import PromptBuilder

pipeline = Pipeline()
prompt_template = "Context: {{ documents }}\nQuestion: {{ query }}\nAnswer:"
pipeline.add_component("prompt_builder", PromptBuilder(template=prompt_template))
