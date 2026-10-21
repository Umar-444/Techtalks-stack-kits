#!/usr/bin/env python3
"""
TechTalks Stack Kits — Single-Source Agent Rules Transpiler
Reference: 03-Agent-Rules-Standard.md & 09-Agent-Master-Brief.md

Transpiles modular rules in rules/source/*.md into all 6 agent dialects:
1. Codex / Standard -> AGENTS.md
2. Claude Code      -> CLAUDE.md
3. Cursor IDE       -> .cursor/rules/*.mdc
4. GitHub Copilot   -> .github/copilot-instructions.md
5. Google Antigravity -> .agents/rules/*.md
6. Windsurf         -> .windsurfrules
"""

import os
import sys
import re
import argparse
import yaml

def parse_source_rule(filepath):
    """Parses a markdown source rule file with YAML frontmatter."""
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    frontmatter = {}
    body = raw
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) >= 3:
            try:
                frontmatter = yaml.safe_load(parts[1]) or {}
                body = parts[2].strip()
            except Exception as e:
                print(f"Warning: Failed to parse frontmatter in {filepath}: {e}")

    rule_id = frontmatter.get("id", os.path.splitext(os.path.basename(filepath))[0])
    title = frontmatter.get("title", rule_id.replace("-", " ").title())
    description = frontmatter.get("description", "")
    globs = frontmatter.get("globs", "*")
    always_apply = frontmatter.get("alwaysApply", True)

    return {
        "id": rule_id,
        "title": title,
        "description": description,
        "globs": globs,
        "always_apply": always_apply,
        "body": body,
        "source_file": filepath
    }

def transpile_kit_rules(kit_dir, check_mode=False):
    """Transpiles rules/source/*.md into all target dialects for a kit."""
    source_dir = os.path.join(kit_dir, "rules", "source")
    if not os.path.isdir(source_dir):
        print(f"[SKIP] No rules/source/ directory found in {kit_dir}")
        return True

    rule_files = sorted([os.path.join(source_dir, f) for f in os.listdir(source_dir) if f.endswith(".md")])
    if not rule_files:
        print(f"[SKIP] No *.md files in {source_dir}")
        return True

    rules = [parse_source_rule(rf) for rf in rule_files]
    kit_name = os.path.basename(os.path.abspath(kit_dir)).replace("-", " ").title()

    # Read kit.yaml if present for metadata
    manifest_path = os.path.join(kit_dir, "kit.yaml")
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, "r", encoding="utf-8") as mf:
                mdata = yaml.safe_load(mf)
                if mdata and "name" in mdata:
                    kit_name = mdata["name"]
        except Exception:
            pass

    print(f"=== Transpiling {len(rules)} rules for: {kit_name} ===")

    # 1. Output: AGENTS.md (Root of kit)
    agents_content = f"# {kit_name} — Agent Operating Rules (AGENTS.md)\n"
    agents_content += "# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.\n\n"
    agents_content += "## Table of Contents\n"
    for r in rules:
        agents_content += f"- [{r['title']}](#{r['id']})\n"
    agents_content += "\n---\n\n"
    for r in rules:
        agents_content += f"<a id=\"{r['id']}\"></a>\n"
        agents_content += f"## {r['title']}\n\n"
        agents_content += f"{r['body']}\n\n---\n\n"

    # 2. Output: CLAUDE.md (Root of kit)
    claude_content = f"# {kit_name} — Claude Code Guidelines (CLAUDE.md)\n"
    claude_content += "# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.\n\n"
    claude_content += "## Quick Reference & Non-Negotiable Standards\n"
    for r in rules:
        claude_content += f"### {r['title']}\n"
        if r['description']:
            claude_content += f"> {r['description']}\n\n"
        claude_content += f"{r['body']}\n\n"

    # 3. Output: .github/copilot-instructions.md
    copilot_content = f"# GitHub Copilot Instructions for {kit_name}\n"
    copilot_content += "# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.\n\n"
    for r in rules:
        copilot_content += f"## {r['title']}\n{r['body']}\n\n"

    # 4. Output: .windsurfrules
    windsurf_content = f"# Windsurf Rules — {kit_name}\n"
    windsurf_content += "# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.\n\n"
    for r in rules:
        windsurf_content += f"## {r['title']}\n{r['body']}\n\n"

    # Targets to write
    files_to_write = {
        os.path.join(kit_dir, "AGENTS.md"): agents_content,
        os.path.join(kit_dir, "CLAUDE.md"): claude_content,
        os.path.join(kit_dir, ".github", "copilot-instructions.md"): copilot_content,
        os.path.join(kit_dir, ".windsurfrules"): windsurf_content
    }

    # 5. Output: .cursor/rules/<id>.mdc
    cursor_dir = os.path.join(kit_dir, ".cursor", "rules")
    for r in rules:
        cursor_mdc = f"---\ndescription: {r['description'] or r['title']}\nglobs: {r['globs']}\nalwaysApply: {'true' if r['always_apply'] else 'false'}\n---\n\n"
        cursor_mdc += f"# {r['title']}\n\n{r['body']}\n"
        files_to_write[os.path.join(cursor_dir, f"{r['id']}.mdc")] = cursor_mdc

    # 6. Output: .agents/rules/<id>.md (Google Antigravity format)
    antigravity_dir = os.path.join(kit_dir, ".agents", "rules")
    for r in rules:
        ag_md = f"# {r['title']}\n\n{r['body']}\n"
        files_to_write[os.path.join(antigravity_dir, f"{r['id']}.md")] = ag_md

    # Write or Check
    drift_detected = False
    for target_path, expected_content in files_to_write.items():
        if check_mode:
            if not os.path.exists(target_path):
                print(f"[DRIFT] Missing generated file: {target_path}")
                drift_detected = True
            else:
                with open(target_path, "r", encoding="utf-8") as existing_f:
                    if existing_f.read() != expected_content:
                        print(f"[DRIFT] Content drift in: {target_path}")
                        drift_detected = True
        else:
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            with open(target_path, "w", encoding="utf-8") as out_f:
                out_f.write(expected_content)
            rel_p = os.path.relpath(target_path, kit_dir)
            print(f"  -> Generated: {rel_p}")

    if check_mode:
        if drift_detected:
            print("[FAILED] Rule transpilation drift detected. Run transpiler to synchronize.")
            return False
        else:
            print("[PASSED] All agent dialect outputs match rules/source/* perfectly!")
            return True

    print(f"[SUCCESS] All 6 agent dialects generated cleanly for {kit_name}!")
    return True

def main():
    parser = argparse.ArgumentParser(description="Single-Source Agent Rules Transpiler")
    parser.add_argument("--kit", type=str, default=None, help="Path to specific kit directory")
    parser.add_argument("--check", action="store_true", help="Check mode: verify generated files match source without modifying")
    args = parser.parse_args()

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    if args.kit:
        kits = [os.path.abspath(args.kit)]
    else:
        # Check all kits under kits/ directory
        kits_base = os.path.join(repo_root, "kits")
        if os.path.isdir(kits_base):
            kits = [os.path.join(kits_base, k) for k in os.listdir(kits_base) if os.path.isdir(os.path.join(kits_base, k))]
        else:
            kits = []

    if not kits:
        print("No kits found to transpile. Specify a kit with --kit <path>")
        sys.exit(0)

    overall_success = True
    for k in kits:
        success = transpile_kit_rules(k, check_mode=args.check)
        if not success:
            overall_success = False

    sys.exit(0 if overall_success else 1)

if __name__ == "__main__":
    main()
