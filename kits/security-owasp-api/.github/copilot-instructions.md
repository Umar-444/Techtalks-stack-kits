# Assistant Guidelines for OWASP API Security Top 10 Stack Kit

## Stack Overview
- Language: Python 3.12+
- Framework: FastAPI 0.115+
- Security Standard: OWASP API Security Top 10 (2023)
- Authentication: PyJWT + Bcrypt (HS256/RS256)
- Test Harness: Pytest + HTTPX TestClient
- Validation: Pydantic v2 with strict schemas

## Mandatory Rules
1. Mandatory object ownership check on all resourceful lookups (API1:2023 BOLA prevention).
2. Enforce explicit role verification for administrative actions (API5:2023 BFLA prevention).
3. Every input schema must reject unexpected fields (`extra = "forbid"`), and responses must never leak internal properties (API3:2023 BOPLA prevention).
4. Strictly enforce pagination caps (`le=100`) and rate limits (API4:2023).
5. All external URL fetching must block private IP ranges, loopback, and cloud metadata 169.254.169.254 (API7:2023 SSRF defense).
