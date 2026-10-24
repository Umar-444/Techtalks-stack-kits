"""Load, normalize and validate kit security manifests.

Three on-disk shapes have existed across the kit catalogue:

  v1-flat    {"checks": [{"id", "name", "status": "PASS", "description"}]}
  v1-nested  {"categories": [{"name", "controls": [{"id", "name", "status", <evidence-key>}]}]}
  v2         the canonical shape defined by schemas/kit-security-checks.schema.json

``normalize`` accepts any of them and returns v2, so every consumer reads one
shape regardless of what a kit currently has on disk.
"""

from __future__ import annotations

import datetime as _dt
import json
import re
from pathlib import Path
from typing import Any

from . import owasp

SCHEMA_VERSION = "2.0.0"
MIN_CHECKS = 12

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "schemas" / "kit-security-checks.schema.json"

_STATUS_MAP = {
    "pass": "enforced",
    "passed": "enforced",
    "enforced": "enforced",
    "active": "enforced",
    "verified": "enforced",
    "advisory": "advisory",
    "warn": "advisory",
    "documented": "advisory",
    "n/a": "not-applicable",
    "na": "not-applicable",
    "not-applicable": "not-applicable",
    "skipped": "not-applicable",
}

#: Keys that carried the evidence pointer in the v1-nested shape.
_EVIDENCE_KEYS = {
    "test": "test",
    "tests": "test",
    "workflow": "workflow",
    "rule": "rule",
    "rules": "rule",
    "docker": "docker",
    "dockerfile": "docker",
    "migration": "migration",
    "config": "config",
    "source": "source",
    "file": "source",
    "tool": "tool",
    "endpoint": "endpoint",
    "docs": "docs",
    "doc": "docs",
}

#: Friendly category names for common control-id prefixes, used when a manifest
#: has no explicit grouping of its own.
_PREFIX_CATEGORIES = {
    "AUTH": "Authentication & Session Security",
    "AUTHZ": "Authorization & Multi-Tenancy",
    "SEC": "Core Security Guardrails",
    "DATA": "Input Validation & Data Layer",
    "DB": "Database Hardening",
    "SQL": "Database Hardening",
    "NET": "Network & Transport",
    "API": "API Surface Hardening",
    "CRYPTO": "Cryptography & Secrets",
    "KEY": "Cryptography & Secrets",
    "OPS": "Runtime & Container Hardening",
    "CONT": "Runtime & Container Hardening",
    "CI": "CI & Supply Chain Guardrails",
    "SUPPLY": "CI & Supply Chain Guardrails",
    "DEP": "CI & Supply Chain Guardrails",
    "LOG": "Logging, Audit & Observability",
    "OBS": "Logging, Audit & Observability",
    "AI": "AI & LLM Safety",
    "LLM": "AI & LLM Safety",
    "RAG": "AI & LLM Safety",
    "PII": "Privacy & Data Protection",
    "ERR": "Error Handling & Resilience",
}

_ID_RE = re.compile(r"^[A-Z][A-Z0-9]{1,11}-[0-9]{2}$")


class ManifestError(ValueError):
    """Raised when a manifest cannot be parsed or normalized."""


def detect_shape(data: dict[str, Any]) -> str:
    if data.get("schema_version") == SCHEMA_VERSION:
        return "v2"
    if isinstance(data.get("categories"), list):
        return "v1-nested"
    if isinstance(data.get("checks"), list):
        return "v1-flat"
    raise ManifestError("unrecognized manifest shape: no 'checks' or 'categories'")


def _status(raw: Any) -> str:
    return _STATUS_MAP.get(str(raw or "enforced").strip().lower(), "enforced")


def _evidence(control: dict[str, Any]) -> dict[str, str] | None:
    existing = control.get("evidence")
    if isinstance(existing, dict) and existing.get("kind") and existing.get("path"):
        return {"kind": str(existing["kind"]), "path": str(existing["path"])}
    for key, kind in _EVIDENCE_KEYS.items():
        value = control.get(key)
        if isinstance(value, str) and value.strip():
            # v1-nested sometimes wrote "starter/src/main.rs: PgPoolOptions";
            # keep the path, drop the trailing symbol hint.
            path = value.split(":", 1)[0].strip() if kind != "endpoint" else value.strip()
            return {"kind": kind, "path": path[:200]}
    return None


