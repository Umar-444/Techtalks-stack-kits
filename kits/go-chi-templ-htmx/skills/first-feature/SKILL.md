---
name: "first-feature"
description: "Scaffold a complete end-to-end feature: parameterized query in sqlc, type-safe templ component, and Chi handler returning reactive HTMX partials."
---

# Skill: First Feature - Scaffolding with templ, sqlc & HTMX

Follow this workflow to add a new full-stack feature with type safety from SQL to HTML.

## Step 1: Define Table Schema & SQL Query
Add the task item query to `query.sql`:
```sql
-- name: CreateItem :one
INSERT INTO items (title, done, created_at)
VALUES ($1, false, NOW())
RETURNING id, title, done, created_at;

-- name: ListItems :many
SELECT id, title, done, created_at
FROM items
ORDER BY created_at DESC;
```

Run `sqlc generate` to produce type-safe Go structs and query methods.

## Step 2: Build the Type-Safe templ Component
Create `views/items.templ`:
```html
package views

import "starter/internal/db"
import "fmt"

templ ItemRow(item db.Item) {
    <tr id={ fmt.Sprintf("item-%d", item.ID) } class="border-b border-border">
        <td class="p-3">{ item.Title }</td>
        <td class="p-3">
            if item.Done {
                <span class="badge badge-success">Done</span>
            } else {
                <span class="badge badge-warning">Pending</span>
            }
        </td>
        <td class="p-3">
            <button 
                hx-delete={ fmt.Sprintf("/items/%d", item.ID) }
                hx-target={ fmt.Sprintf("#item-%d", item.ID) }
                hx-swap="outerHTML"
                class="text-red-500 hover:underline">
                Delete
            </button>
        </td>
    </tr>
}
```

Run `templ generate` to compile template into Go code.

## Step 3: Register Chi Route Handler
In `main.go` or `internal/handler/`:
```go
r.Post("/items", func(w http.ResponseWriter, r *http.Request) {
    title := r.FormValue("title")
    if title == "" {
        http.Error(w, "Title is required", http.StatusBadRequest)
        return
    }

    item, err := queries.CreateItem(r.Context(), title)
    if err != nil {
        http.Error(w, "Failed to save item", http.StatusInternalServerError)
        return
    }

    // Render only the newly created table row for HTMX insertion
    views.ItemRow(item).Render(r.Context(), w)
})
```

## Step 4: Verify with Curl
```bash
curl -X POST http://localhost:8080/items \
  -H "HX-Request: true" \
  -d "title=Complete+Token+Light+Benchmark"
```
Returns HTML partial `<tr id="item-1">...</tr>` ready for immediate DOM swap.
