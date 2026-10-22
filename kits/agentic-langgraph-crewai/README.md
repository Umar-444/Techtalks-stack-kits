# Agentic LangGraph + CrewAI + FastAPI Stack Kit

Production-ready multi-agent coordination architecture: LangGraph state machines paired with CrewAI autonomous agent squads and high-throughput async FastAPI endpoints.

## What is Inside
- **LangGraph 0.2+**: Cyclic state graphs with TypedDict immutability and recursion ceilings.
- **CrewAI 0.70+**: Autonomous agent squads with non-overlapping roles and task hierarchies.
- **FastAPI 0.115+**: Async endpoints with Pydantic v2 schemas and /health probes.
- **Rootless Docker**: Multi-stage unprivileged Docker container with healthcheck.
- **6 Agent Dialects**: Rules pre-compiled for Claude Code, Cursor, Codex, Copilot, Cline, and Antigravity.
- **4 Skills**: langgraph-graph, crewai-orchestration, 	ool-sandboxing, and eval-benchmark.

## Quickstart

### Prerequisites
- Docker and Docker Compose (or Python 3.12+)
- Git

### 1. Clone & Start Containers
````bash
git clone https://github.com/Umar-444/Techtalks-stack-kits.git
cd Techtalks-stack-kits/kits/agentic-langgraph-crewai/starter
cp .env.example .env
docker compose up -d
`

### 2. Verify Health
````bash
curl http://localhost:8000/health
# {"status":"healthy","service":"agentic-langgraph-crewai","version":"1.0.0"}
`

### 3. Run Agent Workflow
````bash
curl -X POST http://localhost:8000/api/v1/run-agent \
  -H "Content-Type: application/json" \
  -d '{"query": "Analyze distributed cloud security"}'
`

### 4. Run Test Suite
````bash
docker compose exec app pytest tests/ -v
`

## Agent Onboarding Prompt
Feed this exact prompt into Claude Code, Cursor, or Codex:
`
You are building with the Agentic LangGraph + CrewAI + FastAPI kit. Adhere strictly to CLAUDE.md / .cursor/rules, state schemas in app/state.py, and steps/agent-build-steps.md. Never execute unvalidated shell commands.
`
