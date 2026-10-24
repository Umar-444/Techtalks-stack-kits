"""Controls declared in security/checks.json, proved against the running app.

Everything is in-process: the starter's search tool is deterministic and the
graph is pure Python, so no LLM, Redis or network is involved.

Declared in checks.json but NOT asserted here because the starter has no code
for them: SEC-04 (prompt-injection sanitisation), SEC-07 (Redis state
serialisation), SEC-09 (PII redaction) and the *whitelist* half of SEC-08 (the
app mounts no CORS middleware at all, which is asserted to be closed by default).
"""

import ast
import json
import os
import re

import pytest
import yaml
from fastapi.testclient import TestClient
from langgraph.errors import GraphRecursionError
from langgraph.graph import END, StateGraph

import app.main as app_main
from app.graph import create_agent_graph, router_condition
from app.state import AgentState
from app.tools import sandboxed_search

STARTER = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KIT = os.path.abspath(os.path.join(STARTER, ".."))
client = TestClient(app_main.app, raise_server_exceptions=False)


def _read(*parts):
    with open(os.path.join(STARTER, *parts), encoding="utf-8") as handle:
        return handle.read()


def _spinning_graph():
    """A graph that never reaches END, to prove the recursion ceiling holds."""

    def spin(state: AgentState) -> dict:
        return {"iteration_count": state.get("iteration_count", 0) + 1}

    workflow = StateGraph(AgentState)
    workflow.add_node("spin", spin)
    workflow.set_entry_point("spin")
    workflow.add_conditional_edges("spin", lambda s: "again", {"again": "spin", "stop": END})
    return workflow.compile()


INITIAL = {"query": "q", "research_notes": [], "synthesized_report": "", "iteration_count": 0, "is_satisfactory": False}


# --- SEC-06: recursive cycle limit -----------------------------------------

def test_recursion_limit_is_bounded():
    assert 1 <= app_main.RECURSION_LIMIT <= 50


def test_runaway_graph_is_stopped_at_the_limit():
    with pytest.raises(GraphRecursionError):
        _spinning_graph().invoke(INITIAL, {"recursion_limit": app_main.RECURSION_LIMIT})


def test_endpoint_passes_the_limit_to_the_graph(monkeypatch):
    seen = {}

    class Spy:
        def invoke(self, state, config):
            seen.update(config)
            return {"synthesized_report": "r", "iteration_count": 1}

    monkeypatch.setattr(app_main, "graph_app", Spy())
    assert client.post("/api/v1/run-agent", json={"query": "valid query"}).status_code == 200
    assert seen == {"recursion_limit": app_main.RECURSION_LIMIT}


def test_runaway_graph_through_the_api_fails_closed(monkeypatch):
    monkeypatch.setattr(app_main, "graph_app", _spinning_graph())
    res = client.post("/api/v1/run-agent", json={"query": "valid query"})
    assert res.status_code == 500
    assert "recursion" not in res.text.lower()


def test_router_stops_after_three_iterations_even_if_unsatisfied():
    assert router_condition({"iteration_count": 3, "is_satisfactory": False}) == "end"
    assert router_condition({"iteration_count": 1, "is_satisfactory": False}) == "synthesize"
    assert router_condition({"iteration_count": 1, "is_satisfactory": True}) == "end"


def test_real_graph_terminates_with_a_report():
    result = create_agent_graph().invoke(INITIAL, {"recursion_limit": 10})
    assert "Synthesized Intelligence Report" in result["synthesized_report"]


# --- SEC-11: strict input validation ---------------------------------------

@pytest.mark.parametrize("payload", [
    {},
    {"query": ""},
    {"query": "ab"},
    {"query": "x" * 501},
    {"query": 123},
    {"query": None},
    {"query": "valid query", "recursion_limit": 9999},
    {"query": "valid query", "is_satisfactory": True},
])
def test_invalid_payloads_are_rejected(payload):
    assert client.post("/api/v1/run-agent", json=payload).status_code == 422


def test_boundary_lengths_are_accepted():
    assert client.post("/api/v1/run-agent", json={"query": "abc"}).status_code == 200
    assert client.post("/api/v1/run-agent", json={"query": "x" * 500}).status_code == 200


# --- SEC-05: tool sandboxing ------------------------------------------------

