# SECURITY.md — MongoDB NoSQL Security Standards

1. **NoSQL Injection Defense:**
   Never allow raw user input as field keys or query operators (`$where`, `$regex`, `$gt`).

2. **BSON Type Validation:**
   Validate incoming request parameters explicitly as strings, integers, or dates before querying.

3. **Authorization & Scoping:**
   Ensure every document query filters by authenticated user or team ID to prevent BOLA vulnerabilities.
