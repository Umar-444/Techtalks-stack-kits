import uuid
import time
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.core.config import settings
from app.guardrails.injection import detect_prompt_injection, sandbox_user_input, generate_canary_token, detect_canary_leak
from app.guardrails.pii import anonymize_pii, deanonymize_pii
from app.guardrails.budget import rate_limiter
from app.guardrails.output import GuardrailEvaluation, StructuredChatResponse

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,
)

# Enforce explicit CORS policy (wildcard "*" is strictly forbidden by Semgrep security rules)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Tenant-ID", "X-API-Key"],
)

@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    """Enforce defense-in-depth HTTP security headers."""
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return response

class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(system|user|assistant)$")
    content: str = Field(..., min_length=1, max_length=16000)

class ChatCompletionRequest(BaseModel):
    model: str = Field(default="gpt-4o")
    messages: List[ChatMessage]
    tenant_id: Optional[str] = Field(default="default-tenant")
    max_tokens: Optional[int] = Field(default=2048, ge=1, le=8192)

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health and gateway status probe."""
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.environment,
        "guardrails_active": True,
        "pii_redaction_engine": "regex_presidio",
        "prompt_injection_guard": "heuristics_and_sandboxing",
    }

@app.post("/v1/chat/completions", response_model=StructuredChatResponse, status_code=status.HTTP_200_OK)
async def proxy_chat_completion(req: ChatCompletionRequest):
    """
    Guarded AI completion proxy:
    1. Tenant rate limit & budget check
    2. Input prompt injection screening
    3. Automated PII anonymization
    4. Input sandboxing & Canary token injection
    5. Mock / Upstream LLM execution
    6. Canary leakage check & PII deanonymization
    7. Pydantic AI structured response validation
    """
    tenant_id = req.tenant_id or "default-tenant"
    
    # 1. Rate Limit & Budget Check
    if rate_limiter.is_rate_limited(tenant_id):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded for tenant. Maximum requests reached."
        )
        
    user_messages = [m.content for m in req.messages if m.role == "user"]
    user_prompt = " ".join(user_messages) if user_messages else ""
    
    # 2. Prompt Injection & Jailbreak Screening
    is_safe, reason = detect_prompt_injection(user_prompt)
    if not is_safe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "PromptInjectionBlocked",
                "message": reason,
                "risk_level": "critical",
            }
        )
        
    # 3. PII Anonymization
    anonymized_prompt, pii_map = anonymize_pii(user_prompt)
    pii_count = len(pii_map)
    
    # 4. Delimiter Sandboxing & Canary Token
    sandboxed_text, tag_id = sandbox_user_input(anonymized_prompt)
    canary = generate_canary_token()
    
    # 5. Simulated Upstream LLM Execution
    simulated_reply = f"Processed request securely: {anonymized_prompt}"
    
    # 6. Canary Leak Detection
    if detect_canary_leak(simulated_reply, canary):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Canary token leakage detected. Prompt extraction blocked."
        )
        
    # Reversible PII restoration
    final_content = deanonymize_pii(simulated_reply, pii_map)
    
    prompt_tokens = max(1, len(user_prompt.split()) * 2)
    completion_tokens = max(1, len(final_content.split()) * 2)
    cost = rate_limiter.record_cost(tenant_id, prompt_tokens, completion_tokens)
    
    evaluation = GuardrailEvaluation(
        is_safe=True,
        risk_level="low",
        detected_pii_count=pii_count,
        blocked_categories=[],
        remediated_text=final_content if pii_count > 0 else None,
    )
    
    return StructuredChatResponse(
        id=f"chatcmpl-{uuid.uuid4().hex[:12]}",
        model=req.model,
        content=final_content,
        evaluation=evaluation,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        cost_usd=cost,
    )
