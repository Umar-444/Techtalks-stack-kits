# CLAUDE.md ? Agentic LangGraph + CrewAI + FastAPI

You are pair programming on an enterprise-grade multi-agent AI system.

## Primary Invariants
1. **LangGraph State**: Never mutate state in-place; always return updated TypedDict partials from nodes.
2. **CrewAI Squads**: Define explicit roles, goals, and backstories. Keep tools sandboxed with Pydantic schemas.
3. **Security**: Never execute unvalidated shell commands. Use Gitleaks for secret scanning and Semgrep for AST checks.
4. **FastAPI**: Write async endpoints with explicit Pydantic v2 
esponse_model definitions.

## Key Commands
- Run API server: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
- Run test suite: pytest tests/ -v
- Run security scans: gitleaks detect --source .
- Docker compose up: docker compose up -d
