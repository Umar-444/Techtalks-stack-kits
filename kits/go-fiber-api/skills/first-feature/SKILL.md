---
name: first-feature
description: Guide to adding a high-throughput API endpoint in Go Fiber with request validation, buffer copying, and JSON envelope.
---
# First Feature Skill: Adding an Ingestion Telemetry Endpoint

## 1. Define Request DTO
```go
type TelemetryBatchRequest struct {
    DeviceID  string                 `json:"device_id"`
    Timestamp int64                  `json:"timestamp"`
    Metrics   map[string]interface{} `json:"metrics"`
}
```

## 2. Implement Fiber Handler
```go
func (h *Handler) IngestTelemetry(c *fiber.Ctx) error {
    var req TelemetryBatchRequest
    if err := c.BodyParser(&req); err != nil {
        return c.Status(fiber.StatusUnprocessableEntity).JSON(fiber.Map{
            "error": "invalid telemetry payload",
        })
    }
    
    // Buffer safety: copy deviceID if passing across goroutines
    deviceID := utils.CopyString(req.DeviceID)
    
    go func(id string, metrics map[string]interface{}) {
        h.processAsyncMetrics(id, metrics)
    }(deviceID, req.Metrics)
    
    return c.Status(fiber.StatusAccepted).JSON(fiber.Map{
        "status": "queued",
        "device_id": req.DeviceID,
    })
}
```

## 3. Register Route
```go
api := app.Group("/api/v1")
api.Post("/telemetry", h.IngestTelemetry)
```

## 4. Done Means
- String values are copied before passing into background goroutines.
- Handler returns HTTP 202 Accepted on success.
- Test verifies response code and payload assertions.
