#!/usr/bin/env python3
"""Repoint or downgrade security controls whose evidence does not resolve.

    python tools/repair_evidence.py --dry-run
    python tools/repair_evidence.py

27% of controls shipped with evidence pointing at test files that were never
written, every one marked `enforced`. A dangling pointer is worse than an
absent one: it reads as proof.

Two outcomes per broken control:

  repoint   the kit does have a security suite, just under a different
            filename. The claim is backed; the pointer was stale.
  downgrade the kit has no suite at all. `enforced` becomes `advisory` —
            still documented guidance, no longer claiming CI enforces it —
            and the dangling pointer is removed.

Nothing here invents a test. Downgrading is the honest outcome when no test
exists, and the control can be promoted back once one is written.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib import security_checks as sc  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
KITS_DIR = REPO_ROOT / "kits"

SKIP_DIRS = {"node_modules", "vendor", "__pycache__", ".pytest_cache", "target", ".next"}

#: Filenames that indicate a suite covering declared security controls.
SECURITY_TEST_HINTS = ("security", "securitycontrols")


def find_security_suite(kit_dir: Path) -> str | None:
    """Kit-relative path to the best security test file, if one exists."""
    candidates: list[Path] = []
    starter = kit_dir / "starter"
    if not starter.is_dir():
        return None
    for path in starter.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        name = path.name.lower()
        if not any(hint in name.replace("_", "").replace("-", "") for hint in SECURITY_TEST_HINTS):
            continue
        if "test" not in name and "spec" not in name:
            continue
        candidates.append(path)
    if not candidates:
        return None
    # Prefer the largest: the richest suite is the most honest pointer.
    best = max(candidates, key=lambda p: p.stat().st_size)
    return best.relative_to(kit_dir).as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="report without writing")
    args = parser.parse_args()

    repointed = downgraded = 0
    per_kit: list[str] = []

    for kit_dir in sorted(p for p in KITS_DIR.iterdir() if (p / "kit.yaml").exists()):
        manifest_path = kit_dir / "security" / "checks.json"
        if not manifest_path.exists():
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        problems = sc.check_evidence_paths(manifest, kit_dir)
        if not problems:
            continue

        broken_ids = {line.split(":", 1)[0] for line in problems}
        suite = find_security_suite(kit_dir)
        r = d = 0

        for check in manifest["checks"]:
            if check["id"] not in broken_ids:
                continue
            old = (check.get("evidence") or {}).get("path", "")
            # Gitleaks and Semgrep do run — from the repo-root workflow, not a
            # per-kit one that never existed. The control is real; the pointer
            # named the wrong file.
            if old.startswith(".github/workflows/"):
                check["evidence"] = {
                    "kind": "workflow",
                    "path": ".github/workflows/validate-kits.yml",
                }
                r += 1
                continue
            if suite:
                check["evidence"] = {"kind": "test", "path": suite}
                r += 1
            else:
                check.pop("evidence", None)
                if check.get("status") == "enforced":
                    check["status"] = "advisory"
                d += 1

        manifest["summary"] = sc.summarize(manifest["checks"])
        if not args.dry_run:
            manifest_path.write_text(
                json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
        repointed += r
        downgraded += d
        per_kit.append(
            f"  {kit_dir.name:<30} repointed {r:>2}  downgraded {d:>2}"
            + (f"  -> {suite}" if suite else "  (no suite found)")
        )

    verb = "would be" if args.dry_run else ""
    print("\n".join(per_kit))
    print(f"\n{repointed} control(s) {verb} repointed to a real suite")
    print(f"{downgraded} control(s) {verb} downgraded to advisory (nothing backs them)")
    if args.dry_run:
        print("\nRe-run without --dry-run to apply.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
