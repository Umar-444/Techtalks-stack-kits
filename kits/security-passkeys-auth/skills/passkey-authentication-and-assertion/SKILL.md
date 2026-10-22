---
name: passkey-authentication-and-assertion
description: Implementing passwordless passkey login, assertion verification, and signature counter rollback protection.
---
# Passkey Authentication and Assertion Skill

## 1. Authentication Options Generation
```typescript
import { generateAuthenticationOptions } from "@simplewebauthn/server";

export async function handleAuthOptions(c: Context) {
    const options = await generateAuthenticationOptions({
        rpID: process.env.RP_ID || "localhost",
        userVerification: "preferred",
    });
    await saveChallenge(c, options.challenge);
    return c.json(options);
}
```

## 2. Assertion Verification & Cloning Protection
```typescript
import { verifyAuthenticationResponse } from "@simplewebauthn/server";

export async function handleAuthVerify(c: Context) {
    const body = await c.req.json();
    const expectedChallenge = await getChallenge(c);
    const passkey = await db.getPasskeyById(body.id);
    
    if (!passkey) {
        return c.json({ error: "Unrecognized credential" }, 404);
    }

    const verification = await verifyAuthenticationResponse({
        response: body,
        expectedChallenge,
        expectedOrigin: process.env.EXPECTED_ORIGIN || "http://localhost:8080",
        expectedRPID: process.env.RP_ID || "localhost",
        credential: {
            id: passkey.id,
            publicKey: passkey.publicKey,
            counter: passkey.counter,
        },
        requireUserVerification: true,
    });

    if (!verification.verified) {
        return c.json({ error: "Assertion verification failed" }, 400);
    }

    const { newCounter } = verification.authenticationInfo;
    if (passkey.counter > 0 && newCounter <= passkey.counter) {
        // Critical: counter did not advance on a physical hardware token
        return c.json({ error: "Authenticator cloning detected" }, 403);
    }

    await db.updatePasskeyCounter(passkey.id, newCounter);
    
    // Rotate session ID and issue HttpOnly cookie
    const sessionToken = await createSession(passkey.userId);
    setSessionCookie(c, sessionToken);

    return c.json({ verified: true, userId: passkey.userId });
}
```
