import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "LLM Guardrails & AI Gateway"
    environment: str = "production"
    port: int = 8080
    allowed_origins: str = "http://localhost:3000,http://localhost:8080"
    redis_url: str = "redis://localhost:6379/0"
    max_input_tokens: int = 8192
    max_output_tokens: int = 2048
    rate_limit_per_minute: int = 60
    monthly_dollar_quota: float = 500.0
    upstream_llm_url: str = "https://api.openai.com/v1"
    
    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
