from typing import Optional, List
from pydantic import BaseModel, Field, ValidationError

class GuardrailEvaluation(BaseModel):
    is_safe: bool = Field(..., description="True if prompt and output adhere to safety policies")
    risk_level: str = Field(..., description="low, medium, high, or critical")
    detected_pii_count: int = Field(default=0, ge=0)
    blocked_categories: List[str] = Field(default_factory=list)
    remediated_text: Optional[str] = None

class StructuredChatResponse(BaseModel):
    id: str
    model: str
    content: str
    evaluation: GuardrailEvaluation
    prompt_tokens: int = Field(..., ge=0)
    completion_tokens: int = Field(..., ge=0)
    cost_usd: float = Field(..., ge=0.0)

def validate_structured_output(raw_payload: dict) -> StructuredChatResponse:
    """Validates that a response conforms strictly to the StructuredChatResponse schema."""
    return StructuredChatResponse.model_validate(raw_payload)
