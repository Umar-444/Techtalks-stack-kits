import pytest

from app.models import Project


def test_health_reports_database_reachable(client, db):
    res = client.get("/health")
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "healthy"
    assert body["database"] == "ok"


@pytest.mark.django_db
def test_create_and_list_project(client, auth_a):
    res = client.post(
        "/projects/",
        json={"name": "Cloud Security", "slug": "cloud-sec", "description": "Audit"},
        headers=auth_a,
    )
    assert res.status_code == 201, res.content
    assert res.json()["slug"] == "cloud-sec"

    listing = client.get("/projects/", headers=auth_a)
    assert listing.status_code == 200
    assert len(listing.json()) == 1


@pytest.mark.django_db
def test_get_project_by_id(client, auth_a, project_a):
    res = client.get(f"/projects/{project_a.id}", headers=auth_a)
    assert res.status_code == 200
    assert res.json()["slug"] == "alpha-audit"


@pytest.mark.django_db
def test_delete_project(client, auth_a, project_a):
    assert client.delete(f"/projects/{project_a.id}", headers=auth_a).status_code == 204
    assert not Project.objects.filter(pk=project_a.id).exists()


@pytest.mark.django_db
def test_duplicate_slug_within_tenant_is_rejected(client, auth_a, project_a):
    res = client.post(
        "/projects/", json={"name": "Dupe", "slug": "alpha-audit"}, headers=auth_a
    )
    assert res.status_code == 409


@pytest.mark.django_db
def test_same_slug_allowed_across_tenants(client, auth_b, project_a):
    """Slug uniqueness is per tenant, so tenant B may reuse tenant A's slug."""
    res = client.post(
        "/projects/", json={"name": "Bravo", "slug": "alpha-audit"}, headers=auth_b
    )
    assert res.status_code == 201


@pytest.mark.django_db
def test_pagination_limit_is_clamped(client, auth_a):
    for i in range(5):
        Project.objects.create(name=f"P{i}", slug=f"p-{i}", tenant_id="tenant-a")
    res = client.get("/projects/?limit=9999", headers=auth_a)
    assert res.status_code == 200
    assert len(res.json()) <= 100
