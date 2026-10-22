---
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
