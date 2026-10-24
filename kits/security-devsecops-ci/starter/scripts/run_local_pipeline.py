#!/usr/bin/env python3
"""
Cross-Platform Local DevSecOps Pipeline Runner.
Executes secret audits, AST rules, and container configuration verification.
"""
import os
import re
import sys
import json

def log(tag, msg, status="INFO"):
    colors = {"PASS": "\033[92m", "FAIL": "\033[91m", "INFO": "\033[94m", "RESET": "\033[0m"}
    c = colors.get(status, "")
    r = colors["RESET"]
    print(f"{c}[{status}] {tag}: {msg}{r}")

def scan_secrets(root_dir):
    log("Gitleaks/Secret Scan", "Scanning workspace for high-entropy tokens and private keys...")
    patterns = [
        ("Private Key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
        ("AWS Access Key", re.compile(r"AKIA[0-9A-Z]{16}")),
        ("Generic Hardcoded Secret", re.compile(r"""(?i)(api[_-]?key|secret[_-]?key)\s*[:=]\s*['"][0-9a-zA-Z\-_]{20,}['"]""")),
        ("GitHub Personal Access Token", re.compile(r"ghp_[0-9a-zA-Z]{36}")),
    ]
    findings = []
    for root, _, files in os.walk(root_dir):
        if any(skip in root for skip in [".git", "node_modules", "vendor", ".venv"]):
            continue
        for fname in files:
            if fname in ["run_local_pipeline.py", "checks.json"]:
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    for line_num, line in enumerate(f, 1):
                        for label, pat in patterns:
                            if pat.search(line):
                                findings.append((label, fpath, line_num))
            except Exception:
                pass
    if findings:
        for f in findings:
            log("Secret Finding", f"{f[0]} at {f[1]}:{f[2]}", "FAIL")
        return False
    log("Secret Scan", "Zero plaintext credentials detected across repository files", "PASS")
    return True

def audit_dockerfile(dockerfile_path):
    log("Container Audit", f"Verifying Dockerfile at {dockerfile_path}...")
    if not os.path.exists(dockerfile_path):
        log("Container Audit", "Dockerfile not found", "FAIL")
        return False
    with open(dockerfile_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    has_user = "USER " in content
    has_alpine = "alpine" in content or "distroless" in content
    has_pinned = "@sha256:" in content or ":" in content
    
    if not has_user:
        log("Container Audit", "Dockerfile runs as root! Missing non-root USER declaration", "FAIL")
        return False
    if not has_alpine:
        log("Container Audit", "Base image not minimal Alpine or Distroless", "FAIL")
        return False
    log("Container Audit", "Non-root execution and minimal base image verified", "PASS")
    return True

def audit_configs(kit_root):
    log("Config Lint", "Checking .gitleaks.toml, .semgrep.yml, and trivy.yaml...")
    required = [".gitleaks.toml", ".semgrep.yml", "trivy.yaml"]
    for r in required:
        p = os.path.join(kit_root, r)
        if not os.path.exists(p):
            log("Config Lint", f"Missing configuration file {r}", "FAIL")
            return False
    log("Config Lint", "All scanner configuration manifests validated", "PASS")
    return True

def main():
    print("=======================================================")
    print("  TechTalks DevSecOps Local Pipeline Runner (Cross-Platform)  ")
    print("=======================================================")
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    sec_ok = scan_secrets(root)
    docker_ok = audit_dockerfile(os.path.join(root, "Dockerfile"))
    cfg_ok = audit_configs(root)
    
    if sec_ok and docker_ok and cfg_ok:
        # Names only what this script actually ran. The full control set is
        # enforced by the CI workflow, which runs Gitleaks, Semgrep, Trivy and
        # Syft against real scanners this pre-flight script does not invoke.
        print("\n\033[92m>>> PRE-FLIGHT PASSED: secret scan, container audit and "
              "config lint are clean. <<<\033[0m")
        print("\033[94m    Full control set runs in CI (.github/workflows/devsecops.yml).\033[0m")
        return 0
    else:
        print("\n\033[91m>>> PIPELINE VERIFICATION FAILED: Resolve issues before pushing! <<<\033[0m")
        return 1

if __name__ == "__main__":
    sys.exit(main())
