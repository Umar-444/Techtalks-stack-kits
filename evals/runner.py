#!/usr/bin/env python3
"""TechTalks Stack Kits — kit verification and context-cost benchmark.

    python evals/runner.py                  # all kits
    python evals/runner.py --kit go-fiber-api
    python evals/runner.py --json           # machine-readable only

WHAT THIS MEASURES (exact, reproducible, no network):

  context_tokens   The real tokenizer count of everything an agent must read
                   before it can work in a kit: its rules dialect plus
                   DESIGN.md, SECURITY.md and the build steps. Counted with
                   tiktoken cl100k_base when installed, otherwise estimated
                   from a calibrated character ratio and flagged as such.

  structural gates Manifest validity, transpiler zero-drift, dialect
                   completeness, and a secret-pattern sweep.

  starter_loc      How much runnable source a kit actually ships.

WHAT THIS DELIBERATELY DOES NOT CLAIM:

  Tokens to complete a reference build, and first-try agent correctness,
  cannot be determined without running a live agent against the kit. This
  runner does not invoke one, so it does not report those numbers. Earlier
  revisions printed hardcoded constants for them; that was removed because a
  constant presented as a measurement is worse than no measurement.

Efficiency tiers are derived from the measured context cost using the
thresholds in TIER_THRESHOLDS, which were set from the observed distribution
across the catalogue. Re-deriving them is a one-line change, so the grade
always traces back to a number you can reproduce.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import shutil
import statistics
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(REPO_ROOT, "evals", "results")

# Derived from the measured catalogue distribution (p25 / p75 / tail).
TIER_THRESHOLDS = ((1_900, "A+"), (2_900, "A"), (4_000, "B"))
TIER_FALLBACK = "C"

#: Files an agent loads before writing code, by dialect.
DIALECT_ENTRYPOINTS = {
    "claude": "CLAUDE.md",
    "codex": "CODEX.md",
    "standard": "AGENTS.md",
    "cline": ".clinerules",
    "windsurf": ".windsurfrules",
    "copilot": os.path.join(".github", "copilot-instructions.md"),
}

#: Supporting context every dialect pulls in alongside its rules file.
SHARED_CONTEXT = ("DESIGN.md", "SECURITY.md", os.path.join("steps", "agent-build-steps.md"))

SOURCE_EXTENSIONS = (
    ".php", ".py", ".go", ".rs", ".ts", ".tsx", ".js", ".jsx",
    ".rb", ".ex", ".exs", ".templ", ".sql",
)

SECRET_PATTERNS = (
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"ghp_[0-9a-zA-Z]{36}"),
    re.compile(r"\bsk-[a-zA-Z0-9_-]{20,}"),
    re.compile(r"BEGIN RSA PRIVATE KEY"),
)

SCANNED_EXTENSIONS = (
    ".php", ".md", ".yaml", ".yml", ".json", ".ts", ".tsx",
    ".sql", ".py", ".go", ".rs", ".rb", ".ex", ".example",
)


# --------------------------------------------------------------------------
# Token counting
# --------------------------------------------------------------------------

class TokenCounter:
    """Exact counts via tiktoken when available, calibrated estimate otherwise."""

    #: chars-per-token measured across this catalogue's markdown with cl100k_base
    FALLBACK_RATIO = 4.4

    def __init__(self) -> None:
        self.encoder = None
        self.exact = False
        try:
            import tiktoken
            self.encoder = tiktoken.get_encoding("cl100k_base")
            self.exact = True
        except Exception:
            pass

    @property
    def method(self) -> str:
        return "tiktoken:cl100k_base" if self.exact else f"estimated:chars/{self.FALLBACK_RATIO}"

    def count(self, text: str) -> int:
        if not text:
            return 0
        if self.encoder is not None:
            return len(self.encoder.encode(text))
        return max(1, round(len(text) / self.FALLBACK_RATIO))

    def count_file(self, path: str) -> int:
        try:
            with open(path, "r", encoding="utf-8") as handle:
                return self.count(handle.read())
        except (OSError, UnicodeDecodeError):
            return 0


def tier_for(context_tokens: int) -> str:
    for ceiling, label in TIER_THRESHOLDS:
        if context_tokens <= ceiling:
            return label
    return TIER_FALLBACK


# --------------------------------------------------------------------------
# Per-kit measurement
# --------------------------------------------------------------------------

def measure_context(kit_dir: str, counter: TokenCounter) -> dict:
    shared = {
        os.path.basename(rel): counter.count_file(os.path.join(kit_dir, rel))
        for rel in SHARED_CONTEXT
    }
    shared_total = sum(shared.values())

    dialects = {}
    for name, rel in DIALECT_ENTRYPOINTS.items():
        rules_tokens = counter.count_file(os.path.join(kit_dir, rel))
        if rules_tokens:
            dialects[name] = {
                "rules_tokens": rules_tokens,
                "total_tokens": rules_tokens + shared_total,
            }

    primary = dialects.get("claude") or (next(iter(dialects.values()), None))
    return {
        "method": counter.method,
        "exact": counter.exact,
        "shared_context": shared,
        "shared_context_tokens": shared_total,
        "dialects": dialects,
        "context_tokens": primary["total_tokens"] if primary else 0,
        "leanest_dialect": min(
            dialects.items(), key=lambda kv: kv[1]["total_tokens"]
        )[0] if dialects else None,
    }


#: Installed dependencies and build output are not the kit's own source.
#: Without this, a kit that has had `composer install` run reports hundreds of
#: thousands of vendored lines and the metric becomes meaningless.
NON_SOURCE_DIRS = {
    "vendor", "node_modules", "__pycache__", ".pytest_cache", ".phpunit.cache",
    "target", "dist", "build", ".next", ".venv", "venv", "migrations_cache",
    "storage", "bootstrap_cache", ".ruff_cache", ".mypy_cache", "instance",
}


def measure_starter(kit_dir: str) -> dict:
    """Count only first-party starter source, excluding installed dependencies."""
    starter = os.path.join(kit_dir, "starter")
    files = 0
    loc = 0
    if os.path.isdir(starter):
        for root, dirs, names in os.walk(starter):
            dirs[:] = [d for d in dirs if d not in NON_SOURCE_DIRS and not d.startswith(".")]
            for name in names:
                files += 1
                if name.endswith(SOURCE_EXTENSIONS):
                    path = os.path.join(root, name)
                    try:
                        with open(path, "r", encoding="utf-8", errors="ignore") as handle:
                            loc += sum(1 for line in handle if line.strip())
                    except OSError:
                        pass
    return {"files": files, "source_loc": loc}


#: Inline markers that mark a credential-shaped literal as a deliberate
#: fixture. A security test needs a realistic fake key to prove detection
#: works; blanket-skipping test files instead would hide a genuine leak.
SECRET_ALLOW_MARKERS = ("pragma: allowlist secret", "gitleaks:allow", "noqa: secret")


def scan_secrets(kit_dir: str) -> list[str]:
    """Scan the kit's own files. Installed dependencies are not its responsibility."""
    hits = []
    for root, dirs, names in os.walk(kit_dir):
        dirs[:] = [d for d in dirs if d not in NON_SOURCE_DIRS]
        for name in names:
            if not name.endswith(SCANNED_EXTENSIONS):
                continue
            path = os.path.join(root, name)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as handle:
                    lines = handle.readlines()
            except OSError:
                continue
            for number, line in enumerate(lines, start=1):
                if any(marker in line for marker in SECRET_ALLOW_MARKERS):
                    continue
                if any(pattern.search(line) for pattern in SECRET_PATTERNS):
                    rel = os.path.relpath(path, REPO_ROOT).replace("\\", "/")
                    hits.append(f"{rel}:{number}")
                    break
    return hits


