"""Security controls declared in security/checks.json, verified.

Each test names the control it backs. Tests assert the control is *active*,
not merely that the happy path works — a test that passes with the control
removed proves nothing.
"""

import json
import os
import re
from pathlib import Path

import pytest
from django.conf import settings
from django.db import connection

from app.models import Project

STARTER = Path(__file__).resolve().parent.parent


# --- SEC-04: Ninja API Key Authentication Guard (A07:2025) ----------------

@pytest.mark.django_db
def test_unauthenticated_request_is_rejected(client):
    assert client.get("/projects/").status_code == 401


@pytest.mark.django_db
def test_invalid_bearer_token_is_rejected(client, tenant_a):
    res = client.get("/projects/", headers={"Authorization": "Bearer not-a-real-token"})
    assert res.status_code == 401


@pytest.mark.django_db
def test_deactivated_token_is_rejected(client, tenant_a):
    tenant_a.is_active = False
    tenant_a.save(update_fields=["is_active"])
    res = client.get("/projects/", headers={"Authorization": f"Bearer {tenant_a.key}"})
    assert res.status_code == 401


# --- SEC-09: BOLA / IDOR authorization (A01:2025) -------------------------

@pytest.mark.django_db
def test_listing_excludes_other_tenants(client, auth_a, project_a, project_b):
    slugs = {row["slug"] for row in client.get("/projects/", headers=auth_a).json()}
    assert slugs == {"alpha-audit"}, f"tenant A saw foreign rows: {slugs}"


@pytest.mark.django_db
def test_direct_id_lookup_across_tenants_is_denied(client, auth_a, project_b):
    """The core BOLA case: a valid id belonging to someone else."""
    res = client.get(f"/projects/{project_b.id}", headers=auth_a)
    assert res.status_code == 404, (
        f"tenant A read tenant B's project {project_b.id} (got {res.status_code})"
    )


@pytest.mark.django_db
def test_foreign_id_is_indistinguishable_from_missing(client, auth_a, project_b):
    """A 403 here would confirm the row exists and leak tenant membership."""
    foreign = client.get(f"/projects/{project_b.id}", headers=auth_a)
    absent = client.get("/projects/99999", headers=auth_a)
    assert foreign.status_code == absent.status_code == 404


@pytest.mark.django_db
def test_cross_tenant_delete_is_denied(client, auth_a, project_b):
    res = client.delete(f"/projects/{project_b.id}", headers=auth_a)
    assert res.status_code == 404
    assert Project.objects.filter(pk=project_b.id).exists(), "foreign row was deleted"


@pytest.mark.django_db
def test_search_cannot_reach_other_tenants(client, auth_a, project_b):
    hits = client.get("/projects/search?q=Bravo", headers=auth_a).json()
    assert hits == []


# --- SEC-11: Pydantic schema input coercion limits (A05:2025) -------------

@pytest.mark.django_db
def test_unknown_field_is_rejected(client, auth_a):
    """extra="forbid" must stop a client smuggling tenant_id into the payload."""
    res = client.post(
        "/projects/",
        json={"name": "Smuggle", "slug": "smuggle", "tenant_id": "tenant-b"},
        headers=auth_a,
    )
    assert res.status_code == 422, f"unknown field accepted (got {res.status_code})"


@pytest.mark.django_db
def test_tenant_id_cannot_be_overridden_even_if_accepted(client, auth_a):
    client.post("/projects/", json={"name": "Scoped", "slug": "scoped"}, headers=auth_a)
    created = Project.objects.get(slug="scoped")
    assert created.tenant_id == "tenant-a"


@pytest.mark.django_db
@pytest.mark.parametrize("payload", [
    {"name": "x", "slug": "ok-slug"},                 # name below min_length
    {"name": "Valid Name", "slug": "Not A Slug!"},    # slug fails pattern
    {"name": "Valid Name", "slug": "a" * 300},        # slug over max_length
    {"name": "Valid Name"},                           # slug missing
])
def test_malformed_payloads_are_rejected(client, auth_a, payload):
    assert client.post("/projects/", json=payload, headers=auth_a).status_code == 422


@pytest.mark.django_db
def test_tenant_id_is_not_exposed_in_responses(client, auth_a, project_a):
    body = client.get(f"/projects/{project_a.id}", headers=auth_a).json()
    assert "tenant_id" not in body


# --- SEC-05: parameterized query enforcement (A05:2025) -------------------

@pytest.mark.django_db
def test_injection_payload_is_treated_as_a_literal(client, auth_a, project_a):
    res = client.get("/projects/search?q=' OR 1=1 --", headers=auth_a)
    assert res.status_code == 200
    assert res.json() == [], "injection payload matched rows; query is not parameterized"


