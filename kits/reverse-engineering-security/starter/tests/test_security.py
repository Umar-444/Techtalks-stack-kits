"""Controls declared in security/checks.json, proved against real inputs.

This kit's product is the analyzers themselves, so each control is exercised by
feeding the tool known-bad and known-good input and checking what it reports:

  AST-01..03   dangerous-sink rules, on source files written to a temp dir
  BIN-01..03   header parsing, on synthetic ELF/PE images built byte by byte
  OPS-01       SARIF 2.1.0 structure
  OPS-02       Dockerfile is rootless
  OPS-03       CLI exit status gates on HIGH findings

SCA-01..03 (SBOM validation, hash pinning, CVE correlation) are declared as
rules only; the starter has no code for them, so they are not asserted here.
"""

import json
import os
import re
import struct
import subprocess
import sys

import pytest

STARTER = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, STARTER)

from analyzers.ast_analyzer import audit_file  # noqa: E402
from analyzers.binary_checker import audit_binary_headers  # noqa: E402
from reporting.sarif_report import generate_sarif  # noqa: E402

CLI = os.path.join(STARTER, "cli.py")


def run_cli(*args):
    return subprocess.run([sys.executable, CLI, *args], capture_output=True, text=True, cwd=STARTER)


def scan_source(tmp_path, code):
    path = tmp_path / "sample.py"
    path.write_text(code, encoding="utf-8")
    return audit_file(str(path))


def rule_ids(findings):
    return sorted(f.rule_id for f in findings)


# --- AST-01: eval / exec ----------------------------------------------------

def test_eval_and_exec_are_flagged_high(tmp_path):
    findings = scan_source(tmp_path, "def f(x):\n    eval(x)\n    exec(x)\n")
    assert rule_ids(findings) == ["SEC-AST-001", "SEC-AST-001"]
    assert all(f.severity == "HIGH" for f in findings)
    assert [f.line for f in findings] == [2, 3]


def test_method_named_eval_on_an_object_is_not_a_false_positive(tmp_path):
    assert scan_source(tmp_path, "model.eval()\nmodel.exec_()\n") == []


# --- AST-02: subprocess shell=True -----------------------------------------

@pytest.mark.parametrize("call", [
    "subprocess.Popen(c, shell=True)",
    "subprocess.run(c, shell=True)",
    "subprocess.call(c, shell=True)",
    "subprocess.check_output(c, shell=True)",
    "subprocess.check_call(c, shell=True)",
])
def test_shell_true_is_flagged_for_every_subprocess_entry_point(tmp_path, call):
    findings = scan_source(tmp_path, f"import subprocess\n{call}\n")
    assert rule_ids(findings) == ["SEC-AST-002"]


def test_argument_list_without_shell_is_clean(tmp_path):
    assert scan_source(tmp_path, "import subprocess\nsubprocess.run(['ls', '-l'])\n") == []
    assert scan_source(tmp_path, "import subprocess\nsubprocess.run(['ls'], shell=False)\n") == []


# --- AST-03: SQL built by string formatting --------------------------------

@pytest.mark.parametrize("expr", [
    'f"SELECT * FROM t WHERE id = {uid}"',
    '"SELECT * FROM t WHERE id = " + uid',
    '"SELECT * FROM t WHERE id = %s" % uid',
    '"SELECT * FROM t WHERE id = {}".format(uid)',
])
def test_dynamic_sql_is_flagged(tmp_path, expr):
    findings = scan_source(tmp_path, f"def q(db, uid):\n    db.execute({expr})\n")
    assert rule_ids(findings) == ["SEC-AST-003"], expr


def test_parameterized_sql_is_clean(tmp_path):
    code = 'def q(db, uid):\n    return db.execute("SELECT * FROM t WHERE id = ?", (uid,))\n'
    assert scan_source(tmp_path, code) == []


def test_unparseable_file_is_reported_not_crashed(tmp_path):
    findings = scan_source(tmp_path, "def broken(:\n")
    assert rule_ids(findings) == ["SEC-SYNTAX-001"]


# --- BIN-01..03: ELF / PE header parsing -----------------------------------

PT_LOAD, PT_DYNAMIC, PT_GNU_RELRO, PT_GNU_STACK = 1, 2, 0x6474E552, 0x6474E551
DT_NULL, DT_FLAGS, DT_BIND_NOW = 0, 30, 24


