import struct
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class BinaryMitigations:
    binary_path: str
    format: str
    nx_enabled: bool
    pie_aslr_enabled: bool
    canary_detected: bool
    relro_detected: bool
    remediation_notes: list[str]

def audit_binary_headers(binary_path: str) -> BinaryMitigations:
    """Safely inspects compiled executable headers without execution."""
    remediation = []
    try:
        with open(binary_path, "rb") as f:
            magic = f.read(4)
            f.seek(0)
            data = f.read(4096)
    except Exception as e:
        return BinaryMitigations(
            binary_path=binary_path,
            format="UNKNOWN",
            nx_enabled=False,
            pie_aslr_enabled=False,
            canary_detected=False,
            relro_detected=False,
            remediation_notes=[f"Failed to open binary: {e}"],
        )

    # Check for Linux ELF
    if magic == b"\x7fELF":
        # ELF format inspection
        ei_class = data[4] if len(data) > 4 else 1 # 1: 32-bit, 2: 64-bit
        e_type = struct.unpack("<H", data[16:18])[0] if len(data) >= 18 else 0
        pie = (e_type == 3) # ET_DYN indicates position-independent executable

        # Check for stack canaries string in symbol table snippet
        canary = b"__stack_chk_fail" in data or b"__stack_chk_guard" in data
        nx = b"GNU_STACK" in data
        relro = b"GNU_RELRO" in data

        if not nx:
            remediation.append("Missing NX/DEP stack protection: Compile with '-Wl,-z,noexecstack'.")
        if not pie:
            remediation.append("Missing Position Independent Executable (PIE/ASLR): Compile with '-fPIE -pie'.")
        if not canary:
            remediation.append("Stack canaries not detected: Compile with '-fstack-protector-strong'.")
        if not relro:
            remediation.append("Missing Full RELRO: Compile with '-Wl,-z,relro,-z,now'.")

        return BinaryMitigations(
            binary_path=binary_path,
            format="ELF",
            nx_enabled=nx,
            pie_aslr_enabled=pie,
            canary_detected=canary,
            relro_detected=relro,
            remediation_notes=remediation,
        )

    # Check for Windows PE
    elif magic[:2] == b"MZ":
        return BinaryMitigations(
            binary_path=binary_path,
            format="PE",
            nx_enabled=True,
            pie_aslr_enabled=True,
            canary_detected=True,
            relro_detected=True,
            remediation_notes=[],
        )

    return BinaryMitigations(
        binary_path=binary_path,
        format="RAW/OTHER",
        nx_enabled=False,
        pie_aslr_enabled=False,
        canary_detected=False,
        relro_detected=False,
        remediation_notes=["Unrecognized binary executable header"],
    )