def _category_for(control: dict[str, Any], fallback_owasp: list[str]) -> str:
    explicit = control.get("category")
    if isinstance(explicit, str) and len(explicit.strip()) >= 3:
        return explicit.strip()[:80]
    prefix = str(control.get("id", "")).split("-", 1)[0].upper()
    if prefix in _PREFIX_CATEGORIES:
        return _PREFIX_CATEGORIES[prefix]
    if fallback_owasp:
        return owasp.BY_ID[fallback_owasp[0]].name
    return "Core Security Guardrails"


def _iter_raw_controls(data: dict[str, Any], shape: str):
    """Yield (control_dict, inherited_category_or_None) pairs."""
    if shape == "v1-nested":
        for category in data.get("categories", []):
            name = str(category.get("name", "")).strip() or None
            for control in category.get("controls", []):
                yield control, name
    else:
        for control in data.get("checks", []):
            yield control, None


def normalize(
    data: dict[str, Any], kit_slug: str, *, reclassify: bool = False
) -> tuple[dict[str, Any], list[str]]:
    """Convert any supported manifest shape to canonical v2.

    Existing ``owasp``/``severity`` values are preserved so hand-tuned
    manifests survive a re-run; pass ``reclassify=True`` to discard them and
    re-derive everything from the classifier.

    Returns ``(manifest, warnings)``. Warnings name controls whose OWASP
    category had to be guessed, so they can be reviewed rather than trusted.
    """
    shape = detect_shape(data)
    warnings: list[str] = []
    checks: list[dict[str, Any]] = []
    used_ids: set[str] = set()
    prefix_counters: dict[str, int] = {}

    for raw, inherited_category in _iter_raw_controls(data, shape):
        name = str(raw.get("name", "")).strip()
        if not name:
            continue
        description = str(raw.get("description", "")).strip()

        existing_owasp = [] if reclassify else [
            normalized
            for normalized in (owasp.normalize_id(x) for x in _as_list(raw.get("owasp")))
            if normalized
        ]
        if existing_owasp:
            classification = owasp.Classification(
                existing_owasp,
                str(raw.get("severity", "")).lower() or "high",
                _as_list(raw.get("cwe")),
                True,
            )
        else:
            classification = owasp.classify(name, description, str(raw.get("id", "")))
            if not classification.confident:
                warnings.append(f"{kit_slug}: unclassified control {raw.get('id')!r} — {name[:60]!r}")

        resolved_owasp = classification.owasp or ["A06:2025"]
        severity = classification.severity if classification.severity in {
            "critical", "high", "medium", "low"
        } else "medium"

        category = (
            str(inherited_category).strip()[:80]
            if inherited_category
            else _category_for(raw, resolved_owasp)
        )

        check: dict[str, Any] = {
            "id": _stable_id(raw.get("id"), category, used_ids, prefix_counters),
            "category": category,
            "name": name[:160],
            "status": _status(raw.get("status")),
            "severity": severity,
            "owasp": resolved_owasp,
        }
        if description:
            check["description"] = description[:400]
        if classification.cwe:
            check["cwe"] = classification.cwe
        evidence = _evidence(raw)
        if evidence:
            check["evidence"] = evidence
        checks.append(check)

    if len(checks) < MIN_CHECKS:
        warnings.append(f"{kit_slug}: only {len(checks)} controls (minimum {MIN_CHECKS})")

    manifest = {
        "$schema": "../../../schemas/kit-security-checks.schema.json",
        "schema_version": SCHEMA_VERSION,
        "kit_slug": kit_slug,
        "updated_at": str(data.get("updated_at") or _dt.date.today().isoformat())[:10],
        "owasp_edition": owasp.EDITION,
        "summary": summarize(checks),
        "checks": checks,
    }
    return manifest, warnings


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(v) for v in value]
    return []


