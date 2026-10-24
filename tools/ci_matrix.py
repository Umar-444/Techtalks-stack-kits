#!/usr/bin/env python3
"""Group kits by the toolchain their eval tasks declare.

    python tools/ci_matrix.py                      # summary table
    python tools/ci_matrix.py --toolchain go       # slugs for one CI job
    python tools/ci_matrix.py --json               # full mapping

CI reads this instead of hardcoding kit lists per job, so adding a kit or
changing what it requires never leaves a stale list behind in the workflow.

Grouping comes from each task's `requires` / `requires_python`, which are the
same fields evals/runner.py uses to decide whether to execute or skip. One
source, so a job can never run a kit whose toolchain it did not install.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TASKS_DIR = REPO_ROOT / "evals" / "tasks"
KITS_DIR = REPO_ROOT / "kits"

#: Binary a task declares -> the CI job that installs it. Order matters: the
#: first match wins, so a kit needing both php and python lands in the php job
#: where composer is available.
TOOLCHAIN_FOR_BINARY = {
    "composer": "php",
    "php": "php",
    "go": "go",
    "cargo": "rust",
    "cargo-audit": "rust",
    "mix": "elixir",
    "bundle": "ruby",
    "ruby": "ruby",
    "bun": "bun",
    "npm": "node",
    "node": "node",
    "python": "python",
}

JOB_ORDER = ["php", "go", "rust", "elixir", "ruby", "bun", "node", "python"]


def classify(task: dict) -> str | None:
    for binary in task.get("requires", []):
        job = TOOLCHAIN_FOR_BINARY.get(binary)
        if job and job != "python":
            return job
    for binary in task.get("requires", []):
        if TOOLCHAIN_FOR_BINARY.get(binary) == "python":
            return "python"
    if task.get("requires_python"):
        return "python"
    return None


def build() -> dict[str, list[str]]:
    groups: dict[str, set[str]] = {job: set() for job in JOB_ORDER}
    unassigned: set[str] = set()

    for kit_dir in sorted(p for p in KITS_DIR.iterdir() if (p / "kit.yaml").exists()):
        slug = kit_dir.name
        path = TASKS_DIR / f"{slug}_tasks.json"
        if not path.exists():
            unassigned.add(slug)
            continue
        tasks = json.loads(path.read_text(encoding="utf-8")).get("eval_tasks", [])
        jobs = {classify(t) for t in tasks if t.get("verify")}
        jobs.discard(None)
        if not jobs:
            unassigned.add(slug)
            continue
        # A kit whose tasks span toolchains runs in each relevant job; the
        # runner skips the tasks that job cannot satisfy.
        for job in jobs:
            groups[job].add(slug)

    result = {job: sorted(slugs) for job, slugs in groups.items() if slugs}
    if unassigned:
        result["_no_verify_commands"] = sorted(unassigned)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--toolchain", help="print one slug per line for this CI job")
    parser.add_argument("--json", action="store_true", help="print the full mapping")
    args = parser.parse_args()

    groups = build()

    if args.toolchain:
        for slug in groups.get(args.toolchain, []):
            print(slug)
        return 0

    if args.json:
        print(json.dumps(groups, indent=2))
        return 0

    total = sum(len(v) for k, v in groups.items() if not k.startswith("_"))
    print(f"{total} kit-job assignments across {len([k for k in groups if not k.startswith('_')])} toolchains\n")
    for job in JOB_ORDER:
        slugs = groups.get(job)
        if slugs:
            print(f"  {job:<8} ({len(slugs):>2})  {' '.join(slugs)}")
    stragglers = groups.get("_no_verify_commands")
    if stragglers:
        print(f"\n  {len(stragglers)} kit(s) with no verify command yet — not run by any job:")
        for slug in stragglers:
            print(f"    - {slug}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
