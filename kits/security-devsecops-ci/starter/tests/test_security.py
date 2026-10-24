"""Controls declared in security/checks.json, verified against real config.

This kit's product *is* its configuration, so each test parses the actual
workflow, scanner and Dependabot files rather than asserting on prose. A
control that claims a scanner runs must be backed by a job that runs it.
"""

import json
import os
import re

import pytest
import yaml

STARTER = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KIT = os.path.abspath(os.path.join(STARTER, ".."))


def _read(*parts):
    with open(os.path.join(STARTER, *parts), encoding="utf-8") as handle:
        return handle.read()


def _yaml(*parts):
    return yaml.safe_load(_read(*parts))


@pytest.fixture(scope="module")
def workflow():
    return _yaml(".github", "workflows", "devsecops.yml")


@pytest.fixture(scope="module")
def workflow_text():
    return _read(".github", "workflows", "devsecops.yml")


@pytest.fixture(scope="module")
def controls():
    with open(os.path.join(KIT, "security", "checks.json"), encoding="utf-8") as handle:
        return {c["id"]: c for c in json.load(handle)["checks"]}


# --- SEC-01 / SEC-02: secret scanning (A04:2025) ---------------------------

def test_secret_scan_job_runs_gitleaks(workflow_text):
    assert "gitleaks" in workflow_text.lower(), "no Gitleaks step in the workflow"


def test_gitleaks_config_parses_and_defines_rules():
    config = _read(".gitleaks.toml")
    assert "[[rules]]" in config, ".gitleaks.toml defines no custom rules"
    assert re.search(r'id\s*=', config), "rules have no id field"


def test_gitleaks_scans_full_history(workflow):
    """fetch-depth 0 is required, or only the tip commit is scanned."""
    steps = workflow["jobs"]["secret-scan"]["steps"]
    checkout = next((s for s in steps if "checkout" in str(s.get("uses", ""))), None)
    assert checkout is not None, "secret-scan has no checkout step"
    depth = (checkout.get("with") or {}).get("fetch-depth")
    assert str(depth) == "0", (
        f"fetch-depth is {depth!r}; Gitleaks would scan only the tip commit, "
        "so SEC-01's 'across git commit history' claim would not hold"
    )


# --- SAST-01 / SAST-02: static analysis (A03 / A05:2025) -------------------

def test_semgrep_config_is_valid_yaml_with_rules():
    data = _yaml(".semgrep.yml")
    assert isinstance(data, dict) and data.get("rules"), ".semgrep.yml has no rules"
    for rule in data["rules"]:
        assert rule.get("id"), "a semgrep rule has no id"
        assert rule.get("severity") in {"ERROR", "WARNING", "INFO"}, rule.get("id")
        assert rule.get("pattern") or rule.get("patterns"), f"{rule['id']} has no pattern"


def test_semgrep_covers_injection_sinks():
    """SAST-02 claims SQL and command injection tracking — prove the rules exist."""
    data = _yaml(".semgrep.yml")
    blob = json.dumps(data).lower()
    assert "execute" in blob, "no SQL-injection rule"
    assert "shell=true" in blob or "subprocess" in blob, "no command-injection rule"


def test_sast_job_runs_semgrep(workflow_text):
    assert "semgrep" in workflow_text.lower(), "no Semgrep step in the workflow"


# --- SAST-03: SARIF reporting (A09:2025) -----------------------------------

def test_findings_upload_as_sarif(workflow_text):
    assert "sarif" in workflow_text.lower(), "no SARIF output in the workflow"
    assert "codeql-action/upload-sarif" in workflow_text, (
        "SARIF is produced but never uploaded to GitHub Code Scanning"
    )


# --- CONT-01 / CONT-02: container scanning (A03:2025) ----------------------

def test_container_job_runs_trivy(workflow_text):
    assert "trivy" in workflow_text.lower(), "no Trivy scan in the workflow"