def load_tasks(kit_slug: str) -> list[dict]:
    path = os.path.join(REPO_ROOT, "evals", "tasks", f"{kit_slug}_tasks.json")
    if not os.path.isfile(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle).get("eval_tasks", [])
    except (OSError, json.JSONDecodeError):
        return []


def evaluate_tasks(kit_slug: str, kit_dir: str) -> dict:
    """Run each task's verify command if it has one; never assume a pass.

    Three distinct non-pass outcomes, kept separate because conflating them is
    how the old runner ended up reporting a clean sweep:

      not_executed  the task defines no verify command — a gap in the task
      skipped       the task declares a toolchain this machine lacks
      fail          the command ran and returned non-zero
    """
    results = []
    for task in load_tasks(kit_slug):
        entry = {
            "id": task.get("id"),
            "title": task.get("title"),
            "assertions": len(task.get("assertions", [])),
        }
        command = task.get("verify")
        missing = [
            binary for binary in task.get("requires", [])
            if shutil.which(binary) is None
        ]
        # Probe the interpreter the verify command will actually use (the
        # `python` on PATH), not the one running this script — they differ
        # whenever the kit's dependencies live in a virtualenv.
        modules = task.get("requires_python", [])
        if modules:
            # Resolve the interpreter explicitly: on Windows, subprocess looks
            # the executable up on the parent's PATH, ignoring any PATH passed
            # in env, so a bare "python" would miss an activated virtualenv.
            interpreter = shutil.which("python") or shutil.which("python3")
            if not interpreter:
                missing.append("python")
            else:
                # find_spec, not import: django-ninja and similar run their
                # module body on import and need DJANGO_SETTINGS_MODULE, so a
                # bare import reports an installed package as missing.
                probe = subprocess.run(
                    [interpreter, "-c",
                     "import importlib.util as u,sys;"
                     f"sys.exit(0 if all(u.find_spec(m) for m in {modules!r}) else 1)"],
                    capture_output=True, text=True,
                )
                if probe.returncode != 0:
                    missing.append(f"python modules: {', '.join(modules)}")

        if not command:
            entry["status"] = "not_executed"
            entry["reason"] = "task defines no verify command"
        elif missing:
            entry["status"] = "skipped"
            entry["reason"] = f"toolchain not installed: {', '.join(missing)}"
        else:
            try:
                completed = subprocess.run(
                    command, shell=True, cwd=kit_dir, capture_output=True,
                    text=True, timeout=180,
                )
                entry["status"] = "pass" if completed.returncode == 0 else "fail"
                entry["exit_code"] = completed.returncode
                if completed.returncode != 0:
                    entry["stderr"] = (completed.stderr or completed.stdout).strip()[:400]
            except subprocess.TimeoutExpired:
                entry["status"] = "fail"
                entry["reason"] = "verify command timed out after 180s"
        results.append(entry)

    return {
        "tasks": results,
        "total": len(results),
        "passed": sum(1 for r in results if r["status"] == "pass"),
        "failed": sum(1 for r in results if r["status"] == "fail"),
        "skipped": sum(1 for r in results if r["status"] == "skipped"),
        "not_executed": sum(1 for r in results if r["status"] == "not_executed"),
    }


