---
name: security-passkeys-auth-core
description: Core operations and scaffolding skill for Passkeys WebAuthn + Hardened Auth Reference (TypeScript).
---
# Passkeys WebAuthn (TypeScript) Core Operations Manual

## 1. Stack Architecture Overview
This reference kit provides an enterprise-ready, passwordless FIDO2 / WebAuthn Level 3 authentication architecture implemented in TypeScript with Hono. It features zero shared secrets (passwords), cryptographic public-key authentication, hardware cloning defenses, and hardened session cookies.

## 2. Invariants & Rules of Engagement
1. **RP ID & Origin Matching**: `rpID` must strictly match the application domain and `expectedOrigin` must match scheme + host + port.
2. **Challenge Expiration**: Challenges expire in `< 120s` and are single-use only.
3. **Discoverable Resident Keys**: Set `residentKey: "required"` to enable platform passkey autofill.
4. **Session Fixation Defense**: Rotate session identifiers upon authentication; issue `HttpOnly; Secure; SameSite=Lax` cookies.
5. **Non-Root Docker Execution**: Run container using `USER 10001:10001`.

## 3. Fast Reference Commands
- **Install**: `bun install` or `npm install`
- **Run**: `bun run src/server.ts`
- **Test**: `bun test` or `npm test`
