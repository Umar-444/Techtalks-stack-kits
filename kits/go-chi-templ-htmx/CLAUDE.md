# Go + Chi + templ + HTMX + sqlc + PostgreSQL — Claude Code Guidelines (CLAUDE.md)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Quick Reference & Non-Negotiable Standards
### 01 Framework Architecture And Standards
﻿---
id: "01-framework-architecture-and-standards"
title: "Go & Chi Architecture Standards"
description: "Architectural standards for lightweight Go services using the Chi router, standard net/http compatibility, middleware composition, and clean domain packages."
globs: ["**/*.go", "go.mod", "Dockerfile", "docker-compose.yml"]
alwaysApply: true
---

# 01 - Go & Chi Architecture Standards

## 1. Architectural Philosophy & The Token-Light Flagship
- **100% net/http Compatibility:** The Chi router is a lightweight idiomatic routing framework for Go built directly on the standard library `net/http` primitives. It introduces zero external transport dependencies and ~1,000 lines of core routing code.
- **The Token-Light Line Standard:** Because Chi adheres strictly to standard `http.Handler` and `http.HandlerFunc` interfaces, AI agents write minimal boilerplate. Median build token consumption is verified at **16,800 tokens (Tier A+ Verified)**.
- **Explicit Lifecycle & Graceful Shutdown:** Every service must handle OS termination signals (`SIGINT`, `SIGTERM`) and execute graceful HTTP server shutdown using `context.WithTimeout`:
  ```go
  ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
  defer cancel()
  if err := srv.Shutdown(ctx); err != nil {
      log.Fatalf("Server forced to shutdown: %v", err)
  }
  ```

## 2. Directory Layout & Package Conventions
```
starter/
├── cmd/
│   └── server/
│       └── main.go                 # Process entrypoint, flag parsing, DI wiring
├── internal/
│   ├── handler/                    # Chi HTTP handlers, request decoding, response encoding
│   ├── db/                         # sqlc generated queries, database interface, migrations
│   └── views/                      # templ type-safe HTML templates and components
├── schema.sql                      # DDL source of truth for sqlc
├── query.sql                       # Parameterized queries for sqlc code generation
├── sqlc.yaml                       # sqlc code generation configuration
├── Dockerfile                      # Multi-stage unprivileged (UID 10001) Alpine container
├── docker-compose.yml              # Local Go + PostgreSQL 16 topology
└── go.mod                          # Go module definition
```

## 3. Middleware Stack Ordering
Compose middleware with intentional failure and tracing semantics:
```go
r := chi.NewRouter()

// 1. Tracing & Identification
r.Use(middleware.RequestID)
r.Use(middleware.RealIP)

// 2. Telemetry & Observability
r.Use(middleware.Logger)

// 3. Crash Resilience & Panic Safety
r.Use(middleware.Recoverer)

// 4. Request Lifetime Bounds
r.Use(middleware.Timeout(30 * time.Second))
```

## 4. Error Handling & HTTP Status Invariants
- Never panic in handler code; all errors must be returned to the caller or handled by `middleware.Recoverer`.
- Always set appropriate Content-Type before writing status codes (`w.Header().Set("Content-Type", "application/json")` or `text/html; charset=utf-8`).
- Never leak raw SQL query errors or file paths in HTTP error responses. Log the underlying error with `middleware.GetReqID(r.Context())` and return an opaque message with the request correlation ID.


### 02 Templ Components And Htmx Reactivity
﻿---
id: "02-templ-components-and-htmx-reactivity"
title: "templ Components & HTMX 2.0 Reactivity"
description: "Patterns for type-safe compile-time JSX HTML rendering with templ, component layout composition, and hypermedia interactions with HTMX 2.0."
globs: ["**/*.templ", "**/*.go"]
alwaysApply: true
---

# 02 - templ Components & HTMX 2.0 Reactivity

## 1. Compile-Time Type Safety with templ
- **Zero Runtime Reflection:** `templ` compiles `.templ` files into standard, highly optimized Go code. Syntax errors, broken variable references, and type mismatches fail the Go compiler build, eliminating runtime template errors.
- **Automatic Context Propagation:** Every `templ.Component` accepts `context.Context` as its first parameter, allowing seamless tracing, localization, and request correlation.
- **Component Rendering:** Render components directly to standard `http.ResponseWriter`:
  ```go
  func (h *UserHandler) List(w http.ResponseWriter, r *http.Request) {
      users, err := h.store.ListUsers(r.Context())
      if err != nil {
          http.Error(w, "Failed to load users", http.StatusInternalServerError)
          return
      }
      views.UserList(users).Render(r.Context(), w)
  }
  ```

## 2. HTMX 2.0 Request Detection & Selective Rendering
- Inspect the `HX-Request` header to distinguish full-page browser loads from asynchronous HTMX hypermedia partial requests:
  ```go
  func isHTMX(r *http.Request) bool {
      return r.Header.Get("HX-Request") == "true"
  }
  ```
- If `isHTMX(r)` is true, render only the target fragment (`views.UserTableRow(user)`). If false, render the full outer layout (`views.Layout("Users", views.UserTable(users))`). This provides instant client-side responsiveness while preserving full SEO, bookmarking, and direct URL navigation.

## 3. Idiomatic HTMX Attributes
- Use explicit HTMX attributes for declarative interaction:
  - `hx-get="/api/items"`: Hypermedia polling or filtered fetching.
  - `hx-post="/api/items"`: Form submission without full page reload.
  - `hx-target="#item-list"`: Explicit DOM insertion container.
  - `hx-swap="beforeend"` / `hx-swap="outerHTML"`: DOM mutation strategy.
  - `hx-indicator="#loading-spinner"`: Visual request progress indicator.
