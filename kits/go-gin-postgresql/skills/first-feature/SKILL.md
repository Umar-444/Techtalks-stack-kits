---
name: first-feature
description: Step-by-step workflow for creating a new resource in Go + Gin: SQL migration, sqlc query generation, service layer, and Gin router endpoint.
---
# First Feature Skill: Adding a Product Catalog Resource

## 1. Define SQL Schema Migration
In `db/migrations/001_create_products.sql`:
```sql
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price_cents INTEGER NOT NULL,
    sku VARCHAR(64) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

## 2. Author SQLC Queries
In `db/queries/products.sql`:
```sql
-- name: GetProductBySKU :one
SELECT * FROM products
WHERE sku = $1 LIMIT 1;

-- name: CreateProduct :one
INSERT INTO products (name, price_cents, sku)
VALUES ($1, $2, $3)
RETURNING *;
```
Generate type-safe Go structs:
```bash
sqlc generate
```

## 3. Wire Gin Handler
In `internal/handler/product.go`:
```go
type CreateProductRequest struct {
    Name       string `json:"name" binding:"required,min=2"`
    PriceCents int32  `json:"price_cents" binding:"required,gt=0"`
    SKU        string `json:"sku" binding:"required,alphanum"`
}

func (h *Handler) CreateProduct(c *gin.Context) {
    var req CreateProductRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusUnprocessableEntity, gin.H{"error": err.Error()})
        return
    }
    product, err := h.repo.CreateProduct(c.Request.Context(), req)
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "failed to create product"})
        return
    }
    c.JSON(http.StatusCreated, gin.H{"data": product})
}
```

## 4. Done Means
- Schema migration applies cleanly.
- `sqlc generate` produces zero type errors.
- Unit test verifies handler validation and 201 Created response.