def run_eval_for_kit(kit_slug: str, counter: TokenCounter, verbose: bool = True) -> tuple[bool, dict | None]:
    kit_dir = os.path.join(REPO_ROOT, "kits", kit_slug)
    if not os.path.isdir(kit_dir):
        if verbose:
            print(f"[FAIL] Kit directory not found: kits/{kit_slug}")
        return False, None

    manifest_path = os.path.join(kit_dir, "kit.yaml")
    manifest_ok = os.path.isfile(manifest_path) and subprocess.run(
        [sys.executable, os.path.join("tools", "validate_manifest.py"), manifest_path],
        capture_output=True, text=True, cwd=REPO_ROOT,
    ).returncode == 0

    drift_ok = True
    if os.path.isdir(os.path.join(kit_dir, "rules", "source")):
        drift_ok = subprocess.run(
            [sys.executable, os.path.join("tools", "transpiler.py"),
             "--kit", os.path.join("kits", kit_slug), "--check"],
            capture_output=True, text=True, cwd=REPO_ROOT,
        ).returncode == 0

    context = measure_context(kit_dir, counter)
    dialects_ok = len(context["dialects"]) == len(DIALECT_ENTRYPOINTS) and all(
        os.path.isdir(os.path.join(kit_dir, d)) and
        any(f.endswith(ext) for f in os.listdir(os.path.join(kit_dir, d)))
        for d, ext in ((os.path.join(".cursor", "rules"), ".mdc"),
                       (os.path.join(".agents", "rules"), ".md"))
    )

    leaks = scan_secrets(kit_dir)
    starter = measure_starter(kit_dir)
    tasks = evaluate_tasks(kit_slug, kit_dir)

    gates_ok = manifest_ok and drift_ok and dialects_ok and not leaks and tasks["failed"] == 0

    metrics = {
        "kit_slug": kit_slug,
        "status": "PASS" if gates_ok else "FAIL",
        "gates": {
            "manifest_valid": manifest_ok,
            "transpiler_zero_drift": drift_ok,
            "dialects_complete": dialects_ok,
            "secret_leak_free": not leaks,
            "secret_hits": leaks,
        },
        "context_cost": {
            "measurement": context["method"],
            "exact": context["exact"],
            "context_tokens": context["context_tokens"],
            "shared_context_tokens": context["shared_context_tokens"],
            "shared_context": context["shared_context"],
            "per_dialect": context["dialects"],
            "leanest_dialect": context["leanest_dialect"],
            "efficiency_tier": tier_for(context["context_tokens"]),
        },
        "starter": starter,
        "task_verification": tasks,
        "not_measured": [
            "tokens_to_complete_build — requires a live agent run",
            "first_try_correctness — requires a live agent run",
        ],
    }

    if verbose:
        print(f"\n=== {kit_slug} ===")
        print(f"  manifest {_mark(manifest_ok)}   drift {_mark(drift_ok)}   "
              f"dialects {_mark(dialects_ok)}   secrets {_mark(not leaks)}")
        print(f"  context  {context['context_tokens']:,} tokens "
              f"(tier {metrics['context_cost']['efficiency_tier']}, {context['method']})")
        print(f"  starter  {starter['files']} files, {starter['source_loc']:,} LOC")
        if tasks["total"]:
            print(f"  tasks    {tasks['passed']} passed, {tasks['failed']} failed, "
                  f"{tasks['skipped']} skipped, {tasks['not_executed']} not executed")

    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(os.path.join(RESULTS_DIR, f"{kit_slug}_metrics.json"), "w", encoding="utf-8") as handle:
        json.dump(metrics, handle, indent=2)

    return gates_ok, metrics


