import os
import sys
import yaml

MANDATORY_ROOT_KEYS = [
    "schema_version", "name", "slug", "version", "status",
    "description", "maintainer", "stack", "layers", "security", "install"
]

MANDATORY_STACK_KEYS = ["language", "framework", "database"]

MANDATORY_LAYERS = ["starter", "rules", "skills", "design", "security", "steps"]

def validate_kit_manifest(manifest_path):
    print(f"Validating kit manifest: {manifest_path}")
    if not os.path.exists(manifest_path):
        print(f"ERROR: File not found: {manifest_path}")
        return False

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

    # 3. Layers
    layers = data.get("layers", {})
    for lk in MANDATORY_LAYERS:
        if lk not in layers:
            errors.append(f"Missing mandatory layer key: 'layers.{lk}'")

    # 4. Security checks
    sec = data.get("security", {})
    if "rules_enforced" not in sec:
        errors.append("Missing 'security.rules_enforced' block")
    else:
        rules = sec["rules_enforced"]
        for expected in ["zero_plaintext_credentials", "strict_parameterized_queries", "authorization_on_every_resource"]:
            if not rules.get(expected, False):
                errors.append(f"Security rule '{expected}' must be true")

    if errors:
        print(f"FAILED: {len(errors)} validation error(s) found:")
        for err in errors:
            print(f"  [X] {err}")
        return False

    print("SUCCESS: Kit manifest passed all validation checks!")
    print(f"  - Kit Name: {data.get('name')}")
    print(f"  - Slug: {data.get('slug')}")
    print(f"  - Stack: {stack.get('language', {}).get('name')} + {stack.get('framework', {}).get('name')} + {stack.get('database', {}).get('engine')}")
    print(f"  - Status: {data.get('status')}")
    return True

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "templates/kit.yaml"
    success = validate_kit_manifest(path)
    sys.exit(0 if success else 1)
