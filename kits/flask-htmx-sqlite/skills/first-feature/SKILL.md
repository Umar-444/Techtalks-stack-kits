---
name: first-feature
description: Guide to implementing an end-to-end reactive feature using Flask blueprints, Jinja2 partials, and HTMX 2.0 DOM swaps.
---
# First Feature Skill: Building an HTMX Reactive Feature in Flask

## 1. Define the Data Schema
Add the table definition to `app/schema.sql`:
```sql
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

## 2. Implement the Blueprint Route
In `app/routes.py`, add the dual-rendering handler:
```python
@main_bp.route("/notes", methods=["GET", "POST"])
def notes():
    db = get_db()
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        body = request.form.get("body", "").strip()
        if not title:
            return "<div class='error'>Title is required</div>", 400
        
        cursor = db.execute("INSERT INTO notes (title, body) VALUES (?, ?) RETURNING id, title, body, created_at", (title, body))
        note = cursor.fetchone()
        db.commit()
        
        # HTMX partial swap returns only the new row
        return render_template("partials/note_card.html", note=note)

    notes = db.execute("SELECT * FROM notes ORDER BY created_at DESC").fetchall()
    if request.headers.get("HX-Request") == "true":
        return render_template("partials/notes_list.html", notes=notes)
    return render_template("notes.html", notes=notes)
```

## 3. Create the Jinja2 Partial
In `app/templates/partials/note_card.html`:
```html
<article id="note-{{ note['id'] }}" class="note-card">
    <h3>{{ note['title'] }}</h3>
    <p>{{ note['body'] }}</p>
    <button hx-delete="/notes/{{ note['id'] }}"
            hx-target="#note-{{ note['id'] }}"
            hx-swap="outerHTML swap:500ms"
            class="btn-delete">
        Delete
    </button>
</article>
```

## 4. Hook up the HTMX Trigger Form
In `app/templates/notes.html`:
```html
<form hx-post="/notes"
      hx-target="#notes-container"
      hx-swap="afterbegin"
      hx-on::after-request="if(event.detail.successful) this.reset()">
    <input type="text" name="title" placeholder="Note title" required />
    <textarea name="body" placeholder="Note body"></textarea>
    <button type="submit">Create Note</button>
</form>
<div id="notes-container">
    {% for note in notes %}
        {% include "partials/note_card.html" %}
    {% endfor %}
</div>
```
