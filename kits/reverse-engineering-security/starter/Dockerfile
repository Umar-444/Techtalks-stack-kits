# Production container for Reverse Engineering & Security Audit Pack
FROM python:3.12-alpine

WORKDIR /app

RUN addgroup -S appgroup -g 10001 && \
    adduser -S appuser -u 10001 -G appgroup

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER 10001:10001

ENTRYPOINT ["python", "cli.py"]
CMD ["scan", "--help"]