- **Out-of-Band Swaps:** Use `hx-swap-oob="true"` on alert banners or counter badges to update multiple disconnected parts of the DOM in a single atomic HTTP response.

## 4. XSS Immunity & Auto-Escaping
- `templ` automatically contextual-escapes all dynamic variables interpolated within HTML tags, attributes, and text nodes.
- Never bypass escaping with `templ.Raw()` unless rendering trusted, pre-sanitized markdown from a cryptographically signed source.


### 03 Sqlc Queries And Pgx Pooling
﻿---
id: "03-sqlc-queries-and-pgx-pooling"
title: "sqlc Type-Safe Queries & pgx Connection Pooling"
description: "SQL-first development standards using sqlc code generation, compile-checked query verification, and PostgreSQL connection pool management via pgxpool."
globs: ["**/*.sql", "**/*.go", "sqlc.yaml"]
alwaysApply: true
---

# 03 - sqlc Type-Safe Queries & pgx Connection Pooling

## 1. SQL-First Development with sqlc
- **Zero ORM Magic:** Avoid heavy ORMs (like GORM) that generate unpredictable, slow N+1 SQL queries via runtime reflection. Write clean, readable, standard PostgreSQL in `schema.sql` and `query.sql`.
- **Compile-Checked Queries:** `sqlc generate` parses DDL and raw SQL queries, verifies schema validity, checks column data types, and emits idiomatic, type-safe Go structs and repository methods.
- **Annotated Queries:** Every query in `query.sql` must have an explicit sqlc comment annotation declaring the method name and result cardinality:
  ```sql
  -- name: GetUserByID :one
  SELECT id, email, full_name, created_at
  FROM users
  WHERE id = $1;

  -- name: ListUsers :many
  SELECT id, email, full_name, created_at
  FROM users
  ORDER BY created_at DESC
  LIMIT $1 OFFSET $2;

  -- name: CreateUser :one
  INSERT INTO users (email, full_name)
  VALUES ($1, $2)
  RETURNING id, email, full_name, created_at;
  ```

## 2. PostgreSQL Connection Pooling with pgxpool
- Connect to PostgreSQL using `github.com/jackc/pgx/v5/pgxpool`:
  ```go
  config, err := pgxpool.ParseConfig(databaseURL)
  if err != nil {
      log.Fatalf("Unable to parse DB config: %v", err)
  }
  config.MaxConns = 25
  config.MinConns = 5
  config.MaxConnLifetime = 1 * time.Hour
  config.MaxConnIdleTime = 30 * time.Minute

  pool, err := pgxpool.NewWithConfig(ctx, config)
  if err != nil {
      log.Fatalf("Unable to create connection pool: %v", err)
  }
  defer pool.Close()
  ```
- Pass `pool` directly into `db.New(pool)` to instantiate the sqlc repository.

## 3. Transaction Safety
- Always wrap multi-statement write operations inside a transaction:
  ```go
  tx, err := pool.Begin(ctx)
  if err != nil {
      return err
  }
  defer tx.Rollback(ctx)

  qtx := queries.WithTx(tx)
  if err := qtx.CreateOrder(ctx, orderParams); err != nil {
      return err
  }
  if err := qtx.DeductInventory(ctx, itemParams); err != nil {
      return err
  }
  return tx.Commit(ctx)
  ```


### 04 Api Security And Input Validation
﻿---
id: "04-api-security-and-input-validation"
title: "API Security & OWASP Defense in Go"
description: "Security invariants covering input validation, parameterized SQL injection prevention, BOLA/IDOR protection, and CSRF defense in Chi & HTMX."
globs: ["**/*.go", "**/*.sql"]
alwaysApply: true
---

# 04 - API Security & OWASP Defense in Go

## 1. Zero SQL Injection by Construction
- `sqlc` generates strictly parameterized queries (`$1, $2, ...`) for all database operations.
- Never construct dynamic SQL via string interpolation (`fmt.Sprintf("SELECT * FROM users WHERE name = '%s'", input)`). String concatenation in SQL statements is strictly rejected during security auditing.

## 2. Broken Object Level Authorization (BOLA/IDOR) Defense
- Always enforce tenant and user ownership checks at the query layer rather than in application memory.
- In every parameterized query accessing customer data, include the tenant ID:
  ```sql
  -- name: GetDocumentForTenant :one
  SELECT id, title, content, tenant_id
  FROM documents
  WHERE id = $1 AND tenant_id = $2;
  ```
- If no record matches both `$1` (resource ID) and `$2` (authenticated tenant ID), return an immediate `404 Not Found` or `403 Forbidden`.

## 3. CSRF Protection for HTMX Requests
- For state-mutating requests (`POST`, `PUT`, `DELETE`), generate an encrypted anti-CSRF token per session.
- Configure HTMX to include the CSRF token in all outgoing requests automatically:
  ```html
  <body hx-headers='{"X-CSRF-Token": "{{ .CSRFToken }}"}'>
  ```
- Validate the token in Chi middleware before executing any mutation handler.

## 4. Rate Limiting & Denial of Service Defense
- Protect login and resource-heavy endpoints using token bucket rate limiting (e.g., `golang.org/x/time/rate` or Chi middleware).
- Limit maximum request body size to prevent memory exhaustion attacks:
  ```go
  r.Body = http.MaxBytesReader(w, r.Body, 10<<20) // 10MB limit
  ```


### 05 Evaluation Testing And Benchmarking
﻿---
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