def build_elf(
    *,
    is64=True,
    endian="<",
    pie=True,
    stack_flags=6,  # 6 = RW, 7 = RWX, None = no PT_GNU_STACK segment
    relro=True,
    bind_now=True,
    canary=True,
):
    """Assemble a minimal ELF image with the requested mitigations."""
    segments = [(PT_LOAD, 5)]
    if stack_flags is not None:
        segments.append((PT_GNU_STACK, stack_flags))
    if relro:
        segments.append((PT_GNU_RELRO, 4))
    segments.append((PT_DYNAMIC, 6))

    ehsize, phentsize = (64, 56) if is64 else (52, 32)
    dyn_fmt = endian + ("qQ" if is64 else "iI")
    dynamic = struct.pack(dyn_fmt, DT_FLAGS, 0x8) if bind_now else struct.pack(dyn_fmt, 21, 0)  # DT_DEBUG
    dynamic += struct.pack(dyn_fmt, DT_NULL, 0)
    dyn_offset = ehsize + phentsize * len(segments)

    ident = b"\x7fELF" + bytes([2 if is64 else 1, 1 if endian == "<" else 2, 1]) + b"\x00" * 9
    e_type = 3 if pie else 2
    if is64:
        header = ident + struct.pack(endian + "HHIQQQIHHHHHH", e_type, 62, 1, 0, ehsize, 0, 0, ehsize, phentsize,
                                     len(segments), 0, 0, 0)
    else:
        header = ident + struct.pack(endian + "HHIIIIIHHHHHH", e_type, 3, 1, 0, ehsize, 0, 0, ehsize, phentsize,
                                     len(segments), 0, 0, 0)

    phdrs = b""
    for p_type, p_flags in segments:
        filesz = len(dynamic) if p_type == PT_DYNAMIC else 0
        offset = dyn_offset if p_type == PT_DYNAMIC else 0
        if is64:
            phdrs += struct.pack(endian + "IIQQQQQQ", p_type, p_flags, offset, 0, 0, filesz, filesz, 8)
        else:
            phdrs += struct.pack(endian + "IIIIIIII", p_type, offset, 0, 0, filesz, filesz, p_flags, 8)

    image = header + phdrs + dynamic
    if canary:
        image += b"\x00__stack_chk_fail\x00"
    return image


def build_pe(*, dll_chars, cookie=False, pe32_plus=True):
    dos = bytearray(64)
    dos[0:2] = b"MZ"
    struct.pack_into("<I", dos, 0x3C, 64)
    coff = b"PE\x00\x00" + struct.pack("<HHIIIHH", 0x8664, 0, 0, 0, 0, 240 if pe32_plus else 224, 0x22)
    optional = bytearray(240 if pe32_plus else 224)
    struct.pack_into("<H", optional, 0, 0x20B if pe32_plus else 0x10B)
    struct.pack_into("<H", optional, 70, dll_chars)
    image = bytes(dos) + coff + bytes(optional)
    if cookie:
        image += b"\x00__security_check_cookie\x00"
    return image


def audit_bytes(tmp_path, blob):
    path = tmp_path / "target.bin"
    path.write_bytes(blob)
    return audit_binary_headers(str(path))


@pytest.mark.parametrize("is64,endian", [(True, "<"), (False, "<"), (True, ">"), (False, ">")])
def test_fully_hardened_elf_passes_every_check(tmp_path, is64, endian):
    r = audit_bytes(tmp_path, build_elf(is64=is64, endian=endian))
    assert r.format == "ELF"
    assert (r.nx_enabled, r.pie_aslr_enabled, r.canary_detected, r.relro_detected) == (True, True, True, True)
    assert r.remediation_notes == []


def test_executable_stack_fails_nx(tmp_path):
    r = audit_bytes(tmp_path, build_elf(stack_flags=7))
    assert r.nx_enabled is False
    assert any("noexecstack" in n for n in r.remediation_notes)


def test_missing_gnu_stack_segment_fails_nx(tmp_path):
    assert audit_bytes(tmp_path, build_elf(stack_flags=None)).nx_enabled is False


def test_non_pie_executable_fails_aslr(tmp_path):
    r = audit_bytes(tmp_path, build_elf(pie=False))
    assert r.pie_aslr_enabled is False
    assert any("-fPIE" in n for n in r.remediation_notes)


def test_missing_canary_symbol_is_detected(tmp_path):
    r = audit_bytes(tmp_path, build_elf(canary=False))
    assert r.canary_detected is False
    assert any("stack-protector" in n for n in r.remediation_notes)


def test_canary_symbol_beyond_first_4k_is_still_found(tmp_path):
    blob = build_elf(canary=False) + b"\x00" * 8192 + b"\x00__stack_chk_fail\x00"
    assert audit_bytes(tmp_path, blob).canary_detected is True


def test_relro_segment_without_bind_now_is_partial_not_full(tmp_path):
    r = audit_bytes(tmp_path, build_elf(relro=True, bind_now=False))
    assert r.relro_detected is False


def test_bind_now_without_relro_segment_is_not_full_relro(tmp_path):
    assert audit_bytes(tmp_path, build_elf(relro=False, bind_now=True)).relro_detected is False


def test_marker_strings_in_data_do_not_fake_mitigations(tmp_path):
    """The old substring check treated the text 'GNU_STACK' as proof of NX."""
    blob = build_elf(stack_flags=7, relro=False, canary=False) + b"GNU_STACK GNU_RELRO"
    r = audit_bytes(tmp_path, blob)
    assert r.nx_enabled is False and r.relro_detected is False


def test_truncated_elf_is_reported_not_crashed(tmp_path):
    r = audit_bytes(tmp_path, build_elf()[:60])
    assert r.nx_enabled is False and r.remediation_notes


