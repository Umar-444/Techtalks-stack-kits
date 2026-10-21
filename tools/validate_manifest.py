"""
tools/validate_manifest.py
CLI Validator for TechTalks Stack Kit Manifests (kit.yaml).
Enforces:
1. Manifest syntax and mandatory YAML schema keys.
2. Physical existence of all declared layer files & directories on disk.
3. Non-empty starter and rule source directories.
"""

import os
import sys
import yaml

MANDATORY_ROOT_KEYS = [
    "schema_version", "name", "slug", "version", "status",
    "description", "maintainer", "stack", "layers", "security", "install"
]

MANDATORY_STACK_KEYS = ["language", "framework"]

MANDATORY_LAYERS = ["starter", "rules", "skills", "design", "security", "steps"]

def validate_kit_manifest(manifest_path):
    print(f"Validating kit manifest: {manifest_path}")
    if not os.path.exists(manifest_path):
        print(f"ERROR: Manifest file not found on disk: {manifest_path}")
        return False

    kit_dir = os.path.dirname(os.path.abspath(manifest_path))

    with open(manifest_path, "r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
        except Exception as e:
            print(f"ERROR: Invalid YAML syntax: {e}")
            return False

    errors = []

    # 1. Root keys
    for k in MANDATORY_ROOT_KEYS:
        if k not in data:
            errors.append(f"Missing mandatory root key: '{k}'")

    # 2. Stack components
    stack = data.get("stack", {})
    for sk in MANDATORY_STACK_KEYS:
        if sk not in stack:
            errors.append(f"Missing mandatory stack key: 'stack.{sk}'")

    # 3. Layers & Physical Disk Existence Checks
    layers = data.get("layers", {})
    for lk in MANDATORY_LAYERS:
        if lk not in layers:
            errors.append(f"Missing mandatory layer key: 'layers.{lk}'")

    # Physical Path Verifications
    # (a) Starter
    starter_layer = layers.get("starter", {})
    starter_rel = starter_layer.get("path") if isinstance(starter_layer, dict) else str(starter_layer)
    if starter_rel:
        starter_abs = os.path.normpath(os.path.join(kit_dir, starter_rel))
        if not os.path.isdir(starter_abs):
            errors.append(f"Declared layers.starter directory does not exist on disk: '{starter_rel}'")
        else:
            files_in_starter = [f for f in os.listdir(starter_abs) if os.path.isfile(os.path.join(starter_abs, f))]
            if not files_in_starter:
                errors.append(f"Declared layers.starter directory is empty: '{starter_rel}'")

    # (b) Rules
    rules_layer = layers.get("rules", {})
    rules_src_rel = rules_layer.get("source_dir") if isinstance(rules_layer, dict) else None
    if rules_src_rel:
        rules_abs = os.path.normpath(os.path.join(kit_dir, rules_src_rel))
        if not os.path.isdir(rules_abs):
            errors.append(f"Declared layers.rules.source_dir does not exist on disk: '{rules_src_rel}'")
        else:
            md_rules = [f for f in os.listdir(rules_abs) if f.endswith(".md")]
            if not md_rules:
                errors.append(f"No rule files (.md) found inside layers.rules.source_dir: '{rules_src_rel}'")

    # (c) Skills
    skills_layer = layers.get("skills", {})
    if isinstance(skills_layer, dict):
        skills_dir_rel = skills_layer.get("dir")
        if skills_dir_rel:
            skills_abs = os.path.normpath(os.path.join(kit_dir, skills_dir_rel))
            if not os.path.isdir(skills_abs):
                errors.append(f"Declared layers.skills.dir does not exist on disk: '{skills_dir_rel}'")

        manifest_skills = skills_layer.get("manifest", [])
        for sk in manifest_skills:
            sk_path = sk.get("path")
            if sk_path:
                sk_abs = os.path.normpath(os.path.join(kit_dir, sk_path))
                if not os.path.isfile(sk_abs):
                    errors.append(f"Declared skill file does not exist on disk: '{sk_path}'")

    # (d) Design System
    design_layer = layers.get("design", {})
    design_rel = design_layer.get("path") if isinstance(design_layer, dict) else str(design_layer)
    if design_rel:
        design_abs = os.path.normpath(os.path.join(kit_dir, design_rel))
        if not os.path.isfile(design_abs):
            errors.append(f"Declared layers.design file does not exist on disk: '{design_rel}'")

    # (e) Security Layer
    sec_layer = layers.get("security", {})
    if isinstance(sec_layer, dict):
        sec_dir_rel = sec_layer.get("config_dir")
        if sec_dir_rel:
            sec_abs = os.path.normpath(os.path.join(kit_dir, sec_dir_rel))
            if not os.path.isdir(sec_abs):
                errors.append(f"Declared layers.security.config_dir does not exist on disk: '{sec_dir_rel}'")

    # (f) Agent Build Steps
    steps_layer = layers.get("steps", {})
    steps_rel = steps_layer.get("path") if isinstance(steps_layer, dict) else str(steps_layer)
    if steps_rel:
        steps_abs = os.path.normpath(os.path.join(kit_dir, steps_rel))
        if not os.path.isfile(steps_abs):
            errors.append(f"Declared layers.steps file does not exist on disk: '{steps_rel}'")

    # 4. Security Rules Invariants
    sec = data.get("security", {})
    if "rules_enforced" not in sec:
        errors.append("Missing 'security.rules_enforced' block")
    else:
        rules = sec["rules_enforced"]
        for expected in ["zero_plaintext_credentials", "strict_parameterized_queries", "authorization_on_every_resource"]:
            if not rules.get(expected, False):
                errors.append(f"Security invariant '{expected}' must be true")

    if errors:
        print(f"FAILED: {len(errors)} validation error(s) found:")
        for err in errors:
            print(f"  [X] {err}")
        return False

    print("SUCCESS: Kit manifest and physical layer files passed all validation checks!")
    print(f"  - Kit Name: {data.get('name')}")
    print(f"  - Slug: {data.get('slug')}")
    print(f"  - Verified on Disk: starter, rules, skills, design, security, steps")
    print(f"  - Status: {data.get('status')}")
    return True

if __name__ == "__main__":
    import glob
    target = sys.argv[1] if len(sys.argv) > 1 else "--all"
    if target == "--all":
        manifests = glob.glob("kits/*/kit.yaml")
        all_passed = True
        for m in sorted(manifests):
            print("\n" + "="*50)
            if not validate_kit_manifest(m):
                all_passed = False
        sys.exit(0 if all_passed else 1)
    else:
        success = validate_kit_manifest(target)
        sys.exit(0 if success else 1)
