# Passkeys WebAuthn + Hardened Auth Reference (TypeScript) — Claude Code Guidelines (CLAUDE.md)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Quick Reference & Non-Negotiable Standards
### 01 Webauthn Fido2 Architecture And Standards
﻿---
id: webauthn-fido2-architecture-and-standards
title: WebAuthn FIDO2 Architecture & Standards
globs: "**/*.ts"
alwaysApply: true
---
# WebAuthn FIDO2 Architecture & Standards

## 1. Relying Party (RP) Invariants
- The Relying Party ID (`rpID`) must be a valid domain string matching the application origin host (e.g. `localhost` in local dev, `auth.example.com` or `example.com` in production).
- The `expectedOrigin` must strictly match the scheme, domain, and port:
  ```typescript
  const rpID = process.env.RP_ID || "localhost";
  const rpName = "TechTalks Passkeys Reference";
  const expectedOrigin = process.env.EXPECTED_ORIGIN || "http://localhost:8080";
  ```
- Subdomain relaxation is permitted (e.g. origin `https://app.example.com` may use `rpID = "example.com"`). Never permit IP addresses or wildcard domains.

## 2. Cryptographic Challenge Lifecycle
- Challenges MUST be generated using cryptographically secure random bytes (min 32 bytes):
  ```typescript
  // Managed automatically by @simplewebauthn/server:
  const options = await generateRegistrationOptions({ rpName, rpID, ... });
  ```
- Challenges MUST be stored server-side in a short-lived session or Redis cache with an absolute TTL (maximum 120 seconds).
- Challenges MUST be consumed exactly once (one-time use). Immediately delete the challenge upon receipt of the client assertion response to prevent replay attacks.

## 3. Supported Public Key Algorithms (COSE)
- Explicitly declare support for modern, secure cryptographic curves:
  - `-7` (ES256: ECDSA with SHA-256 over P-256 curve) - Mandatory default across Apple, Android, Windows Hello.
  - `-257` (RS256: RSASSA-PKCS1-v1_5 with SHA-256) - Enterprise smartcard / TPM fallback.
  - `-8` (Ed25519: EdDSA over Curve25519) - High-performance modern hardware tokens.


### 02 Registration And Attestation Ceremony
﻿---
id: registration-and-attestation-ceremony
title: Passkey Registration & Attestation Ceremony
globs: "**/*.ts"
alwaysApply: true
---
# Passkey Registration & Attestation Ceremony

## 1. Registration Options Generation
- Enforce resident keys (discoverable credentials) for true passwordless passkeys:
  ```typescript
  import { generateRegistrationOptions } from "@simplewebauthn/server";

  const options = await generateRegistrationOptions({
      rpName,
      rpID,
      userID: new TextEncoder().encode(user.id),
      userName: user.email,
      userDisplayName: user.name,
      attestationType: "none", // Recommended for consumer privacy & performance
      authenticatorSelection: {
          residentKey: "required", // Mandatory for passwordless autofill & passkeys
          userVerification: "preferred", // Prompts biometric/PIN without failing hardware keys
          authenticatorAttachment: "platform", // Platform authenticators (Face ID, Touch ID, Windows Hello)
      },
  });
  ```

## 2. Attestation Verification & Public Key Storage
- Always verify the client attestation response using `@simplewebauthn/server`:
  ```typescript
  import { verifyRegistrationResponse } from "@simplewebauthn/server";

  const verification = await verifyRegistrationResponse({
      response: clientResponse,
      expectedChallenge: session.currentChallenge,
      expectedOrigin,
      expectedRPID: rpID,
      requireUserVerification: true,
  });

  if (!verification.verified || !verification.registrationInfo) {
      throw new Error("Passkey registration verification failed");
  }

  const { credential, credentialDeviceType, credentialBackedUp } = verification.registrationInfo;
  
  // Persist passkey to database
  await db.passkeys.create({
      id: credential.id, // Base64URL string
      publicKey: Buffer.from(credential.publicKey),
      counter: credential.counter,
      transports: credential.transports,
      deviceType: credentialDeviceType,
      backedUp: credentialBackedUp,
      userId: user.id,
  });
  ```


### 03 Authentication And Assertion Ceremony
﻿---
id: authentication-and-assertion-ceremony
title: Passkey Authentication & Assertion Ceremony
globs: "**/*.ts"
alwaysApply: true
---
# Passkey Authentication & Assertion Ceremony

