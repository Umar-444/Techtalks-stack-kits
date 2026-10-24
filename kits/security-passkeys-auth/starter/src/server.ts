import { Hono } from "hono";
import { cors } from "hono/cors";
import { bodyLimit } from "hono/body-limit";
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
const IS_PROD = process.env.NODE_ENV === "production";
const MAX_BODY_BYTES = 16 * 1024;

const cookieBase = {
    httpOnly: true,
    secure: IS_PROD,
    sameSite: "Lax" as const,
    path: "/",
};

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

// Ceremony responses are small; cap request bodies before parsing.
app.use(
    "/api/*",
    bodyLimit({
        maxSize: MAX_BODY_BYTES,
        onError: (c) => c.json({ error: "Payload too large" }, 413),
    })
);

// Never leak library or runtime error text to the client.
app.onError((_err, c) => c.json({ error: "Internal error" }, 500));

async function readJson(c: { req: { json: () => Promise<unknown> } }): Promise<any | null> {
    try {
        const body = await c.req.json();
        return body && typeof body === "object" ? body : null;
    } catch {
        return null;
    }
}

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
//    A brand-new account gets a server-generated userId. Adding a passkey to an
//    existing account requires a session that already belongs to that account,
//    otherwise anyone could attach their authenticator to a victim's userId.
app.get("/api/auth/register-options", async (c) => {
    const requestedUserId = c.req.query("userId");
    const userName = (c.req.query("userName") || "developer@example.com").slice(0, 254);

    let userId: string;
    let userPasskeys: StoredPasskey[] = [];
    if (requestedUserId) {
        userPasskeys = await authStore.getUserPasskeys(requestedUserId);
        if (userPasskeys.length > 0) {
            const sessionUser = await authStore.getSessionUser(getCookie(c, "sid"));
            if (sessionUser !== requestedUserId) {
                return c.json({ error: "Authentication required" }, 401);
            }
        }
        userId = requestedUserId;
    } else {
        userId = crypto.randomUUID();
    }

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

    // Challenge and the identity it was issued for are bound to a random
    // registration session cookie, so the verify step cannot be redirected to
    // another userId and a third party cannot burn someone else's challenge.
    const regSession = crypto.randomUUID();
    await authStore.saveChallenge(`reg-${regSession}`, options.challenge, 120, { userId, userName });
    setCookie(c, "reg_challenge_session", regSession, { ...cookieBase, maxAge: 120 });
    return c.json(options);
});

// 2. Passkey Registration Ceremony: Verification
app.post("/api/auth/register-verify", async (c) => {
    const body = await readJson(c);
    if (!body) return c.json({ error: "Invalid request body" }, 400);

    const regSession = getCookie(c, "reg_challenge_session");
    const pending = regSession ? await authStore.consumeChallenge(`reg-${regSession}`) : null;
    if (!pending || !pending.meta) {
        return c.json({ error: "Challenge expired or missing" }, 400);
    }
    deleteCookie(c, "reg_challenge_session", { path: "/" });
    const { userId, userName } = pending.meta;

    try {
        const verification = await verifyRegistrationResponse({
            response: body,
            expectedChallenge: pending.challenge,
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

        return c.json({ verified: true, credentialId: credential.id, userId });
    } catch {
        return c.json({ error: "Registration verification failed" }, 400);
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
        ...cookieBase,
        maxAge: 120, // 2 minutes
    });

    return c.json(options);
});

// 4. Passkey Authentication Ceremony: Verification
app.post("/api/auth/authenticate-verify", async (c) => {
    const body = await readJson(c);
    if (!body || typeof body.id !== "string") return c.json({ error: "Invalid request body" }, 400);

    const challengeSession = getCookie(c, "auth_challenge_session");
    // The challenge is consumed before anything else is checked, so a failed
    // attempt cannot be retried against the same challenge.
    const expectedChallenge = challengeSession
        ? await authStore.getChallenge(`auth-${challengeSession}`)
        : null;
    if (!expectedChallenge) {
        return c.json({ error: "Authentication challenge expired" }, 400);
    }
    deleteCookie(c, "auth_challenge_session", { path: "/" });

    const passkey = await authStore.getPasskeyById(body.id);
    if (!passkey) {
        return c.json({ error: "Authentication failed" }, 400);
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
            return c.json({ error: "Authentication failed" }, 400);
        }

        const { newCounter } = verification.authenticationInfo;
        if (passkey.counter > 0 && newCounter <= passkey.counter) {
            return c.json({ error: "Authenticator cloning detected: counter rolled back" }, 403);
        }

        await authStore.updatePasskeyCounter(passkey.id, newCounter);

        // Session fixation defense: any pre-login session id is destroyed and a
        // fresh one is issued.
        const previousSid = getCookie(c, "sid");
        if (previousSid) await authStore.deleteSession(previousSid);
        const userSessionToken = crypto.randomUUID();
        await authStore.createSession(userSessionToken, passkey.userId);

        setCookie(c, "sid", userSessionToken, { ...cookieBase, maxAge: 86400 * 7 });

        return c.json({
            verified: true,
            userId: passkey.userId,
            userName: passkey.userName,
        });
    } catch {
        return c.json({ error: "Authentication failed" }, 400);
    }
});

export default app;
