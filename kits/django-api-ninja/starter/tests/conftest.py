"""Shared fixtures.

Two tenants exist in every fixture set. A single-tenant fixture cannot prove
isolation: the scoping filter could be missing entirely and the tests would
still pass.
"""

import pytest
from django.contrib.auth import get_user_model
from ninja.testing import TestClient

from app.models import ApiToken, Project
from config.api import api


@pytest.fixture(scope="session")
def client():
    """One TestClient for the whole session.

    Django Ninja registers each NinjaAPI by version, so building a second
    TestClient over the same api raises ConfigError.
    """
    return TestClient(api)


@pytest.fixture
def tenant_a(db):
    # create() not create_user(): these tests authenticate by bearer token,
    # so hashing a password here would add a dependency they do not need.
    user = get_user_model().objects.create(username="alice")
    return ApiToken.objects.create(key="token-alpha", tenant_id="tenant-a", user=user)


@pytest.fixture
def tenant_b(db):
    user = get_user_model().objects.create(username="bob")
    return ApiToken.objects.create(key="token-bravo", tenant_id="tenant-b", user=user)


@pytest.fixture
def auth_a(tenant_a):
    return {"Authorization": f"Bearer {tenant_a.key}"}


@pytest.fixture
def auth_b(tenant_b):
    return {"Authorization": f"Bearer {tenant_b.key}"}


@pytest.fixture
def project_a(tenant_a):
    return Project.objects.create(
        name="Alpha Audit", slug="alpha-audit", tenant_id=tenant_a.tenant_id
    )


@pytest.fixture
def project_b(tenant_b):
    return Project.objects.create(
        name="Bravo Audit", slug="bravo-audit", tenant_id=tenant_b.tenant_id
    )
