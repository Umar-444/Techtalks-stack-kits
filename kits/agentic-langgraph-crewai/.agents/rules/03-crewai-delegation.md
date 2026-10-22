---
name: 03-crewai-delegation
description: CrewAI Agent Squads, Roles and Task Hierarchies
---
# CrewAI Squad Orchestration Invariants
- Each agent must define a clear, non-overlapping 
ole, goal, and ackstory.
- Limit agent tool access: assign only the specific tools required for that agent's explicit responsibilities.
- Set erbose=True in development and stream agent execution thoughts to structured logs.
- Never allow agents to delegate infinitely; set max_iter=5 on autonomous task executions.
