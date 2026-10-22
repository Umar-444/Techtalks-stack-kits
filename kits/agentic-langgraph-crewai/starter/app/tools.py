from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    query: str = Field(description="Search term to lookup factual knowledge")

def sandboxed_search(query: str) -> str:
    """Deterministic simulated search tool with strict output constraints."""
    clean_query = query.strip()[:150]
    return f"Factual search result for topic '{clean_query}': Architecture verified with zero drift."
