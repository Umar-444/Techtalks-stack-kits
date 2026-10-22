# LangGraph State Machine & Cyclic Graph Control

# LangGraph State Graph & Cyclic Loop Engineering

## 1. Immutable State Definitions
- Define graph state using `TypedDict` or Pydantic `BaseModel` with explicit reducer annotations (`Annotated[list, add]` or custom operators).
- Never mutate state in-place within a node; always return a dictionary representing the state delta:
  ```python
  from typing import TypedDict, Annotated, List
  from operator import add

  class AgentState(TypedDict):
      task: str
      messages: Annotated[List[str], add]
      current_step: str
      iteration_count: int
      is_finished: bool
  ```

## 2. Bounded Recursion & Cycle Limits
- All cyclic graphs (self-correction loops, critique loops, agent debate) MUST define explicit recursion limits:
  ```python
  config = {"recursion_limit": 25}
  await graph.ainvoke(initial_state, config=config)
  ```
- Conditional edges must inspect `iteration_count` and force-route to `END` if maximum threshold is reached, preventing infinite agent spend loops.
