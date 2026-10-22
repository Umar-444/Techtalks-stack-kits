---
name: install-and-verify
description: Comprehensive preflight verification, package installation, and ceremony test execution for TypeScript Passkeys WebAuthn.
---
# Install and Verify Skill: Passkeys WebAuthn (TypeScript)

## 1. Environment & Package Setup
Install dependencies using Bun or Node.js / npm:
```bash
bun install
# Or: npm install
```

## 2. Configuration & Environment Setup
Ensure `.env` matches your local development hostname:
```bash
cp .env.example .env
```
Default parameters:
- `RP_ID=localhost`
- `EXPECTED_ORIGIN=http://localhost:8080`
- `PORT=8080`

## 3. Run Test Suite
Run the automated WebAuthn ceremony simulation:
```bash
bun test
# Or: npm test
```

## 4. Launch Development Server
Start the Hono WebAuthn server:
```bash
bun run src/server.ts
```
Check health: `curl http://localhost:8080/health`.
