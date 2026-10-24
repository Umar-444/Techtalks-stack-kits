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

CMD ["node", "--loader", "ts-node/esm", "src/server.ts"]
