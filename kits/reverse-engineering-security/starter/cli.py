import argparse
import os
import sys
from analyzers.ast_analyzer import audit_file
from analyzers.binary_checker import audit_binary_headers
from reporting.sarif_report import generate_sarif
from reporting.console_report import render_console

def scan_path(target_path: str):
    all_findings = []
    if os.path.isfile(target_path):
        all_findings.extend(audit_file(target_path))
    elif os.path.isdir(target_path):
        for root, _, files in os.walk(target_path):
            for file in files:
                if file.endswith(".py"):
                    full_p = os.path.join(root, file)
                    all_findings.extend(audit_file(full_p))
    return all_findings

def main():
    parser = argparse.ArgumentParser(description="Security Audit & Reverse Engineering Analysis CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Command: scan
    scan_cmd = subparsers.add_parser("scan", help="Scan source code using AST security analyzers")
    scan_cmd.add_argument("--path", required=True, help="Target file or directory to scan")
    scan_cmd.add_argument("--format", choices=["console", "sarif"], default="console", help="Report format")
    scan_cmd.add_argument("--out", default=None, help="Output file path")

    # Command: checksec
    sec_cmd = subparsers.add_parser("checksec", help="Inspect compiled binary security mitigations")
    sec_cmd.add_argument("--binary", required=True, help="Path to compiled executable")

    # Command: health
    subparsers.add_parser("health", help="Output health and status metadata")

    args = parser.parse_args()

    if args.command == "health":
        print('{"status": "ok", "app": "reverse-engineering-security", "version": "1.0.0"}')
        sys.exit(0)

    elif args.command == "scan":
        findings = scan_path(args.path)
        if args.format == "sarif":
            sarif_json = generate_sarif(findings)
            if args.out:
                with open(args.out, "w", encoding="utf-8") as f:
                    f.write(sarif_json)
                print(f"SARIF report written to {args.out}")
            else:
                print(sarif_json)
        else:
            render_console(findings)

        # Non-zero exit code on HIGH findings for CI gating
        high_severity = any(f.severity == "HIGH" for f in findings)
        sys.exit(1 if high_severity else 0)

    elif args.command == "checksec":
        res = audit_binary_headers(args.binary)
        print(f"\n[Binary Checksec Audit] {res.binary_path} (Format: {res.format})")
        print(f"  NX / DEP:        {'[PASS]' if res.nx_enabled else '[FAIL]'}")
        print(f"  PIE / ASLR:      {'[PASS]' if res.pie_aslr_enabled else '[FAIL]'}")
        print(f"  Stack Canary:    {'[PASS]' if res.canary_detected else '[FAIL]'}")
        last_label = "Control Flow Guard:" if res.format == "PE" else "Full RELRO:"
        print(f"  {last_label:<16} {'[PASS]' if res.relro_detected else '[FAIL]'}")
        if res.remediation_notes:
            print("\n  Remediation Actions Required:")
            for note in res.remediation_notes:
                print(f"    - {note}")
        sys.exit(0)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
