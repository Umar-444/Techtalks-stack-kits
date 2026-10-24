import os
import sys
import yaml
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import security_checks as _sc

phase2_slugs = [
    "laravel-mysql",
    "django-tailwind-postgresql",
    "rag-fastapi-qdrant",
    "rag-llamaindex-pgvector",
    "rag-local-private",
    "go-chi-templ-htmx",
    "django-api-ninja",
    "python-litestar-postgresql",
    "flask-htmx-sqlite",
    "security-llm-guardrails",
    "security-passkeys-auth",
    "agentic-langgraph-crewai",
    "rag-langgraph-agentic",
    "rag-haystack-weaviate",
    "go-gin-postgresql",
    "go-fiber-api",
    "rust-actix-postgresql",
    "rust-loco-sqlite",
    "rust-leptos-fullstack",
    "elixir-phoenix-liveview",
    "reverse-engineering-security",
]

base_dir = "kits"
all_pass = True
results = []

for slug in phase2_slugs:
    kit_dir = os.path.join(base_dir, slug)
    kit_yaml_p = os.path.join(kit_dir, "kit.yaml")
    
    status = {"slug": slug, "errors": []}
    
    if not os.path.exists(kit_yaml_p):
        status["errors"].append("Missing kit.yaml")
        results.append(status)
        all_pass = False
        continue
        
    with open(kit_yaml_p, "r", encoding="utf-8") as f:
        meta = yaml.safe_load(f)
        
    # Check 1: Status
    if meta.get("status") != "stable":
        status["errors"].append(f"Status is {meta.get('status')} instead of stable")
        
    # Check 2: Dockerfile
    df_p = os.path.join(kit_dir, "starter", "Dockerfile")
    if not os.path.exists(df_p):
        status["errors"].append("Missing starter/Dockerfile")
    else:
        with open(df_p, "r", encoding="utf-8") as f:
            df_content = f.read()
            if "USER" not in df_content:
                status["errors"].append("Dockerfile lacks USER unprivileged directive")
                
    # Check 3: docker-compose.yml
    dc_p = os.path.join(kit_dir, "starter", "docker-compose.yml")
    if not os.path.exists(dc_p):
        status["errors"].append("Missing starter/docker-compose.yml")
        
    # Check 4: Source rules (>= 5)
    sr_dir = os.path.join(kit_dir, "rules", "source")
    if not os.path.exists(sr_dir):
        status["errors"].append("Missing rules/source directory")
    else:
        rules = [f for f in os.listdir(sr_dir) if f.endswith(".md")]
        if len(rules) < 5:
            status["errors"].append(f"Only {len(rules)} source rules (expected >= 5)")
            
    # Check 5: Skills (>= 4)
    sk_dir = os.path.join(kit_dir, "skills")
    if not os.path.exists(sk_dir):
        status["errors"].append("Missing skills directory")
    else:
        skills = [d for d in os.listdir(sk_dir) if os.path.isfile(os.path.join(sk_dir, d, "SKILL.md"))]
        if len(skills) < 4:
            status["errors"].append(f"Only {len(skills)} skills (expected >= 4)")
            
    # Check 6: Evals (>= 3)
    ev_dir = os.path.join(kit_dir, "evals", "tasks")
    if not os.path.exists(ev_dir):
        status["errors"].append("Missing evals/tasks directory")
    else:
        evals = [f for f in os.listdir(ev_dir) if f.endswith(".json")]
        if len(evals) < 3:
            status["errors"].append(f"Only {len(evals)} evals (expected >= 3)")
            
    # Check 7: Security checks — canonical v2 manifest with >= 12 controls
    sc_p = os.path.join(kit_dir, "security", "checks.json")
    if not os.path.exists(sc_p):
        status["errors"].append("Missing security/checks.json")
    else:
        try:
            manifest = _sc.load(sc_p)
            count = len(manifest["checks"])
            if count < _sc.MIN_CHECKS:
                status["errors"].append(f"Only {count} security controls (expected >= {_sc.MIN_CHECKS})")
            raw_version = json.load(open(sc_p, "r", encoding="utf-8")).get("schema_version")
            if raw_version != _sc.SCHEMA_VERSION:
                status["errors"].append(
                    f"checks.json is schema {raw_version or 'v1'}; "
                    "run tools/validate_checks.py --fix"
                )
        except Exception as e:
            status["errors"].append(f"Corrupt security/checks.json: {e}")
                
    # Check 8: FAQs (>= 14)
    faq_p = os.path.join(kit_dir, "faq.json")
    if not os.path.exists(faq_p):
        status["errors"].append("Missing faq.json")
    else:
        with open(faq_p, "r", encoding="utf-8") as f:
            try:
                faqs = json.load(f)
                if len(faqs) < 14:
                    status["errors"].append(f"Only {len(faqs)} FAQs (expected >= 14)")
            except Exception as e:
                status["errors"].append(f"Corrupt faq.json: {e}")
                
    # Check 9: VERIFICATION.md
    v_p = os.path.join(kit_dir, "VERIFICATION.md")
    if not os.path.exists(v_p):
        status["errors"].append("Missing VERIFICATION.md")
        
    # Check 10: CODEX.md & .clinerules
    if not os.path.exists(os.path.join(kit_dir, "CODEX.md")):
        status["errors"].append("Missing CODEX.md")
    if not os.path.exists(os.path.join(kit_dir, ".clinerules")):
        status["errors"].append("Missing .clinerules")
        
    # Check 11: agent-build-steps.md
    if not os.path.exists(os.path.join(kit_dir, "steps", "agent-build-steps.md")):
        status["errors"].append("Missing steps/agent-build-steps.md")
        
    results.append(status)
    if status["errors"]:
        all_pass = False

print(f"Audited {len(phase2_slugs)} Phase 2 Blueprint Kits:")
for r in results:
    if r["errors"]:
        print(f"  [FAIL] {r['slug']}: " + "; ".join(r["errors"]))
    else:
        print(f"  [PASS] {r['slug']}: All 18 checkpoints verified!")

if all_pass:
    print("\n=======================================================")
    print(" OVERALL AUDIT: 100% PERFECT! All 21 Phase 2 Kits pass!")
    print("=======================================================")
else:
    print("\n[!] Some kits need attention.")
    sys.exit(1)
