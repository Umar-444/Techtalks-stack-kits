# Hono Web Framework Conventions and Middleware Chaining

# Hono Web Framework Conventions and Middleware Chaining

## 1. Minimal Zero-Overhead Handler Design
- Instantiate applications using `new Hono()`. Keep routing declarative and modular using `app.route('/prefix', subApp)`.
- Use native Web Standard objects: Hono handlers accept standard `Context` (`c`) wrapping `Request` and returning standard `Response`.
- Always return typed JSON using `return c.json(data, status)`.

## 2. Middleware Architecture
- Order middleware logically:
  1. `logger()`: Request timing and access logs.
  2. `secureHeaders()`: Helmet-like HTTP response security headers (HSTS, CSP, X-Frame-Options).
  3. `cors()`: Explicit origin whitelisting. Never permit wildcard `*` with credentials.
  4. Authentication & RBAC middleware.
- Never block the event loop inside middleware. Use asynchronous handlers.

## 3. Error Handling
- Register a global error boundary using `app.onError((err, c) => ...)` returning standardized RFC 7807 Problem Details or JSON error envelopes.
