# WebAuthn FIDO2 Architecture & Standards

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
