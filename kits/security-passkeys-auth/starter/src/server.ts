import { Hono } from "hono";
import { generateRegistrationOptions, verifyRegistrationResponse } from "@simplewebauthn/server";

const app = new Hono();
const rpName = "TechTalks Verified Passkeys";
const rpID = "localhost";

app.get("/api/auth/register-options", async (c) => {
    const options = await generateRegistrationOptions({
        rpName,
        rpID,
        userID: new TextEncoder().encode("user-123"),
        userName: "user@example.com",
    });
    return c.json(options);
});

export default app;
