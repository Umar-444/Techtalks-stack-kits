"""Controls declared in security/checks.json, proved against the running app.

Runs in-process with Litestar's test client; the item store is in-memory, so no
PostgreSQL or Redis is needed. Controls that need those services (SEC-09,
SEC-11) have no code in the starter to test and are not asserted here.
"""

import ast
import json
import os
import re

import pytest
import yaml
from litestar.testing import AsyncTestClient

from app.main import app, cors_config

STARTER = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KIT = os.path.abspath(os.path.join(STARTER, ".."))


def _read(*parts):
    with open(os.path.join(STARTER, *parts), encoding="utf-8") as handle:
        return handle.read()


async def _create(client, tenant, title="Record"):
    res = await client.post("/api/v1/items", json={"title": title, "tenant_id": tenant})
    assert res.status_code == 201
    return res.json()["id"]


# --- SEC-04: tenant isolation (BOLA) ---------------------------------------

async def test_foreign_tenant_cannot_read_item():
    async with AsyncTestClient(app=app) as client:
        item_id = await _create(client, "tenant-a")
        assert (await client.get(f"/api/v1/items/{item_id}?tenant_id=tenant-b")).status_code == 404
        assert (await client.get(f"/api/v1/items/{item_id}?tenant_id=tenant-a")).status_code == 200


async def test_foreign_id_is_indistinguishable_from_missing_id():
    """404 for both, so a caller cannot probe which ids exist."""
    async with AsyncTestClient(app=app) as client:
        item_id = await _create(client, "tenant-a")
        foreign = await client.get(f"/api/v1/items/{item_id}?tenant_id=tenant-b")
        missing = await client.get("/api/v1/items/999999?tenant_id=tenant-b")
        assert foreign.status_code == missing.status_code == 404
        assert foreign.json() == missing.json()


async def test_get_requires_tenant_id():
    async with AsyncTestClient(app=app) as client:
        item_id = await _create(client, "tenant-a")
        assert (await client.get(f"/api/v1/items/{item_id}")).status_code == 400


async def test_list_is_scoped_to_tenant():
    async with AsyncTestClient(app=app) as client:
        await _create(client, "tenant-list-a", "only-a")
        await _create(client, "tenant-list-b", "only-b")
        titles = {i["title"] for i in (await client.get("/api/v1/items?tenant_id=tenant-list-a")).json()}
        assert "only-a" in titles and "only-b" not in titles


async def test_list_without_tenant_does_not_dump_every_tenant():
    async with AsyncTestClient(app=app) as client:
        await _create(client, "tenant-x")
        res = await client.get("/api/v1/items")
        assert res.status_code == 400, "unscoped listing must be refused, not return all tenants"


# --- SEC-05: DTO rejects unknown fields ------------------------------------

async def test_unknown_field_is_rejected():
    async with AsyncTestClient(app=app) as client:
        res = await client.post(
            "/api/v1/items",
            json={"title": "x", "tenant_id": "t", "is_active": False, "id": 1},
        )
        assert res.status_code == 400


@pytest.mark.parametrize("payload", [
    {"title": "", "tenant_id": "t"},
    {"title": "x" * 201, "tenant_id": "t"},
    {"title": "x", "tenant_id": "t" * 65},
    {"title": "x", "tenant_id": "t", "description": "d" * 1001},
])
async def test_length_bounds_enforced(payload):
    async with AsyncTestClient(app=app) as client:
        assert (await client.post("/api/v1/items", json=payload)).status_code == 400


# --- SEC-06: explicit CORS --------------------------------------------------

def test_cors_has_no_wildcard_origin():
    assert "*" not in cors_config.allow_origins


async def test_cors_allows_listed_origin_and_not_others():
    async with AsyncTestClient(app=app) as client:
        ok = await client.get("/health", headers={"Origin": "http://localhost:3000"})
        assert ok.headers.get("access-control-allow-origin") == "http://localhost:3000"
        bad = await client.get("/health", headers={"Origin": "https://evil.example"})
        assert "access-control-allow-origin" not in bad.headers


def test_cors_origins_come_from_environment():
    assert 'os.getenv("ALLOWED_ORIGINS"' in _read("app", "main.py")


# --- SEC-07: rootless container --------------------------------------------

def test_dockerfile_runs_as_uid_10001():
    users = re.findall(r"^USER\s+(\S+)", _read("Dockerfile"), re.M)
    assert users, "no USER directive"
    assert users[-1].split(":")[0] == "10001", f"final USER is {users[-1]!r}"


# --- SEC-08: health probe ---------------------------------------------------

async def test_health_probe_reports_ok():
    async with AsyncTestClient(app=app) as client:
        res = await client.get("/health")
        assert res.status_code == 200 and res.json()["status"] == "ok"


def test_dockerfile_healthcheck_targets_health_route():
    match = re.search(r"HEALTHCHECK.*?CMD.*", _read("Dockerfile"), re.S)
    assert match and "/health" in match.group(0)


# --- SEC-10: no exception disclosure ---------------------------------------

def test_debug_mode_is_off():
    assert app.debug is False
    assert "debug=True" not in _read("app", "main.py").replace(" ", "")


async def test_unhandled_error_does_not_leak_internals():
    from litestar import Litestar, get

    @get("/boom")
    async def boom() -> None:
        raise RuntimeError("secret-internal-detail")

    async with AsyncTestClient(app=Litestar(route_handlers=[boom], debug=app.debug)) as client:
        res = await client.get("/boom")
        assert res.status_code == 500
        assert "secret-internal-detail" not in res.text
        assert "Traceback" not in res.text


# --- SEC-03: no string-built SQL -------------------------------------------

def test_no_string_built_sql_in_app():
    """Flags f-string / concatenated arguments to execute() or text()."""
    offenders = []
    for root, _, files in os.walk(os.path.join(STARTER, "app")):
        for name in files:
            if not name.endswith(".py"):
                continue
            with open(os.path.join(root, name), encoding="utf-8") as handle:
                tree = ast.parse(handle.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    fn = getattr(node.func, "attr", getattr(node.func, "id", ""))
                    if fn in {"execute", "text", "exec_driver_sql"} and node.args:
                        if isinstance(node.args[0], (ast.JoinedStr, ast.BinOp)):
                            offenders.append(f"{name}:{node.lineno}")
    assert not offenders, f"string-built SQL: {offenders}"


def test_sql_scanner_would_flag_string_built_sql():
    """Guards the scanner above against silently matching nothing."""
    tree = ast.parse('session.execute(f"SELECT * FROM t WHERE id={x}")')
    call = next(n for n in ast.walk(tree) if isinstance(n, ast.Call))
    assert isinstance(call.args[0], ast.JoinedStr) and call.func.attr == "execute"


# --- SEC-01 / SEC-02 / manifest --------------------------------------------

def test_semgrep_rules_are_valid():
    with open(os.path.join(KIT, "security", "semgrep.yml"), encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    assert data["rules"]
    for rule in data["rules"]:
        assert rule["id"] and rule["severity"] in {"ERROR", "WARNING", "INFO"}
        assert rule.get("pattern") or rule.get("patterns") or rule.get("pattern-either")


def test_gitleaks_extends_default_ruleset():
    with open(os.path.join(KIT, "security", "gitleaks.toml"), encoding="utf-8") as handle:
        assert "useDefault = true" in handle.read()


def test_manifest_total_matches_checks():
    with open(os.path.join(KIT, "security", "checks.json"), encoding="utf-8") as handle:
        data = json.load(handle)
    assert data["summary"]["total"] == len(data["checks"])