def test_hardened_pe_passes(tmp_path):
    r = audit_bytes(tmp_path, build_pe(dll_chars=0x0040 | 0x0100 | 0x4000, cookie=True))
    assert r.format == "PE"
    assert (r.nx_enabled, r.pie_aslr_enabled, r.canary_detected, r.relro_detected) == (True, True, True, True)


def test_unhardened_pe_fails_every_check(tmp_path):
    r = audit_bytes(tmp_path, build_pe(dll_chars=0))
    assert (r.nx_enabled, r.pie_aslr_enabled, r.canary_detected, r.relro_detected) == (False,) * 4
    assert len(r.remediation_notes) == 4


@pytest.mark.parametrize("flag,field", [(0x0100, "nx_enabled"), (0x0040, "pie_aslr_enabled"), (0x4000, "relro_detected")])
def test_each_pe_flag_controls_exactly_its_own_check(tmp_path, flag, field):
    r = audit_bytes(tmp_path, build_pe(dll_chars=flag))
    assert getattr(r, field) is True
    assert sum([r.nx_enabled, r.pie_aslr_enabled, r.relro_detected]) == 1


def test_unknown_and_missing_files_are_reported(tmp_path):
    assert audit_bytes(tmp_path, b"not an executable").format == "RAW/OTHER"
    assert audit_binary_headers(str(tmp_path / "absent")).format == "UNKNOWN"


def test_checksec_cli_reports_failures(tmp_path):
    path = tmp_path / "weak.elf"
    path.write_bytes(build_elf(stack_flags=7, pie=False, canary=False, relro=False))
    out = run_cli("checksec", "--binary", str(path)).stdout
    assert out.count("[FAIL]") == 4 and "[PASS]" not in out


# --- OPS-01: SARIF 2.1.0 ----------------------------------------------------

def _sarif_for(tmp_path, code):
    return json.loads(generate_sarif(scan_source(tmp_path, code)))


def test_sarif_document_has_required_2_1_0_structure(tmp_path):
    doc = _sarif_for(tmp_path, "eval(x)\nimport subprocess\nsubprocess.run(c, shell=True)\n")
    assert doc["version"] == "2.1.0"
    assert doc["$schema"].endswith("sarif-schema-2.1.0.json")
    run = doc["runs"][0]
    assert run["tool"]["driver"]["name"]
    assert len(run["results"]) == 2
    declared = {r["id"] for r in run["tool"]["driver"]["rules"]}
    for result in run["results"]:
        assert result["ruleId"] in declared
        assert result["level"] == "error"
        assert result["message"]["text"]
        loc = result["locations"][0]["physicalLocation"]
        assert loc["region"]["startLine"] >= 1 and loc["region"]["startColumn"] >= 1
        assert "\\" not in loc["artifactLocation"]["uri"]


def test_sarif_for_clean_code_has_empty_results(tmp_path):
    doc = _sarif_for(tmp_path, "x = 1\n")
    assert doc["runs"][0]["results"] == []


def test_sarif_cli_writes_file(tmp_path):
    src = tmp_path / "bad.py"
    src.write_text("eval(x)\n", encoding="utf-8")
    out = tmp_path / "report.sarif"
    run_cli("scan", "--path", str(src), "--format", "sarif", "--out", str(out))
    assert json.loads(out.read_text(encoding="utf-8"))["runs"][0]["results"][0]["ruleId"] == "SEC-AST-001"


# --- OPS-03: CI gating ------------------------------------------------------

def test_cli_exits_nonzero_on_high_finding(tmp_path):
    src = tmp_path / "bad.py"
    src.write_text("eval(x)\n", encoding="utf-8")
    assert run_cli("scan", "--path", str(src)).returncode == 1


def test_cli_exits_zero_on_clean_code(tmp_path):
    src = tmp_path / "ok.py"
    src.write_text("x = 1\n", encoding="utf-8")
    assert run_cli("scan", "--path", str(src)).returncode == 0


def test_cli_scans_directories_recursively(tmp_path):
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "deep.py").write_text("exec(x)\n", encoding="utf-8")
    assert run_cli("scan", "--path", str(tmp_path)).returncode == 1


def test_syntax_error_alone_does_not_fail_the_gate(tmp_path):
    src = tmp_path / "broken.py"
    src.write_text("def broken(:\n", encoding="utf-8")
    assert run_cli("scan", "--path", str(src)).returncode == 0


def test_audit_entry_point_reports_real_findings(tmp_path):
    src = tmp_path / "bad.py"
    src.write_text("eval(x)\n", encoding="utf-8")
    r = subprocess.run([sys.executable, os.path.join(STARTER, "audit.py"), str(src)],
                       capture_output=True, text=True, cwd=STARTER)
    assert r.returncode == 1 and "1 finding" in r.stdout


def test_health_command():
    r = run_cli("health")
    assert r.returncode == 0 and json.loads(r.stdout)["status"] == "ok"


# --- OPS-02: container ------------------------------------------------------

def test_dockerfile_is_rootless():
    with open(os.path.join(STARTER, "Dockerfile"), encoding="utf-8") as handle:
        users = re.findall(r"^USER\s+(\S+)", handle.read(), re.M)
    assert users and users[-1].split(":")[0] == "10001"