def _stable_id(
    raw_id: Any,
    category: str,
    used: set[str],
    counters: dict[str, int],
) -> str:
    """Keep conforming ids; renumber the rest while preserving their prefix."""
    candidate = str(raw_id or "").strip().upper()
    if _ID_RE.match(candidate) and candidate not in used:
        used.add(candidate)
        prefix = candidate.split("-")[0]
        counters[prefix] = max(counters.get(prefix, 0), int(candidate.split("-")[1]))
        return candidate

    prefix = candidate.split("-", 1)[0] if "-" in candidate else candidate
    prefix = re.sub(r"[^A-Z0-9]", "", prefix)[:12]
    if not prefix or not prefix[0].isalpha():
        words = re.findall(r"[A-Za-z]+", category)
        prefix = (words[0][:4].upper() if words else "SEC")

    while True:
        counters[prefix] = counters.get(prefix, 0) + 1
        new_id = f"{prefix}-{counters[prefix]:02d}"
        if new_id not in used:
            used.add(new_id)
            return new_id


def summarize(checks: list[dict[str, Any]]) -> dict[str, Any]:
    by_status: dict[str, int] = {}
    by_severity: dict[str, int] = {}
    covered: set[str] = set()
    categories: set[str] = set()
    for check in checks:
        by_status[check["status"]] = by_status.get(check["status"], 0) + 1
        by_severity[check["severity"]] = by_severity.get(check["severity"], 0) + 1
        covered.update(check.get("owasp", []))
        categories.add(check["category"])
    return {
        "total": len(checks),
        "categories": len(categories),
        "by_status": dict(sorted(by_status.items())),
        "by_severity": {
            s: by_severity[s]
            for s in ("critical", "high", "medium", "low")
            if s in by_severity
        },
        "owasp_covered": sorted(covered),
    }


def load(path: str | Path) -> dict[str, Any]:
    """Read a manifest from disk and return it in canonical v2 form."""
    path = Path(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    slug = str(data.get("kit_slug") or data.get("kit") or path.parent.parent.name)
    manifest, _ = normalize(data, slug)
    return manifest


def dump(manifest: dict[str, Any], path: str | Path) -> None:
    Path(path).write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


#: Evidence kinds that name a file on disk. `tool` and `endpoint` identify a
#: binary or an HTTP route instead, so they have nothing to resolve.
_FILE_EVIDENCE_KINDS = frozenset(
    {"test", "workflow", "rule", "docker", "migration", "config", "source", "docs"}
)


def check_evidence_paths(manifest: dict[str, Any], kit_dir: Path) -> list[str]:
    """Report controls whose evidence pointer does not resolve to a real file.

    A manifest that says a control is enforced, and points at a test that was
    never written, is worse than one that admits the gap: it reads as proof.
    """
    problems: list[str] = []
    for check in manifest.get("checks", []):
        evidence = check.get("evidence")
        if not evidence:
            if check.get("status") == "enforced":
                problems.append(
                    f"{check['id']}: status is 'enforced' with no evidence pointer"
                )
            continue
        if evidence["kind"] not in _FILE_EVIDENCE_KINDS:
            continue
        # Strip a pytest-style ::node selector before resolving.
        rel = evidence["path"].split("::", 1)[0]
        bases = [kit_dir, kit_dir / "starter"]
        # CI lives at the repository root, not inside each kit, so a workflow
        # pointer resolves there.
        if rel.startswith(".github/") or evidence["kind"] == "workflow":
            bases.append(REPO_ROOT)
        if not any((base / rel).exists() for base in bases):
            problems.append(
                f"{check['id']}: evidence path does not exist — {rel}"
            )
    return problems


def validate(manifest: dict[str, Any]) -> list[str]:
    """Validate against the JSON Schema plus repo-specific invariants."""
    errors: list[str] = []
    try:
        import jsonschema
    except ImportError:
        errors.append("jsonschema not installed; run pip install -r requirements.txt")
        return errors

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(manifest), key=lambda e: list(e.path)):
        location = "/".join(str(p) for p in error.path) or "<root>"
        errors.append(f"{location}: {error.message}")

    seen: set[str] = set()
    for check in manifest.get("checks", []):
        cid = check.get("id")
        if cid in seen:
            errors.append(f"duplicate control id: {cid}")
        seen.add(cid)

    expected = summarize(manifest.get("checks", []))
    if manifest.get("summary") != expected:
        errors.append("summary block is stale; regenerate with validate_checks.py --fix")

    return errors
