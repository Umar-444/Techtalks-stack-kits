---
name: crewai-orchestration
description: Configure role-playing CrewAI agents, assign sandboxed tools, and run squads.
---
# CrewAI Orchestration Skill

## Usage
`python
from crewai import Agent, Crew, Process, Task

researcher = Agent(
    role="Principal Data Analyst",
    goal="Extract factual, verifiable metrics from input text",
    backstory="You are an expert quantitative researcher with high analytical standards.",
    tools=[search_tool],
    verbose=True
)
`
