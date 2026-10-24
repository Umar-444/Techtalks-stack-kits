#!/usr/bin/env python3
"""Reject UTF-8 BOMs in files that are parsed or served byte-for-byte.

    python tools/check_encoding.py          # report, non-zero exit on failure
    python tools/check_encoding.py --fix    # strip the BOMs

A BOM is invisible in an editor and harmless in prose, but it breaks anything
that reads the first bytes literally:

  .env.example   dotenv parses the first key as "\\ufeffDATABASE_URL"
  templates      the BOM renders into the HTML body, before <!doctype>
  .sql           some drivers reject a statement that does not start with SQL
  .json / .yml   strict parsers fail outright

This runs in CI so the problem cannot reappear through an editor default.
"""

from __future__ import annotations

import argparse
import os
import sys

BOM = b"\xef\xbb\xbf"

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build"}

#: Extensions where a BOM changes behaviour rather than just looking untidy.
CHECKED_EXTENSIONS = {
    ".env", ".example", ".html", ".htm", ".sql", ".json", ".yml", ".yaml",
    ".toml", ".css", ".js", ".mjs", ".ts", ".tsx", ".jsx", ".py", ".rb",
    ".go", ".rs", ".php", ".ex", ".exs", ".templ", ".md", ".txt", ".sh",
    ".clinerules", ".windsurfrules", ".mdc",
}

#: Extensionless files that are still parsed as text.
CHECKED_NAMES = {
    ".clinerules", ".windsurfrules", ".env.example", "Dockerfile",
    "docker-compose.yml", "Makefile",
}


def is_checked(path: str) -> bool:
    name = os.path.basename(path)
    if name in CHECKED_NAMES:
        return True
    return os.path.splitext(name)[1].lower() in CHECKED_EXTENSIONS


def scan() -> list[str]:
    found = []
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            path = os.path.join(root, name)
            if not is_checked(path):
                continue
            try:
                with open(path, "rb") as handle:
                    if handle.read(3) == BOM:
                        found.append(os.path.relpath(path, REPO_ROOT).replace("\\", "/"))
            except OSError:
                continue
    return sorted(found)


def strip(rel_paths: list[str]) -> None:
    for rel in rel_paths:
        path = os.path.join(REPO_ROOT, rel)
        with open(path, "rb") as handle:
            data = handle.read()
        with open(path, "wb") as handle:
            handle.write(data[len(BOM):])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fix", action="store_true", help="strip the BOMs in place")
    args = parser.parse_args()

    found = scan()
    if not found:
        print("PASS — no UTF-8 BOMs in parsed or served files")
        return 0

    if args.fix:
        strip(found)
        print(f"stripped UTF-8 BOM from {len(found)} file(s):")
        for rel in found:
            print(f"  - {rel}")
        return 0

    print(f"FAIL — {len(found)} file(s) start with a UTF-8 BOM:")
    for rel in found:
        print(f"  - {rel}")
    print("\nFix with: python tools/check_encoding.py --fix")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
