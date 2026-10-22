---
id: security-tool-sandboxing-and-guardrails
title: Security, Tool Sandboxing & Guardrails
globs: "**/*.py"
alwaysApply: true
---
# Agent Tool Sandboxing, Authorization & Prompt Isolation

## 1. Strict Tool Input Validation
- All tools accessible to agents must enforce strict Pydantic schemas.
- NEVER permit agents to run raw arbitrary shell commands or unsanitized SQL queries.
- Read-only tools must be partitioned from state-mutating tools:
  ```python
  from pydantic import BaseModel, Field

  class CodeExecutionInput(BaseModel):
      code: str = Field(..., max_length=4000)
      timeout_seconds: int = Field(default=5, le=10)
  ```

## 2. Tool Sandboxing Invariants
- Any code execution tool must execute inside an ephemeral, resource-constrained container or isolated WebAssembly (Wasm) sandbox without network egress or host filesystem mount.

## 3. Human-in-the-Loop (HITL) Interception
- Critical state mutations (deploying code, purchasing, deleting databases) must yield LangGraph interrupts:
  ```python
  graph.compile(checkpointer=checkpointer, interrupt_before=["execute_deployment"])
  ```
