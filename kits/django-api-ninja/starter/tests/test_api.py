import pytest
from ninja.testing import TestClient
from config.api import api
from app.models import Project

client = TestClient(api)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

@pytest.mark.django_db
def test_create_and_list_project():
    res = client.post("/projects/", json={"name": "Cloud Security", "slug": "cloud-sec", "description": "Audit"})
    assert res.status_code == 201
    assert res.json()["slug"] == "cloud-sec"
    
    list_res = client.get("/projects/")
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1
