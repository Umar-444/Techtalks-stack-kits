---
name: fasthttp-buffer-management
description: Rules and memory patterns for safely handling Fasthttp zero-allocation byte buffers in Go Fiber.
---
# Fasthttp Buffer Management Skill

## 1. The Core Hazard
Fasthttp recycles internal request buffers as soon as a handler finishes. Retaining string references or byte slices across request boundaries or into background goroutines causes silent memory corruption and data races.

## 2. Safe Copy Patterns
```go
// WRONG - Dangerous pointer reuse!
go func() {
    log.Println(c.Params("id")) // Race condition!
}()

// CORRECT - Explicit memory copy
idCopy := strings.Clone(c.Params("id"))
go func() {
    log.Println(idCopy) // Safe!
}()
```

## 3. Parsing Request Bodies
Always parse bodies into concrete structs via `c.BodyParser(&target)` rather than holding references to `c.Body()`.

## 4. Done Means
- `go test -race ./...` passes with zero data race detections under concurrency load.