FORBIDDEN_IMPORTS = {"os", "subprocess", "socket", "requests", "httpx", "urllib", "shutil", "pathlib", "ctypes", "pickle"}
FORBIDDEN_CALLS = {"eval", "exec", "open", "compile", "__import__", "system", "popen"}


def test_search_tool_imports_nothing_that_can_reach_the_host():
    tree = ast.parse(_read("app", "tools.py"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom):
            imported.add((node.module or "").split(".")[0])
    assert not imported & FORBIDDEN_IMPORTS, imported & FORBIDDEN_IMPORTS


def test_search_tool_calls_no_dangerous_builtins():
    tree = ast.parse(_read("app", "tools.py"))
    called = {
        getattr(n.func, "id", getattr(n.func, "attr", ""))
        for n in ast.walk(tree) if isinstance(n, ast.Call)
    }
    assert not called & FORBIDDEN_CALLS, called & FORBIDDEN_CALLS


def test_search_tool_bounds_what_it_echoes():
    out = sandboxed_search("A" * 10_000)
    assert len(out) < 300 and "A" * 151 not in out


def test_search_tool_does_not_execute_its_input():
    payload = "__import__('os').system('echo pwned')"
    out = sandboxed_search(payload)
    assert "pwned" not in out.replace(payload[:150], "")


# --- SEC-03: no credentials in source --------------------------------------

KEY_SHAPES = re.compile(r"sk-[A-Za-z0-9]{16,}|lsv2_[A-Za-z0-9_]{16,}|AKIA[0-9A-Z]{16}")


def test_no_api_key_shaped_literals_in_application_code():
    for root, _, files in os.walk(os.path.join(STARTER, "app")):
        for name in files:
            if name.endswith(".py"):
                with open(os.path.join(root, name), encoding="utf-8") as handle:
                    assert not KEY_SHAPES.search(handle.read()), name


def test_env_example_holds_placeholders_only():
    for line in _read(".env.example").splitlines():
        key, _, value = line.partition("=")
        if key.endswith("_KEY"):
            assert value.startswith("your_") or value == "", f"{key} looks like a real secret"


def test_compose_does_not_bake_in_an_api_key():
    compose = yaml.safe_load(_read("docker-compose.yml"))
    env = compose["services"]["app"]["environment"]
    for entry in env:
        if entry.startswith("OPENAI_API_KEY"):
            assert entry.split("=", 1)[1] == "", "compose hardcodes OPENAI_API_KEY"


# --- SEC-08: CORS closed by default ----------------------------------------

def test_no_cross_origin_access_is_granted():
    res = client.options(
        "/api/v1/run-agent",
        headers={"Origin": "https://evil.example", "Access-Control-Request-Method": "POST"},
    )
    assert "access-control-allow-origin" not in res.headers
    assert "access-control-allow-origin" not in client.get("/health", headers={"Origin": "https://evil.example"}).headers


def test_no_wildcard_cors_middleware_is_mounted():
    for mw in app_main.app.user_middleware:
        if "cors" in mw.cls.__name__.lower():
            assert "*" not in mw.kwargs.get("allow_origins", [])


# --- Error disclosure (exception text must not reach callers) --------------

def test_internal_error_text_is_not_returned(monkeypatch):
    class Boom:
        def invoke(self, *_a, **_k):
            raise RuntimeError("secret-internal-detail /srv/app/keys")

    monkeypatch.setattr(app_main, "graph_app", Boom())
    res = client.post("/api/v1/run-agent", json={"query": "valid query"})
    assert res.status_code == 500
    assert "secret-internal-detail" not in res.text and "/srv/app" not in res.text


# --- SEC-10: container ------------------------------------------------------

def test_dockerfile_final_user_is_not_root():
    users = re.findall(r"^USER\s+(\S+)", _read("Dockerfile"), re.M)
    assert users, "no USER directive"
    assert users[-1].split(":")[0] not in {"root", "0"}


def test_dockerfile_path_keeps_the_system_path():
    """`ENV PATH=/x:` with nothing after the colon wipes PATH and breaks python/uvicorn."""
    paths = re.findall(r"^ENV\s+PATH=(\S+)", _read("Dockerfile"), re.M)
    assert paths and all("$PATH" in p or "${PATH}" in p for p in paths), paths


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
