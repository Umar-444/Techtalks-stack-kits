---
name: first-feature
description: Guide to adding multi-passkey management, credential renaming, and device metadata labeling.
---
# First Feature Skill: Managing Multiple Passkeys per User

## 1. Schema Expansion for Passkey Metadata
In your database store, track friendly names and device models:
```typescript
interface UserPasskey {
    id: string; // Base64URL credential ID
    userId: string;
    friendlyName: string; // e.g. "MacBook Pro Touch ID", "YubiKey 5C"
    deviceType: string;   // "singleDevice" | "multiDevice"
    backedUp: boolean;
    transports: string[];
    createdAt: Date;
    lastUsedAt: Date;
}
```

## 2. Implement the Passkey List & Rename Route
In `src/routes/passkeys.ts`:
```typescript
app.get("/api/passkeys", requireAuth, async (c) => {
    const user = c.get("user");
    const passkeys = await db.getUserPasskeys(user.id);
    return c.json(passkeys.map(p => ({
        id: p.id,
        friendlyName: p.friendlyName,
        createdAt: p.createdAt,
        backedUp: p.backedUp,
    })));
});

app.patch("/api/passkeys/:id", requireAuth, async (c) => {
    const user = c.get("user");
    const passkeyId = c.req.param("id");
    const { friendlyName } = await c.req.json();
    
    await db.renamePasskey(user.id, passkeyId, friendlyName);
    return c.json({ success: true });
});
```
