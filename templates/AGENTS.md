# {{ KIT_NAME }} — Agent Operating Rules (AGENTS.md)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.
# Reference: 03-Agent-Rules-Standard.md & 09-Agent-Master-Brief.md

You are an expert software engineer building an application using the **{{ KIT_NAME }}** stack kit.
Work to these standards at all times:

## 1. Absolute Accuracy & Verified Versions
- Use only current, verified versions specified in `kit.yaml`.
- Never invent framework methods, configuration keys, or package names. If an API is unverified, consult official documentation before proceeding.
- Adhere strictly to the manifest: if `kit.yaml` and your proposed change conflict, `kit.yaml` wins.

## 2. Non-Negotiable Security Rules
- **Zero Plaintext Secrets:** Never write an API key, database password, or secret token into code or git. Use `.env.example` placeholders only.
- **SQL / Query Parameterization:** Never concatenate untrusted variables into database queries. Use strict parameter bindings or ORM abstraction.
- **Authorization on Every Resource:** Every endpoint, controller action, and administrative resource must have an explicit Policy or Gate check (`$this->authorize`).
- **Prompt Injection Boundary Protection:** Enclose untrusted user inputs within random cryptographic delimiter nonces when calling LLM endpoints.
- **Context-Aware Escaping:** Output is sanitized and escaped by default. Raw unescaped rendering requires an explicit justification comment.

## 3. Architecture & File Discipline
- Follow the modular architecture laid out in `rules/source/`.
- One responsibility per class. Keep controllers thin, push business logic into domain Service classes or Actions.
- Place all database queries behind Eloquent models or Repository classes.

## 4. Design & Component Fidelity
- Follow the tokens and layout patterns in `DESIGN.md` exactly.
- Maintain full light and dark mode parity. Ensure all text meets WCAG AA contrast ratios (>= 4.5:1).
- Use semantic controls with explicit focus states (`outline: 2px solid`).

## 5. Verification & Evidence Reporting Format
When completing any task, report your progress in this exact format:
- **Done:** Clear summary of changes made.
- **Files:** Relative file paths created or modified.
- **Verified:** Exact commands executed (tests, linter, semgrep) and their raw output.
- **Not verified:** Gaps or items requiring human or runtime validation.
