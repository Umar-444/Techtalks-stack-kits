from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

def screen_prompt(user_input: str) -> str:
    results = analyzer.analyze(text=user_input, language="en")
    anonymized = anonymizer.anonymize(text=user_input, analyzer_results=results)
    return anonymized.text
