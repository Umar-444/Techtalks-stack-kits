---
name: "templ-component-architecture"
description: "Master advanced templ patterns: layout nesting, conditional rendering, loops, out-of-band swaps (hx-swap-oob), and context injection."
---

# Skill: templ Component Architecture and HTMX Composition

Use this skill to structure complex reactive UIs without JavaScript client bundles.

## 1. Base Layout & Component Slotting
Define an extensible base layout in `views/layout.templ`:
```html
package views

templ Layout(title string, body templ.Component) {
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>{ title } • TechTalks</title>
        <script src="https://unpkg.com/htmx.org@2.0.2"></script>
        <link rel="stylesheet" href="/static/style.css"/>
    </head>
    <body class="bg-[#FDFDFC] text-[#12140F]">
        <header class="border-b border-[#E6E6DF] p-4">
            <h1 class="text-xl font-bold">TechTalks Stack Kit</h1>
        </header>
        <main class="max-w-4xl mx-auto p-6">
            @body
        </main>
    </body>
    </html>
}
```

## 2. Dynamic Component Swapping (Full Page vs HTMX Fragment)
```go
func RenderPageOrFragment(w http.ResponseWriter, r *http.Request, title string, component templ.Component) {
    if r.Header.Get("HX-Request") == "true" {
        // HTMX request: render ONLY the targeted fragment
        component.Render(r.Context(), w)
    } else {
        // Direct browser visit: wrap inside full HTML shell
        views.Layout(title, component).Render(r.Context(), w)
    }
}
```

## 3. Atomic Out-of-Band Swaps
When an action updates both the primary target and an alert banner:
```html
package views

templ TaskCreatedResponse(task db.Task, totalCount int) {
    <!-- Primary swap into task list -->
    @TaskRow(task)

    <!-- Out-of-band swap into separate stats badge -->
    <span id="task-counter" hx-swap-oob="true" class="badge">
        { fmt.Sprintf("%d Total", totalCount) }
    </span>
}
```