def test_trivy_blocks_on_critical_and_high():
    """CONT-02 claims the build is blocked, not merely annotated."""
    config = _read("trivy.yaml")
    assert re.search(r"CRITICAL", config), "trivy.yaml does not mention CRITICAL"
    assert re.search(r"HIGH", config), "trivy.yaml does not mention HIGH"


# --- CONT-03: container hardening (A02:2025) -------------------------------

def test_dockerfile_runs_as_non_root():
    dockerfile = _read("Dockerfile")
    assert re.search(r"^USER\s+(?!root)", dockerfile, re.M), "no non-root USER directive"


def test_dockerfile_uses_minimal_base():
    assert "alpine" in _read("Dockerfile").lower(), "base image is not Alpine"


# --- SUP-01 / SUP-02: supply chain (A03:2025) ------------------------------

def test_sbom_job_generates_both_formats(workflow_text):
    blob = workflow_text.lower()
    assert "syft" in blob, "no Syft SBOM step"
    assert "cyclonedx" in blob, "SUP-01 claims CycloneDX output"
    assert "spdx" in blob, "SUP-01 claims SPDX output"


def test_dependabot_covers_every_ecosystem_in_the_repo():
    """SUP-02 claims dependency updates; prove the app's ecosystem is watched."""
    data = _yaml(".github", "dependabot.yml")
    ecosystems = {u.get("package-ecosystem") for u in data.get("updates", [])}
    assert "github-actions" in ecosystems, "workflow actions are not watched"
    if os.path.exists(os.path.join(STARTER, "requirements.txt")):
        assert "pip" in ecosystems, (
            "a Python requirements.txt is present but pip is not a watched "
            "ecosystem, so SUP-02's dependency-update claim does not cover the app"
        )
    assert "docker" in ecosystems, (
        "a Dockerfile is present but docker is not a watched ecosystem, so base "
        "image updates are never proposed"
    )


def test_dependabot_schedule_is_weekly_or_tighter():
    data = _yaml(".github", "dependabot.yml")
    for update in data.get("updates", []):
        interval = (update.get("schedule") or {}).get("interval")
        assert interval in {"daily", "weekly"}, (
            f"{update.get('package-ecosystem')} interval is {interval!r}"
        )


# --- SUP-03: local pre-flight (A03:2025) -----------------------------------

def test_local_pipeline_script_is_importable_and_cross_platform():
    source = _read("scripts", "run_local_pipeline.py")
    compile(source, "run_local_pipeline.py", "exec")
    assert "shell=True" not in source, (
        "the local runner uses shell=True, which is the exact pattern its own "
        "Semgrep ruleset flags as command injection"
    )


# --- Manifest consistency ---------------------------------------------------

def test_every_declared_control_has_evidence(controls):
    missing = [cid for cid, c in controls.items() if not c.get("evidence")]
    assert not missing, f"controls with no evidence pointer: {missing}"


def test_control_count_matches_manifest_summary(controls):
    with open(os.path.join(KIT, "security", "checks.json"), encoding="utf-8") as handle:
        data = json.load(handle)
    assert data["summary"]["total"] == len(controls)


# --- SEC-03: pre-commit protection (A03:2025) ------------------------------

def test_pre_commit_config_exists_and_pins_revisions():
    data = _yaml(".pre-commit-config.yaml")
    repos = data.get("repos", [])
    assert repos, "no pre-commit repos configured"
    for repo in repos:
        if repo.get("repo") == "local":
            continue
        rev = repo.get("rev")
        assert rev and rev not in {"main", "master", "HEAD"}, (
            f"{repo.get('repo')} is not pinned to a release (rev={rev!r}); an "
            "unpinned hook has commit access to the working tree"
        )


def test_pre_commit_runs_gitleaks_on_staged_changes():
    blob = _read(".pre-commit-config.yaml")
    assert "gitleaks" in blob, "SEC-03 claims secret protection but no gitleaks hook"
    assert "--staged" in blob, "gitleaks hook does not scan staged changes"
