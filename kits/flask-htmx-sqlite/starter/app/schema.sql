DROP TABLE IF EXISTS items;

CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT NOT NULL DEFAULT 'general',
    completed BOOLEAN NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_items_category ON items(category);
CREATE INDEX idx_items_created_at ON items(created_at);

-- Seed initial records
INSERT INTO items (title, description, category, completed) VALUES
    ('Initialize SQLite WAL Mode', 'Execute PRAGMA journal_mode = WAL to enable non-blocking readers', 'database', 1),
    ('Setup HTMX 2.0 Partial Render', 'Implement request.headers.get("HX-Request") dual render pattern', 'frontend', 1),
    ('Configure Flask-WTF CSRF', 'Inject X-CSRFToken into htmx:configRequest event header', 'security', 0);
