# Tool Sandboxing, Prompt Injection Defense and Secret Hygiene

# Security & Agent Guardrails
- NEVER execute unvalidated bash or shell commands from LLM outputs.
- All custom tools must wrap arguments in strict Pydantic schemas with type assertions.
- Wrap external user inputs in XML delimiter tags (<user_prompt>...</user_prompt>) to neutralize prompt injection attacks.
- Store all LLM API keys in environment variables; zero plaintext credentials permitted in source files.
