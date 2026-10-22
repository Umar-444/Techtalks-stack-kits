# Agentic LangGraph + CrewAI + FastAPI — Claude Code Guidelines (CLAUDE.md)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Quick Reference & Non-Negotiable Standards
### Architecture for Agentic LangGraph + CrewAI + FastAPI
# Architecture
Modular structure.

### 01 Framework Conventions
# Python 3.12, Strict Typing and FastAPI Async Standards

# Python 3.12 & FastAPI Architecture Guidelines
- Target Python 3.12+ with strict type hints on all functions and methods.
- Use Pydantic v2 schemas (BaseModel) for all request/response validation and tool schemas.
- Declare all FastAPI endpoints as sync def with explicit 
esponse_model and status codes.
- Structure dependencies using FastAPI Depends() for state, session, and agent squad injection.


### 02 Langgraph State Machine
# LangGraph StateGraph Invariants and Cyclic Graph Termination

# LangGraph State Machine Invariants
- Define all workflow states as immutable TypedDict schemas with Annotated reducers.
- Every cyclic edge MUST have an explicit termination condition checked via conditional router functions.
- Enforce 
ecursion_limit (default max: 25) on all .invoke() and .stream() calls to prevent infinite execution loops.
- Use MemorySaver or Redis checkpointing for state persistence across asynchronous user turns.


### Security for Agentic LangGraph + CrewAI + FastAPI
# Security
Zero credential leaks.

### 03 Crewai Delegation
# CrewAI Agent Squads, Roles and Task Hierarchies

# CrewAI Squad Orchestration Invariants
- Each agent must define a clear, non-overlapping 
ole, goal, and ackstory.
- Limit agent tool access: assign only the specific tools required for that agent's explicit responsibilities.
- Set erbose=True in development and stream agent execution thoughts to structured logs.
- Never allow agents to delegate infinitely; set max_iter=5 on autonomous task executions.


### 04 Security And Guardrails
# Tool Sandboxing, Prompt Injection Defense and Secret Hygiene

# Security & Agent Guardrails
- NEVER execute unvalidated bash or shell commands from LLM outputs.
- All custom tools must wrap arguments in strict Pydantic schemas with type assertions.
- Wrap external user inputs in XML delimiter tags (<user_prompt>...</user_prompt>) to neutralize prompt injection attacks.
- Store all LLM API keys in environment variables; zero plaintext credentials permitted in source files.


### 05 Testing And Evals
# Pytest-Asyncio Test Suites and Evaluation Gates

# Testing and Evaluation Gates
- Every node function in the LangGraph workflow must have an isolated unit test in 	ests/test_graph.py.
- Mock external LLM API calls in CI using pytest fixtures to guarantee deterministic, fast test runs.
- Verify token budget consumption: total session tokens must not exceed 20,000 tokens per standard query.
- Assert API response contracts using FastAPI TestClient in 	ests/test_api.py.


