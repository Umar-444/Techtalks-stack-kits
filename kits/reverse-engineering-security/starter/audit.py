"""Convenience entry point: scan a path and report what was actually found."""
import sys

from cli import scan_path


def run_audit(target: str = ".") -> int:
    findings = scan_path(target)
    print(f"Security audit scan complete: {len(findings)} finding(s) in {target}.")
    return 1 if any(f.severity == "HIGH" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(run_audit(sys.argv[1] if len(sys.argv) > 1 else "."))
