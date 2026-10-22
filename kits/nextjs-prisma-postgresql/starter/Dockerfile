FROM node:22-alpine AS base

# Install OpenSSL for Prisma
RUN apk add --no-cache openssl libc6-compat

WORKDIR /app

# Create non-root user
RUN addgroup -g 10001 appgroup && \
    adduser -u 10001 -G appgroup -s /bin/sh -D appuser

FROM base AS dependencies
COPY package.json package-lock.json* ./
RUN npm install

FROM base AS builder
COPY --from=dependencies /app/node_modules ./node_modules
COPY . .
RUN npx prisma generate
RUN npm run build || true

FROM base AS runner
ENV NODE_ENV=production
ENV PORT=3000

COPY --chown=appuser:appgroup --from=dependencies /app/node_modules ./node_modules
COPY --chown=appuser:appgroup . .
RUN npx prisma generate

USER 10001:10001

EXPOSE 3000
CMD ["npm", "start"]
