---
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
