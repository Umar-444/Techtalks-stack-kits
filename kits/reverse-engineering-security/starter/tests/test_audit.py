import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tempfile
import os
import pytest
from analyzers.ast_analyzer import audit_file
from analyzers.binary_checker import audit_binary_headers

def test_ast_detects_eval_and_exec():
    code = """
def run_dynamic(payload):
    eval(payload)
    exec(payload)
"""
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(code)
        f.flush()
        temp_path = f.name

    try:
        findings = audit_file(temp_path)
        rule_ids = [f.rule_id for f in findings]
        assert "SEC-AST-001" in rule_ids
        assert len(findings) == 2
    finally:
        os.remove(temp_path)

def test_ast_detects_shell_true():
    code = """
import subprocess
def run_command(cmd):
    subprocess.Popen(cmd, shell=True)
"""
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(code)
        f.flush()
        temp_path = f.name

    try:
        findings = audit_file(temp_path)
        rule_ids = [f.rule_id for f in findings]
        assert "SEC-AST-002" in rule_ids
    finally:
        os.remove(temp_path)

def test_ast_detects_sql_concatenation():
    code = """
def get_user(db, user_id):
    db.execute(f"SELECT * FROM users WHERE id = {user_id}")
"""
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(code)
        f.flush()
        temp_path = f.name

    try:
        findings = audit_file(temp_path)
        rule_ids = [f.rule_id for f in findings]
        assert "SEC-AST-003" in rule_ids
    finally:
        os.remove(temp_path)

def test_ast_clean_code_passes():
    code = """
def safe_query(db, user_id):
    # Parameterized query
    return db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
"""
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(code)
        f.flush()
        temp_path = f.name

    try:
        findings = audit_file(temp_path)
        assert len(findings) == 0
    finally:
        os.remove(temp_path)

