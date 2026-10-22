# Hardened Alpine Dockerfile for OWASP API Security Test Target
FROM python:3.12-alpine AS base

WORKDIR /app

RUN apk add --no-cache tzdata ca-certificates && \
    addgroup -S appgroup -g 10001 && \
    adduser -S appuser -u 10001 -G appgroup

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER 10001:10001

EXPOSE 8000

HEALTHCHECK --interval=5s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/healthz')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
