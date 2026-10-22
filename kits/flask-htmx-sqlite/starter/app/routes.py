from flask import Blueprint, render_template, request, jsonify, abort
from app.db import get_db

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    db = get_db()
    items = db.execute("SELECT * FROM items ORDER BY created_at DESC").fetchall()
    return render_template("index.html", items=items)

@main_bp.route("/health")
def health():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("PRAGMA journal_mode;")
    mode = cursor.fetchone()[0]
    cursor.close()
    return jsonify({
        "status": "ok",
        "journal_mode": mode,
        "token_light": True,
        "engine": "sqlite"
    })

@main_bp.route("/items", methods=["GET", "POST"])
def items():
    db = get_db()
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "general").strip()
        
        if not title:
            return "<div class='alert error'>Title is required</div>", 400
        
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO items (title, description, category, completed) VALUES (?, ?, ?, 0)",
            (title, description, category)
        )
        item_id = cursor.lastrowid
        db.commit()
        
        item = db.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        
        # When triggered by HTMX, return only the rendered partial item row
        if request.headers.get("HX-Request") == "true":
            return render_template("partials/item_row.html", item=item), 201
        
        # Fallback to direct page render
        items = db.execute("SELECT * FROM items ORDER BY created_at DESC").fetchall()
        return render_template("index.html", items=items)
    
    # GET request with optional search filter
    search = request.args.get("q", "").strip()
    if search:
        query = "%" + search + "%"
        items = db.execute(
            "SELECT * FROM items WHERE title LIKE ? OR description LIKE ? ORDER BY created_at DESC",
            (query, query)
        ).fetchall()
    else:
        items = db.execute("SELECT * FROM items ORDER BY created_at DESC").fetchall()
        
    if request.headers.get("HX-Request") == "true":
        return render_template("partials/item_list.html", items=items)
    
    return render_template("index.html", items=items)

@main_bp.route("/items/<int:item_id>/toggle", methods=["POST"])
def toggle_item(item_id):
    db = get_db()
    item = db.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    if not item:
        abort(404)
        
    new_status = 0 if item["completed"] else 1
    db.execute("UPDATE items SET completed = ? WHERE id = ?", (new_status, item_id))
    db.commit()
    
    updated_item = db.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    return render_template("partials/item_row.html", item=updated_item)

@main_bp.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    db = get_db()
    db.execute("DELETE FROM items WHERE id = ?", (item_id,))
    db.commit()
    # Empty string response allows HTMX hx-swap="outerHTML" to clean remove element from DOM
    return "", 200
