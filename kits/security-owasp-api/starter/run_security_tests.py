#!/usr/bin/env python3
"""
CLI Test Runner for OWASP API Security Top 10 Verification Suite.
"""
import sys
import subprocess
import os

def main():
    print("=======================================================")
    print("   OWASP API Security Top 10 (2023) Verification Run   ")
    print("=======================================================")
    
    test_file = os.path.join(os.path.dirname(__file__), "tests", "test_owasp_top10.py")
    cmd = [sys.executable, "-m", "pytest", "-v", test_file]
    
    res = subprocess.run(cmd)
    if res.returncode == 0:
        print("\n\033[92m>>> ALL OWASP API SECURITY TESTS PASSED (100% Compliance) <<<\033[0m")
        return 0
    else:
        print("\n\033[91m>>> OWASP API SECURITY TESTS FAILED <<<\033[0m")
        return res.returncode

if __name__ == "__main__":
    sys.exit(main())
