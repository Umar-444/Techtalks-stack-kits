import { Hono } from "hono";
import { cors } from "hono/cors";
import { getCookie, setCookie, deleteCookie } from "hono/cookie";
import {
    generateRegistrationOptions,
    verifyRegistrationResponse,
    generateAuthenticationOptions,
    verifyAuthenticationResponse,
} from "@simplewebauthn/server";
import { authStore, StoredPasskey } from "./db.js";

const app = new Hono();

const RP_NAME = process.env.RP_NAME || "TechTalks Verified Passkeys";
const RP_ID = process.env.RP_ID || "localhost";
const EXPECTED_ORIGIN = process.env.EXPECTED_ORIGIN || "http://localhost:8080";
const allowedOrigins = (process.env.ALLOWED_ORIGINS || "http://localhost:3000,http://localhost:8080").split(",");

// Explicit CORS (Zero wildcard '*')
app.use(
    "/*",
    cors({
        origin: allowedOrigins,
        credentials: true,
        allowMethods: ["GET", "POST", "OPTIONS"],
        allowHeaders: ["Content-Type", "Authorization", "X-Session-ID"],
    })
);

// Security Headers Middleware
app.use("/*", async (c, next) => {
    await next();
    c.header("X-Content-Type-Options", "nosniff");
    c.header("X-Frame-Options", "DENY");
    c.header("Referrer-Policy", "strict-origin-when-cross-origin");
});

app.get("/health", (c) => {
    return c.json({
        status: "ok",
        service: "passkeys-auth-reference",
        rpId: RP_ID,
        expectedOrigin: EXPECTED_ORIGIN,
        compliance: "FIDO2 / WebAuthn Level 3",
        passkeys_active: true,
    });
});

// 1. Passkey Registration Ceremony: Options
app.get("/api/auth/register-options", async (c) => {
    const userId = c.req.query("userId") || "user-default-123";
    const userName = c.req.query("userName") || "developer@example.com";
    
    const userPasskeys = await authStore.getUserPasskeys(userId);

    const options = await generateRegistrationOptions({
        rpName: RP_NAME,
        rpID: RP_ID,
        userID: new TextEncoder().encode(userId),
        userName: userName,
        attestationType: "none",
        excludeCredentials: userPasskeys.map(p => ({
            id: p.id,
            transports: p.transports as any,
        })),
        authenticatorSelection: {
            residentKey: "required",
            userVerification: "preferred",
            authenticatorAttachment: "platform",
        },
    });

    await authStore.saveChallenge(`reg-${userId}`, options.challenge);
    return c.json(options);
});

// 2. Passkey Registration Ceremony: Verification
app.post("/api/auth/register-verify", async (c) => {
    const body = await c.req.json();
    const userId = c.req.query("userId") || "user-default-123";
    const userName = c.req.query("userName") || "developer@example.com";
    
    const expectedChallenge = await authStore.getChallenge(`reg-${userId}`);
    if (!expectedChallenge) {
        return c.json({ error: "Challenge expired or missing" }, 400);
    }

    try {
        const verification = await verifyRegistrationResponse({
            response: body,
            expectedChallenge,
            expectedOrigin: EXPECTED_ORIGIN,
            expectedRPID: RP_ID,
            requireUserVerification: true,
        });

        if (!verification.verified || !verification.registrationInfo) {
            return c.json({ error: "Registration verification failed" }, 400);
        }

        const { credential, credentialDeviceType, credentialBackedUp } = verification.registrationInfo;
        
        const newPasskey: StoredPasskey = {
            id: credential.id,
            publicKey: credential.publicKey,
            userId,
            userName,
            counter: credential.counter,
            deviceType: credentialDeviceType,
            backedUp: credentialBackedUp,
            transports: credential.transports,
            createdAt: new Date(),
        };

        await authStore.savePasskey(newPasskey);

        return c.json({ verified: true, credentialId: credential.id });
    } catch (err: any) {
        return c.json({ error: err.message }, 400);
    }
});

// 3. Passkey Authentication Ceremony: Options
app.get("/api/auth/authenticate-options", async (c) => {
    const options = await generateAuthenticationOptions({
        rpID: RP_ID,
        userVerification: "preferred",
    });

    const sessionId = crypto.randomUUID();
    await authStore.saveChallenge(`auth-${sessionId}`, options.challenge);

    setCookie(c, "auth_challenge_session", sessionId, {
        httpOnly: true,
        secure: process.env.NODE_ENV === "production",
        sameSite: "Lax",
        maxAge: 120, // 2 minutes
        path: "/",
    });

    return c.json(options);
});

// 4. Passkey Authentication Ceremony: Verification
app.post("/api/auth/authenticate-verify", async (c) => {
    const body = await c.req.json();
    const sessionId = getCookie(c, "auth_challenge_session") || "default";
    
    const expectedChallenge = await authStore.getChallenge(`auth-${sessionId}`);
    if (!expectedChallenge) {
        return c.json({ error: "Authentication challenge expired" }, 400);
    }

    const passkey = await authStore.getPasskeyById(body.id);
    if (!passkey) {
        return c.json({ error: "Unrecognized credential ID" }, 404);
    }

    try {
        const verification = await verifyAuthenticationResponse({
            response: body,
            expectedChallenge,
            expectedOrigin: EXPECTED_ORIGIN,
            expectedRPID: RP_ID,
            credential: {
                id: passkey.id,
                publicKey: passkey.publicKey,
                counter: passkey.counter,
                transports: passkey.transports as any,
            },
            requireUserVerification: true,
        });

        if (!verification.verified) {
            return c.json({ error: "Assertion signature invalid" }, 400);
        }

        const { newCounter } = verification.authenticationInfo;
        if (passkey.counter > 0 && newCounter <= passkey.counter) {
            return c.json({ error: "Authenticator cloning detected: counter rolled back" }, 403);
        }

        await authStore.updatePasskeyCounter(passkey.id, newCounter);

        // Session fixation defense: regenerate session cookie
        deleteCookie(c, "auth_challenge_session");
        const userSessionToken = crypto.randomUUID();
        
        setCookie(c, "sid", userSessionToken, {
            httpOnly: true,
            secure: process.env.NODE_ENV === "production",
            sameSite: "Lax",
            maxAge: 86400 * 7,
            path: "/",
        });

        return c.json({
            verified: true,
            userId: passkey.userId,
            userName: passkey.userName,
        });
    } catch (err: any) {
        return c.json({ error: err.message }, 400);
    }
});

export default app;
