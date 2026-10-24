# Multi-stage production container for Rust + Loco.rs + SeaORM + SQLite
FROM rust:1.81-alpine AS builder

WORKDIR /app

RUN apk add --no-cache musl-dev gcc make sqlite-dev

COPY Cargo.toml ./
RUN mkdir src && echo "pub fn dummy() {}" > src/lib.rs && echo "fn main() {}" > src/main.rs && cargo build --release || true

COPY . .
RUN cargo build --release

FROM alpine:3.20 AS final

WORKDIR /app

RUN apk add --no-cache ca-certificates tzdata sqlite-libs && \
    addgroup -S appgroup -g 10001 && \
    adduser -S appuser -u 10001 -G appgroup && \
    mkdir -p /app/storage && \
    chown -R 10001:10001 /app/storage

COPY --from=builder /app/target/release/rust_loco_sqlite_starter /app/server
COPY --from=builder /app/config /app/config

USER 10001:10001

EXPOSE 5150

VOLUME ["/app/storage"]

HEALTHCHECK --interval=5s --timeout=3s --retries=3 \
  CMD wget --spider -q http://localhost:5150/healthz || exit 1

CMD ["/app/server", "start"]
