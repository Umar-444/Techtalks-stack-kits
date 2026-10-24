# Multi-stage production Dockerfile for Go + Chi service
FROM golang:1.23-alpine AS builder

WORKDIR /build

COPY go.mod ./
COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o server main.go

FROM alpine:3.20 AS runner

WORKDIR /app

# Create unprivileged user to satisfy security invariants
RUN addgroup -g 10001 appgroup && \
    adduser -u 10001 -G appgroup -D -s /bin/sh appuser

COPY --from=builder --chown=10001:10001 /build/server /app/server

USER 10001:10001

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

CMD ["/app/server"]
