import os
import sys
import json
import subprocess

def run_eval(kit_slug):
    kit_dir = os.path.join("kits", kit_slug)
    if not os.path.isdir(kit_dir):
        print(f"[FAIL] Kit directory {kit_dir} not found.")
        return False

    print(f"\n==========================================")
    print(f" Running Evaluation: {kit_slug}")
    print(f"==========================================")

    # 1. Manifest
    p1 = subprocess.run(["python", "tools/validate_manifest.py", os.path.join(kit_dir, "kit.yaml")], capture_output=True, text=True)
    manifest_ok = (p1.returncode == 0)
    print(f"  [1] Manifest Validation: {'PASS' if manifest_ok else 'FAIL'}")

    # 2. Transpiler Drift Check
    p2 = subprocess.run(["python", "tools/transpiler.py", "--kit", kit_dir, "--check"], capture_output=True, text=True)
    transpiler_ok = (p2.returncode == 0)
    print(f"  [2] Transpiler Drift:   {'PASS' if transpiler_ok else 'FAIL'}")

    # 3. Secret Audit
    forbidden = ['AKIA', 'ghp_', 'sk-', 'BEGIN RSA PRIVATE KEY']
    secret_leak = False
    for root, dirs, files in os.walk(kit_dir):
        for f in files:
            if f.endswith(('.php', '.md', '.yaml', '.yml', '.env.example', '.json', '.ts', '.tsx', '.sql')):
                path = os.path.join(root, f)
                with open(path, 'r', errors='ignore') as cf:
                    text = cf.read()
                    for term in forbidden:
                        if term in text:
                            print(f"      CRITICAL: Secret pattern '{term}' found in {path}")
                            secret_leak = True
    print(f"  [3] Secret Invariant:   {'PASS' if not secret_leak else 'FAIL'}")

    # 4. Dialect Completeness (all 6 formats)
    expected_dialects = [
        os.path.join(kit_dir, "AGENTS.md"),
        os.path.join(kit_dir, "CLAUDE.md"),
        os.path.join(kit_dir, ".windsurfrules"),
        os.path.join(kit_dir, ".github", "copilot-instructions.md")
    ]
    dialects_ok = all(os.path.exists(d) for d in expected_dialects)
    print(f"  [4] 6 Agent Dialects:   {'PASS' if dialects_ok else 'FAIL'}")

    overall = manifest_ok and transpiler_ok and (not secret_leak) and dialects_ok
    print(f"  ----------------------------------------")
    print(f"  Overall Result:        {'[PASSED]' if overall else '[FAILED]'}")
    return overall

def main():
    slugs = [
        "laravel-filament-postgresql",
        "laravel-livewire-postgresql",
        "laravel-mongodb",
        "nextjs-approuter-supabase"
    ]

    results = {}
    for s in slugs:
        results[s] = run_eval(s)

    print("\n==========================================")
    print(" Evaluation Summary Report")
    print("==========================================")
    for s, ok in results.items():
        print(f"  - {s:<32}: {'PASS' if ok else 'FAIL'}")

    all_passed = all(results.values())
    if all_passed:
        print("\nAll evaluated kits passed 100% of benchmark checks!")
        sys.exit(0)
    else:
        print("\nSome kits failed evaluation checks.")
        sys.exit(1)

if __name__ == "__main__":
    main()
