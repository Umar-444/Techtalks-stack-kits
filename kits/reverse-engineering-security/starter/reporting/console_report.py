from typing import List
from analyzers.ast_analyzer import Finding

def render_console(findings: List[Finding]):
    print(f"\n=======================================================")
    print(f" SECURITY AUDIT SCAN RESULTS: {len(findings)} Finding(s)")
    print(f"=======================================================")
    if not findings:
        print("[OK] Zero security vulnerabilities detected.")
        return

    for idx, f in enumerate(findings, 1):
        print(f"\n[{idx}] [{f.severity}] {f.rule_id} at {f.file_path}:{f.line}:{f.col}")
        print(f"    Message: {f.message}")
        if f.snippet:
            print(f"    Code:    {f.snippet}")
