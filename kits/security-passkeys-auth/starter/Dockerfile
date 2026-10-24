# Multi-stage hardened build for Passkeys WebAuthn Reference
FROM node:22-bookworm-slim AS builder

WORKDIR /build

COPY package.json ./
RUN npm install

COPY . .

# Final runtime image
FROM node:22-bookworm-slim AS runner

# Create non-root user (UID 10001)
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/sh -m appuser

WORKDIR /app

COPY --from=builder --chown=appuser:appgroup /build/node_modules ./node_modules
COPY --from=builder --chown=appuser:appgroup /build/package.json ./package.json
COPY --from=builder --chown=appuser:appgroup /build/src ./src

USER 10001:10001

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD node -e "fetch('http://127.0.0.1:8080/health').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"

# src/server.ts exports the Hono app only; src/index.ts is what binds a port
# via @hono/node-server. The previous CMD invoked ts-node, which was never a
# dependency, against a module that starts no listener.
CMD ["npx", "tsx", "src/index.ts"]
