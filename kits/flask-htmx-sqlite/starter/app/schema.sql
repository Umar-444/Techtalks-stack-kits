DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS audit_log;

CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT NOT NULL DEFAULT 'general',
    completed BOOLEAN NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id TEXT,
    action TEXT NOT NULL,
    entity TEXT NOT NULL,
    entity_id TEXT,
    detail TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_log_entity ON audit_log(entity, entity_id);
CREATE INDEX idx_audit_log_created_at ON audit_log(created_at);

CREATE INDEX idx_items_category ON items(category);
CREATE INDEX idx_items_created_at ON items(created_at);

-- Seed initial records
INSERT INTO items (title, description, category, completed) VALUES
    ('Initialize SQLite WAL Mode', 'Execute PRAGMA journal_mode = WAL to enable non-blocking readers', 'database', 1),
    ('Setup HTMX 2.0 Partial Render', 'Implement request.headers.get("HX-Request") dual render pattern', 'frontend', 1),
    ('Configure Flask-WTF CSRF', 'Inject X-CSRFToken into htmx:configRequest event header', 'security', 0);
