import os
import sys
import yaml
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import security_checks as sc

def audit(slug):
    kit_dir = os.path.join("kits", slug)
    kit_yaml_p = os.path.join(kit_dir, "kit.yaml")

    errors = []
    if not os.path.exists(kit_yaml_p):
        return [f"Missing kit.yaml in {kit_dir}"]

    with open(kit_yaml_p, "r", encoding="utf-8") as f:
        y = yaml.safe_load(f)

    if y.get("status") != "stable":
        errors.append(f"kit.yaml status is {y.get('status')} (must be stable)")

    # 1. kit.yaml schema
    for k in ["schema_version", "name", "slug", "version", "status", "maintainer", "stack", "layers", "security", "install"]:
        if k not in y:
            errors.append(f"kit.yaml missing key: {k}")

    layers = y.get("layers", {})
    for lk in ["starter", "rules", "skills", "evals", "design", "security", "steps"]:
        if lk not in layers:
            errors.append(f"layers missing subkey: {lk}")

    # 2. README.md
    readme_p = os.path.join(kit_dir, "README.md")
    if not os.path.exists(readme_p) or os.path.getsize(readme_p) < 200:
        errors.append("README.md missing or too small")

    # 3. starter / Dockerfile rootless
    dockerfile_p = os.path.join(kit_dir, "starter", "Dockerfile")
    if os.path.exists(dockerfile_p):
        with open(dockerfile_p, "r", encoding="utf-8") as f:
            df = f.read()
            if "USER 10001:10001" not in df and "USER " not in df:
                errors.append("Dockerfile missing non-root USER directive")
    else:
        errors.append("Missing starter/Dockerfile")

    dc_p = os.path.join(kit_dir, "starter", "docker-compose.yml")
    if not os.path.exists(dc_p):
        errors.append("Missing starter/docker-compose.yml")

    # 4. VERIFICATION.md
    ver_p = os.path.join(kit_dir, "VERIFICATION.md")
    if not os.path.exists(ver_p) or os.path.getsize(ver_p) < 200:
        errors.append("Missing or incomplete VERIFICATION.md")

    # 5. rules/source
    rules_src = os.path.join(kit_dir, "rules", "source")
    if not os.path.exists(rules_src) or len(os.listdir(rules_src)) < 5:
        errors.append("Fewer than 5 source rules")

    # 6. Dialects
    for d in ["AGENTS.md", "CLAUDE.md", "CODEX.md", ".clinerules", ".windsurfrules", os.path.join(".github", "copilot-instructions.md")]:
        if not os.path.exists(os.path.join(kit_dir, d)):
            errors.append(f"Missing agent dialect: {d}")

    cursor_dir = os.path.join(kit_dir, ".cursor", "rules")
    if not os.path.exists(cursor_dir) or len([f for f in os.listdir(cursor_dir) if f.endswith(".mdc")]) < 5:
        errors.append("Missing Cursor .mdc rules")

    agents_dir = os.path.join(kit_dir, ".agents", "rules")
    if not os.path.exists(agents_dir) or len([f for f in os.listdir(agents_dir) if f.endswith(".md")]) < 5:
        errors.append("Missing Antigravity .agents rules")

    # 7 & 8 & 9. Skills
    skills_dir = os.path.join(kit_dir, "skills")
    if not os.path.exists(skills_dir) or len(os.listdir(skills_dir)) < 4:
        errors.append("Fewer than 4 skills")

    for sk in ["install-and-verify", "first-feature"]:
        sk_p = os.path.join(skills_dir, sk, "SKILL.md")
        if not os.path.exists(sk_p):
            errors.append(f"Missing core skill: {sk}")

    # 11. DESIGN.md / DESIGN-NOTES.md
    if not os.path.exists(os.path.join(kit_dir, "DESIGN.md")) and not os.path.exists(os.path.join(kit_dir, "DESIGN-NOTES.md")):
        errors.append("Missing DESIGN.md or DESIGN-NOTES.md")

    # 12. security/checks.json — canonical v2 schema, >= 12 OWASP-mapped controls
    sec_p = os.path.join(kit_dir, "security", "checks.json")
    if os.path.exists(sec_p):
        try:
            raw = json.load(open(sec_p, "r", encoding="utf-8"))
            if raw.get("schema_version") != sc.SCHEMA_VERSION:
                errors.append(
                    f"security/checks.json is not schema v{sc.SCHEMA_VERSION}; "
                    "run tools/validate_checks.py --fix"
                )
            else:
                for problem in sc.validate(raw):
                    errors.append(f"security/checks.json {problem}")
        except (json.JSONDecodeError, sc.ManifestError) as exc:
            errors.append(f"security/checks.json unreadable: {exc}")
    else:
        errors.append("Missing security/checks.json")

    # 14. steps
    steps_p = os.path.join(kit_dir, "steps", "agent-build-steps.md")
    if not os.path.exists(steps_p):
        errors.append("Missing steps/agent-build-steps.md")

    # 15 & 16. faq.json (>= 14 FAQs)
    faq_p = os.path.join(kit_dir, "faq.json")
    if os.path.exists(faq_p):
        with open(faq_p, "r", encoding="utf-8") as f:
            faqs = json.load(f)
            if len(faqs) < 14:
                errors.append(f"faq.json has only {len(faqs)} items (minimum 14)")
    else:
        errors.append("Missing faq.json")

    # 18. evals
    evals_dir = os.path.join(kit_dir, "evals", "tasks")
    if not os.path.exists(evals_dir) or len(os.listdir(evals_dir)) < 3:
        errors.append("evals/tasks missing or fewer than 3 tasks")

    return errors

if __name__ == "__main__":
    slug = sys.argv[1] if len(sys.argv) > 1 else "laravel-filament-mysql"
    errs = audit(slug)
    if not errs:
        print(f"[PASS] {slug}: All 18 checkpoints verified perfectly!")
    else:
        print(f"[FAIL] {slug}:")
        for e in errs:
            print(f"  - {e}")
        sys.exit(1)
