# 04 Session Management And Cookie Hardening

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

