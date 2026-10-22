# Multi-stage production container for Hono + Bun + SQLite
FROM oven/bun:1.1-alpine AS base

WORKDIR /app

# Non-root unprivileged execution
USER bun

COPY package.json bun.lockb* ./
RUN bun install --frozen-lockfile --production

COPY --chown=bun:bun src/ ./src/

EXPOSE 3000

HEALTHCHECK --interval=5s --timeout=3s --retries=3 \
  CMD wget --spider -q http://localhost:3000/healthz || exit 1

CMD ["bun", "src/index.ts"]
