FROM node:22-alpine AS base

WORKDIR /app

RUN addgroup -g 10001 appgroup && \
    adduser -u 10001 -G appgroup -s /bin/sh -D appuser

FROM base AS dependencies
COPY package.json package-lock.json* ./
RUN npm install

FROM base AS builder
COPY --from=dependencies /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM base AS runner
ENV NODE_ENV=production
ENV PORT=8080

COPY --chown=appuser:appgroup --from=dependencies /app/node_modules ./node_modules
COPY --chown=appuser:appgroup --from=builder /app/dist ./dist
COPY --chown=appuser:appgroup . .

USER 10001:10001

EXPOSE 8080
CMD ["node", "dist/transports/sse.js"]
