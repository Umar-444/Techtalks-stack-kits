---
name: first-feature
description: Implement the canonical first feature: a multi-agent automated code review and summary graph.
---

# First Feature Skill: Multi-Agent Code Review Graph

## Objective
Construct an autonomous dual-agent pipeline combining a LangGraph state machine coordinator with a CrewAI specialized security audit agent.

## Implementation Steps
1. Define the shared state schema in `app/state.py`:
   ```python
   from typing import TypedDict, List
   class AgentState(TypedDict):
       task: str
       code_snippet: str
       security_findings: List[str]
       final_summary: str
   ```
2. Implement the CrewAI security agent tool caller.
3. Wire the LangGraph state machine with validation nodes.
4. Expose the workflow on `POST /review` in `app/main.py`.

## Done Means
A developer or agent posts a code snippet to `/review` and receives structured security analysis findings and refactoring suggestions within 5 seconds.