def _mark(ok: bool) -> str:
    return "ok" if ok else "FAIL"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kit", help="evaluate a single kit slug")
    parser.add_argument("--json", action="store_true", help="suppress the human report")
    args = parser.parse_args()

    kits_dir = os.path.join(REPO_ROOT, "kits")
    slugs = [args.kit] if args.kit else sorted(
        name for name in os.listdir(kits_dir)
        if os.path.isfile(os.path.join(kits_dir, name, "kit.yaml"))
    )

    counter = TokenCounter()
    if not counter.exact and not args.json:
        print("note: tiktoken not installed — context costs are estimated, not exact.\n"
              "      pip install -r requirements.txt for exact counts.\n")

    all_metrics = []
    failures = []
    for slug in slugs:
        ok, metrics = run_eval_for_kit(slug, counter, verbose=not args.json)
        if metrics:
            all_metrics.append(metrics)
        if not ok:
            failures.append(slug)

    costs = [m["context_cost"]["context_tokens"] for m in all_metrics if m["context_cost"]["context_tokens"]]
    not_executed = sum(m["task_verification"]["not_executed"] for m in all_metrics)
    skipped = sum(m["task_verification"]["skipped"] for m in all_metrics)
    passed_tasks = sum(m["task_verification"]["passed"] for m in all_metrics)
    tasks_total = sum(m["task_verification"]["total"] for m in all_metrics)

    summary = {
        "kits_evaluated": len(all_metrics),
        "kits_passing_gates": len(all_metrics) - len(failures),
        "kits_failing_gates": failures,
        "measurement": counter.method,
        "context_tokens": {
            "min": min(costs) if costs else 0,
            "median": int(statistics.median(costs)) if costs else 0,
            "max": max(costs) if costs else 0,
        },
        "task_verification": {
            "total": tasks_total,
            "passed": passed_tasks,
            "skipped_no_toolchain": skipped,
            "not_executed": not_executed,
        },
        "not_measured": [
            "tokens_to_complete_build — requires a live agent run",
            "first_try_correctness — requires a live agent run",
        ],
    }

    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(os.path.join(RESULTS_DIR, "summary.json"), "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    if not args.json:
        print("\n" + "=" * 62)
        print(f" {summary['kits_passing_gates']}/{summary['kits_evaluated']} kits pass structural gates")
        print(f" context cost: min {summary['context_tokens']['min']:,} / "
              f"median {summary['context_tokens']['median']:,} / "
              f"max {summary['context_tokens']['max']:,} tokens  ({counter.method})")
        if tasks_total:
            print(f" task verification: {passed_tasks} passed, {skipped} skipped (toolchain), "
                  f"{not_executed} lack a verify command")
        print(" not measured: build-completion tokens, first-try correctness")
        print("=" * 62)
        if failures:
            print(f"\nFAILING: {', '.join(failures)}")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
