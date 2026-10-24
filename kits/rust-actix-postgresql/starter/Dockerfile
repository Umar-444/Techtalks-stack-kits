# Multi-stage production container for Rust + Actix Web + SeaORM + PostgreSQL
FROM rust:1.81-alpine AS builder

WORKDIR /app

RUN apk add --no-cache musl-dev gcc make openssl-dev postgresql-dev

COPY Cargo.toml ./
RUN mkdir src && echo "pub fn dummy() {}" > src/lib.rs && echo "fn main() {}" > src/main.rs && cargo build --release || true

COPY . .
RUN cargo build --release

FROM alpine:3.20 AS final

WORKDIR /app

RUN apk add --no-cache ca-certificates tzdata libpq && \
    addgroup -S appgroup -g 10001 && \
    adduser -S appuser -u 10001 -G appgroup

COPY --from=builder /app/target/release/rust_actix_postgresql_starter /app/server

USER 10001:10001

EXPOSE 8080

HEALTHCHECK --interval=5s --timeout=3s --retries=3 \
  CMD wget --spider -q http://localhost:8080/healthz || exit 1

CMD ["/app/server"]