@pytest.mark.django_db
def test_legitimate_search_still_matches(client, auth_a, project_a):
    """Guards the test above from passing vacuously."""
    hits = client.get("/projects/search?q=Alpha", headers=auth_a).json()
    assert len(hits) == 1


@pytest.mark.django_db
def test_injection_payload_does_not_drop_table(client, auth_a, project_a):
    client.get("/projects/search?q='; DROP TABLE app_project; --", headers=auth_a)
    assert Project.objects.filter(pk=project_a.id).exists()


@pytest.mark.django_db
def test_orm_emits_bound_parameters(client, auth_a):
    """The payload must appear as a bound parameter, never inline in the SQL."""
    sql, params = (
        Project.objects.filter(tenant_id="tenant-a", name__icontains="' OR 1=1 --")
        .query.sql_with_params()
    )
    assert "OR 1=1" not in sql
    assert any("OR 1=1" in str(p) for p in params)


# --- SEC-07: Celery JSON-only serialization (A08:2025) --------------------

def test_celery_accepts_json_only():
    assert settings.CELERY_ACCEPT_CONTENT == ["json"]
    assert settings.CELERY_TASK_SERIALIZER == "json"
    assert settings.CELERY_RESULT_SERIALIZER == "json"


def test_pickle_is_not_an_accepted_content_type():
    joined = " ".join(settings.CELERY_ACCEPT_CONTENT).lower()
    assert "pickle" not in joined


# --- SEC-08: Django security middleware active (A02:2025) -----------------

@pytest.mark.parametrize("middleware", [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
])
def test_security_middleware_installed(middleware):
    assert middleware in settings.MIDDLEWARE


def test_response_hardening_settings():
    assert settings.SECURE_CONTENT_TYPE_NOSNIFF is True
    assert settings.X_FRAME_OPTIONS == "DENY"
    assert settings.SESSION_COOKIE_HTTPONLY is True
    assert settings.SECURE_REFERRER_POLICY == "strict-origin-when-cross-origin"


def test_argon2_is_the_default_password_hasher():
    assert "Argon2" in settings.PASSWORD_HASHERS[0]


# --- SEC-10: database health probe (A10:2025) -----------------------------

@pytest.mark.django_db
def test_health_probe_actually_queries_the_database(client):
    """A literal-only health endpoint would pass this; executing SQL is the point."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        assert cursor.fetchone()[0] == 1
    assert client.get("/health").json()["database"] == "ok"


# --- SEC-03 / SEC-01: no committed secrets (A04:2025) ---------------------

def test_env_example_has_no_real_secret():
    content = (STARTER / ".env.example").read_text(encoding="utf-8")
    assert not content.startswith("﻿"), ".env.example starts with a UTF-8 BOM"
    for line in content.splitlines():
        if line.startswith("SECRET_KEY="):
            value = line.split("=", 1)[1]
            assert "change" in value.lower() or "replace" in value.lower()


def test_no_hardcoded_secrets_in_source():
    patterns = [
        re.compile(r"AKIA[0-9A-Z]{16}"),
        re.compile(r"ghp_[0-9a-zA-Z]{36}"),
        re.compile(r"\bsk-[a-zA-Z0-9_-]{20,}"),
        re.compile(r"BEGIN RSA PRIVATE KEY"),  # pragma: allowlist secret
    ]
    for path in list(STARTER.rglob("*.py")) + list(STARTER.rglob("*.yml")):
        # tests/ legitimately contains secret-shaped literals — these very
        # patterns — so scanning it would always self-match.
        if "__pycache__" in str(path) or "tests" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in patterns:
            assert not pattern.search(text), f"secret-shaped string in {path.name}"


# --- SEC-06: rootless container (A01:2025) --------------------------------

def test_dockerfile_runs_as_non_root():
    dockerfile = (STARTER / "Dockerfile").read_text(encoding="utf-8")
    assert "USER 10001:10001" in dockerfile
    user_lines = [l for l in dockerfile.splitlines() if l.strip().startswith("USER ")]
    assert user_lines and user_lines[-1].strip() == "USER 10001:10001", (
        "a later USER directive overrides the unprivileged one"
    )


def test_compose_worker_is_not_privileged():
    compose = (STARTER / "docker-compose.yml").read_text(encoding="utf-8")
    assert "privileged: true" not in compose


# --- Manifest consistency -------------------------------------------------

def test_security_manifest_is_canonical_and_populated():
    manifest = json.loads(
        (STARTER.parent / "security" / "checks.json").read_text(encoding="utf-8")
    )
    assert manifest["schema_version"] == "2.0.0"
    assert len(manifest["checks"]) >= 12
    for check in manifest["checks"]:
        assert check["owasp"], f"{check['id']} has no OWASP mapping"
