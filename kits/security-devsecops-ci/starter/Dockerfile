# Hardened Minimal Production Container for DevSecOps Target
FROM python:3.11-alpine AS base

WORKDIR /app

RUN apk add --no-cache tzdata ca-certificates && \
    addgroup -S appgroup -g 10001 && \
    adduser -S appuser -u 10001 -G appgroup

COPY app/ ./app/

USER 10001:10001

EXPOSE 8080

HEALTHCHECK --interval=5s --timeout=3s --retries=3 \
  CMD wget --spider -q http://localhost:8080/healthz || exit 1

CMD ["python", "app/main.py"]
