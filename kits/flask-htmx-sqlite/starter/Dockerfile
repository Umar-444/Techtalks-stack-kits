# Multi-stage hardened build for Flask + HTMX + SQLite
FROM python:3.12-slim-bookworm AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final Runtime Image
FROM python:3.12-slim-bookworm AS runner

# Create non-root user (UID 10001)
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/sh -m appuser

WORKDIR /app

# Copy installed python wheels from builder
COPY --from=builder /root/.local /home/appuser/.local
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Copy application source
COPY --chown=appuser:appgroup . .

# Ensure instance directory exists with write permissions for SQLite database and WAL files
RUN mkdir -p /app/instance && chown -R appuser:appgroup /app/instance

USER 10001:10001

EXPOSE 8080

CMD ["gunicorn", "-w", "2", "-k", "gthread", "--threads", "4", "-b", "0.0.0.0:8080", "app:create_app()"]
