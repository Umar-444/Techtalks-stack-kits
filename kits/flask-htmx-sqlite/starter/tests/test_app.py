import os
import tempfile
import pytest
from app import create_app
from app.db import init_db, get_db

@pytest.fixture
def app():
    """Create and configure a clean test app with isolated temporary SQLite DB."""
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        "TESTING": True,
        "DATABASE": db_path,
        "WTF_CSRF_ENABLED": False,  # Disabled for unit client tests
        "SECRET_KEY": "test-secret-key-32-chars-at-least-abcdef",
    })
    
    with app.app_context():
        init_db()
        
    yield app
    
    os.close(db_fd)
    if os.path.exists(db_path):
        os.unlink(db_path)

@pytest.fixture
def client(app):
    """Test client fixture."""
    return app.test_client()

def test_health_check_endpoint(client):
    """Verify health endpoint reports ok status and WAL journal mode."""
    res = client.get("/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "ok"
    assert data["journal_mode"] == "wal"
    assert data["token_light"] is True

def test_full_page_render_vs_htmx_partial(client):
    """Verify dual rendering pattern: full page on standard GET, partial on HX-Request."""
    # 1. Standard browser navigation (full page)
    full_res = client.get("/")
    assert full_res.status_code == 200
    assert b"<!DOCTYPE html>" in full_res.data
    assert b"<html" in full_res.data
    assert b"Data Management Dashboard" in full_res.data
    
    # 2. HTMX partial request
    partial_res = client.get("/items", headers={"HX-Request": "true"})
    assert partial_res.status_code == 200
    assert b"<!DOCTYPE html>" not in partial_res.data
    assert b"<html" not in partial_res.data
    assert b"class=\"item-row" in partial_res.data

def test_create_item_htmx(client):
    """Test creating an item with HTMX partial response."""
    res = client.post("/items", data={
        "title": "Automated Test Item",
        "description": "Created during pytest execution",
        "category": "security"
    }, headers={"HX-Request": "true"})
    
    assert res.status_code == 201
    assert b"Automated Test Item" in res.data
    assert b"tag-security" in res.data

def test_create_item_validation(client):
    """Test creating an item without required title fails with 400."""
    res = client.post("/items", data={"title": ""}, headers={"HX-Request": "true"})
    assert res.status_code == 400
    assert b"Title is required" in res.data

def test_toggle_and_delete_item(client):
    """Test item status toggle and delete endpoints."""
    # Create item
    res = client.post("/items", data={"title": "Item To Delete", "category": "database"}, headers={"HX-Request": "true"})
    assert res.status_code == 201
    
    # Toggle item
    toggle_res = client.post("/items/1/toggle", headers={"HX-Request": "true"})
    assert toggle_res.status_code == 200
    
    # Delete item
    del_res = client.delete("/items/1", headers={"HX-Request": "true"})
    assert del_res.status_code == 200
    assert del_res.data == b""
