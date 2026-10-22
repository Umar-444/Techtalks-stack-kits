---
name: webauthn-registration-and-attestation
description: Configuring SimpleWebAuthn registration ceremonies, discoverable resident keys, and public key persistence.
---
# WebAuthn Registration and Attestation Skill

## 1. Options Generation Endpoint
```typescript
import { generateRegistrationOptions } from "@simplewebauthn/server";

export async function handleRegisterOptions(c: Context) {
    const user = c.get("user");
    const userPasskeys = await db.getUserPasskeys(user.id);
    
    const options = await generateRegistrationOptions({
        rpName: process.env.RP_NAME || "TechTalks Passkeys",
        rpID: process.env.RP_ID || "localhost",
        userID: new TextEncoder().encode(user.id),
        userName: user.email,
        attestationType: "none",
        excludeCredentials: userPasskeys.map(p => ({
            id: p.id,
            transports: p.transports,
        })),
        authenticatorSelection: {
            residentKey: "required",
            userVerification: "preferred",
        },
    });

    // Save challenge to temporary session
    await saveChallenge(c, options.challenge);
    return c.json(options);
}
```

## 2. Attestation Response Verification
```typescript
import { verifyRegistrationResponse } from "@simplewebauthn/server";

export async function handleRegisterVerify(c: Context) {
    const body = await c.req.json();
    const expectedChallenge = await getChallenge(c);
    
    const verification = await verifyRegistrationResponse({
        response: body,
        expectedChallenge,
        expectedOrigin: process.env.EXPECTED_ORIGIN || "http://localhost:8080",
        expectedRPID: process.env.RP_ID || "localhost",
        requireUserVerification: true,
    });

    if (!verification.verified || !verification.registrationInfo) {
        return c.json({ error: "Verification failed" }, 400);
    }

    const { credential, credentialDeviceType, credentialBackedUp } = verification.registrationInfo;
    await db.savePasskey({
        id: credential.id,
        publicKey: credential.publicKey,
        counter: credential.counter,
        deviceType: credentialDeviceType,
        backedUp: credentialBackedUp,
    });

    return c.json({ verified: true });
}
```
