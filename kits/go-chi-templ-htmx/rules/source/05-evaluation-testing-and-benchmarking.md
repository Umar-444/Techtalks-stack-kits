---
id: "05-evaluation-testing-and-benchmarking"
title: "Testing, Container Hardening & Token Benchmark"
description: "Testing standards using standard library httptest, non-root Docker hardening (UID 10001), and token-light efficiency verification."
globs: ["**/*_test.go", "Dockerfile", "evals/**"]
alwaysApply: true
---

# 05 - Testing, Container Hardening & Token Benchmark

## 1. Unit & Handler Testing with httptest
- Test Chi routes and handlers using standard library `net/http/httptest`:
  ```go
  func TestHealthEndpoint(t *testing.T) {
      req := httptest.NewRequest("GET", "/health", nil)
      rec := httptest.NewRecorder()

      router := setupRouter()
      router.ServeHTTP(rec, req)

      if rec.Code != http.StatusOK {
          t.Fatalf("expected status 200, got %d", rec.Code)
      }
      body := rec.Body.String()
      if !strings.Contains(body, `"status":"ok"`) {
          t.Errorf("unexpected body: %s", body)
      }
  }
  ```
- Fast execution invariant: All unit and handler tests must complete in under 500ms without spinning up full external network dependencies.

## 2. Container Hardening & Unprivileged Execution
- Build using multi-stage Alpine images, compiling a static Go binary with CGO disabled:
  ```dockerfile
  FROM golang:1.23-alpine AS builder
  WORKDIR /build
  COPY go.mod go.sum ./
  RUN go mod download
  COPY . .
  RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o server ./main.go

  FROM alpine:3.20 AS runner
  RUN addgroup -g 10001 appgroup && adduser -u 10001 -G appgroup -D -s /bin/sh appuser
  COPY --from=builder --chown=10001:10001 /build/server /app/server
  USER 10001:10001
  EXPOSE 8080
  CMD ["/app/server"]
  ```
- Explicit `USER 10001:10001` directive is strictly required to satisfy Semgrep container security policies.

## 3. The Token-Light Flagship Metric (Document 20 Part F)
- Benchmark verification: Run `python evals/runner.py --kit go-chi-templ-htmx`.
- The kit must maintain:
  - Median build token target: ~16,800 tokens.
  - Efficiency Tier: **A+ (Token-Light Verified)**.
  - Justification: Chi standard library `net/http` ergonomics, `templ` compile-time type checking, and `sqlc` codegen require minimal code output from LLM agents to achieve full end-to-end features.