## 1. Discoverable Autofill / Passwordless Options
- For discoverable passkeys, `allowCredentials` can be omitted or empty, enabling browser autofill UI:
  ```typescript
  import { generateAuthenticationOptions } from "@simplewebauthn/server";

  const options = await generateAuthenticationOptions({
      rpID,
      userVerification: "preferred",
      // allowCredentials left empty for 1-click modal / autofill login
  });
  ```

## 2. Signature Assertion Verification & Counter Rollback Defense
- Verify the client assertion signature against the registered public key:
  ```typescript
  import { verifyAuthenticationResponse } from "@simplewebauthn/server";

  const passkey = await db.passkeys.findById(clientResponse.id);
  if (!passkey) {
      throw new Error("Passkey credential not found");
  }

  const verification = await verifyAuthenticationResponse({
      response: clientResponse,
      expectedChallenge: session.currentChallenge,
      expectedOrigin,
      expectedRPID: rpID,
      credential: {
          id: passkey.id,
          publicKey: passkey.publicKey,
          counter: passkey.counter,
          transports: passkey.transports,
      },
      requireUserVerification: true,
  });

  if (!verification.verified) {
      throw new Error("Authentication assertion signature invalid");
  }

  // Update signature counter (Crucial for hardware cloning detection)
  // Multi-device synced passkeys (iCloud, Google Password Manager) typically keep counter = 0
  const { newCounter } = verification.authenticationInfo;
  if (passkey.counter > 0 && newCounter <= passkey.counter) {
      throw new Error("Potential authenticator cloning detected: counter rolled back");
  }
  await db.passkeys.updateCounter(passkey.id, newCounter);
  ```


### 04 Session Management And Cookie Hardening
﻿---
id: session-management-and-cookie-hardening
title: Session Management & Cookie Hardening
globs: "**/*.ts"
alwaysApply: true
---
# Session Fixation Defenses & Cookie Security Standards

## 1. Session Token Rotation Post-Authentication
- To eliminate session fixation attacks, the session identifier MUST be regenerated immediately upon successful passkey verification:
  ```typescript
  // Invalidate pre-authentication session and issue fresh secure token
  await sessionStore.destroy(oldSessionId);
  const newSessionToken = crypto.randomUUID();
  await sessionStore.set(newSessionToken, { userId: user.id, authenticatedAt: Date.now() });
  ```

## 2. Hardened Cookie Attributes
- Session cookies MUST enforce:
  - `HttpOnly`: Inaccessible to JavaScript `document.cookie` (immune to XSS exfiltration).
  - `Secure`: Transmitted only over HTTPS (permitted on localhost in local dev).
  - `SameSite=Lax`: Defends against Cross-Site Request Forgery (CSRF).
  - `Path=/`: Scoped to application root.
  ```typescript
  import { setCookie } from "hono/cookie";

  setCookie(c, "sid", newSessionToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "Lax",
      maxAge: 86400 * 7, // 7 days
      path: "/",
  });
  ```

## 3. Rate Limiting on Ceremony Endpoints
- Apply strict IP-based and user-based rate limiting on `/api/auth/register-options` and `/api/auth/authenticate-options` (maximum 10 requests per minute per IP) to prevent challenge generation flooding.


### 05 Testing Verification And Ci
﻿---
id: testing-verification-and-ci
title: Testing, Verification & CI Invariants
globs: "**/*.{ts,js}"
alwaysApply: true
---
# Testing Protocols, Ceremony Mocking & CI Compliance

## 1. Automated WebAuthn Ceremony Mocking
- Unit tests must simulate WebAuthn registration and authentication without physical hardware prompts:
  - Generate valid ECDSA P-256 keypairs.
  - Construct synthetic `AuthenticatorAttestationResponse` and `AuthenticatorAssertionResponse` payloads.
  - Assert that tampered challenges or altered origins fail verification with HTTP 400.
  - Assert that counter decrements throw cloning detection exceptions.

## 2. Docker & Container Security Invariants
- Production containers must run rootless using `USER 10001:10001`.
- Alpine or slim Node.js base images with non-root ownership of bundle files.

## 3. Automated Security Scans in CI
- Pipeline must pass:
  1. `gitleaks detect --no-git` with 0 secret leaks.
  2. `semgrep scan --config p/security-code-scan` with 0 blocking SAST errors.
  3. `python tools/validate_manifest.py` verifying 100% physical file layout.
  4. `python tools/transpiler.py --check` guaranteeing zero dialect drift.


