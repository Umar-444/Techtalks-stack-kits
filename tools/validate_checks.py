#!/usr/bin/env python3
"""Validate — and optionally migrate — every kit security manifest.

    python tools/validate_checks.py            # validate, non-zero exit on failure
    python tools/validate_checks.py --fix      # rewrite manifests in canonical v2
    python tools/validate_checks.py --kit go-fiber-api --verbose

Run with --fix once to migrate legacy manifests, then keep the bare form in CI
so manifests cannot drift back out of schema.
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


def kit_slugs(only: str | None) -> list[str]:
    if only:
        return [only]
    return sorted(
        p.name for p in KITS_DIR.iterdir()
        if p.is_dir() and (p / "kit.yaml").exists()
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fix", action="store_true", help="rewrite manifests in canonical v2 form")
    parser.add_argument(
        "--reclassify",
        action="store_true",
        help="discard stored owasp/severity and re-derive them from the classifier "
             "(use after editing tools/lib/owasp.py; implies --fix)",
    )
    parser.add_argument("--kit", help="limit to a single kit slug")
    parser.add_argument("--verbose", action="store_true", help="show classification warnings")
    args = parser.parse_args()
    if args.reclassify:
        args.fix = True

    failures: dict[str, list[str]] = {}
    warnings: list[str] = []
    migrated: list[str] = []
    unchanged = 0

    for slug in kit_slugs(args.kit):
        path = KITS_DIR / slug / "security" / "checks.json"
        if not path.exists():
            failures[slug] = ["missing security/checks.json"]
            continue

        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            shape = sc.detect_shape(raw)
            manifest, warns = sc.normalize(raw, slug, reclassify=args.reclassify)
        except (json.JSONDecodeError, sc.ManifestError) as exc:
            failures[slug] = [f"unreadable manifest: {exc}"]
            continue

        warnings.extend(warns)

        if args.fix:
            before = path.read_text(encoding="utf-8")
            after = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
            if before != after:
                sc.dump(manifest, path)
                migrated.append(f"{slug} ({shape} -> v2, {manifest['summary']['total']} controls)")
            else:
                unchanged += 1

        errors = sc.validate(manifest)
        errors += sc.check_evidence_paths(manifest, KITS_DIR / slug)
        if shape != "v2" and not args.fix:
            errors.insert(0, f"legacy {shape} manifest; run validate_checks.py --fix")
        if errors:
            failures[slug] = errors

    if args.fix:
        print(f"migrated {len(migrated)} manifest(s), {unchanged} already canonical")
        for line in migrated:
            print(f"  + {line}")

    if warnings and args.verbose:
        print(f"\n{len(warnings)} classification warning(s):")
        for line in warnings:
            print(f"  ! {line}")
    elif warnings:
        print(f"\n{len(warnings)} classification warning(s) (use --verbose to list)")

    if failures:
        print(f"\nFAIL — {len(failures)} kit(s) with schema errors:")
        for slug, errors in failures.items():
            print(f"\n  {slug}")
            for error in errors:
                print(f"    - {error}")
        return 1

    print(f"\nPASS — all {len(kit_slugs(args.kit))} manifest(s) valid against schema v{sc.SCHEMA_VERSION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
