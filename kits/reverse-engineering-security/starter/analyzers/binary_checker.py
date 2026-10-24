"""Static exploit-mitigation inspection of ELF and PE executables.

Headers are parsed structurally with `struct`; the target is never executed.
"""

import struct
from dataclasses import dataclass


@dataclass
class BinaryMitigations:
    binary_path: str
    format: str
    nx_enabled: bool
    pie_aslr_enabled: bool
    canary_detected: bool
    relro_detected: bool
    remediation_notes: list[str]


# ELF constants
PT_LOAD, PT_DYNAMIC, PT_GNU_RELRO, PT_GNU_STACK = 1, 2, 0x6474E552, 0x6474E551
PF_X = 1
ET_DYN = 3
DT_NULL, DT_FLAGS, DT_FLAGS_1 = 0, 30, 0x6FFFFFFB
DF_BIND_NOW, DF_1_NOW = 0x8, 0x1
DT_BIND_NOW = 24
CANARY_SYMBOLS = (b"__stack_chk_fail", b"__stack_chk_guard")

# PE constants
IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE = 0x0040
IMAGE_DLLCHARACTERISTICS_NX_COMPAT = 0x0100
IMAGE_DLLCHARACTERISTICS_GUARD_CF = 0x4000
PE_COOKIE_SYMBOLS = (b"__security_check_cookie", b"__security_init_cookie")


def _unknown(path: str, fmt: str, note: str) -> BinaryMitigations:
    return BinaryMitigations(path, fmt, False, False, False, False, [note])


def _parse_elf(path: str, data: bytes) -> BinaryMitigations:
    if len(data) < 52:
        return _unknown(path, "ELF", "Truncated ELF header")
    is64 = data[4] == 2
    endian = "<" if data[5] == 1 else ">"
    if is64:
        if len(data) < 64:
            return _unknown(path, "ELF", "Truncated ELF64 header")
        e_type = struct.unpack_from(endian + "H", data, 16)[0]
        e_phoff = struct.unpack_from(endian + "Q", data, 32)[0]
        e_phentsize, e_phnum = struct.unpack_from(endian + "HH", data, 54)
    else:
        e_type = struct.unpack_from(endian + "H", data, 16)[0]
        e_phoff = struct.unpack_from(endian + "I", data, 28)[0]
        e_phentsize, e_phnum = struct.unpack_from(endian + "HH", data, 42)

    segments = []  # (p_type, p_flags, p_offset, p_filesz)
    for i in range(e_phnum):
        base = e_phoff + i * e_phentsize
        try:
            if is64:
                p_type, p_flags, p_offset = struct.unpack_from(endian + "IIQ", data, base)
                p_filesz = struct.unpack_from(endian + "Q", data, base + 32)[0]
            else:
                p_type, p_offset = struct.unpack_from(endian + "II", data, base)
                p_filesz, _memsz, p_flags = struct.unpack_from(endian + "III", data, base + 16)
        except struct.error:
            return _unknown(path, "ELF", "Program header table is truncated or corrupt")
        segments.append((p_type, p_flags, p_offset, p_filesz))

    # NX: a PT_GNU_STACK segment must exist and must not request execute.
    gnu_stack = next((s for s in segments if s[0] == PT_GNU_STACK), None)
    nx = gnu_stack is not None and not (gnu_stack[1] & PF_X)

    pie = e_type == ET_DYN

    # Full RELRO: PT_GNU_RELRO present AND immediate binding requested.
    has_relro_segment = any(s[0] == PT_GNU_RELRO for s in segments)
    bind_now = False
    dyn = next((s for s in segments if s[0] == PT_DYNAMIC), None)
    if dyn is not None:
        entry = 16 if is64 else 8
        fmt = endian + ("qQ" if is64 else "iI")
        offset, end = dyn[2], min(dyn[2] + dyn[3], len(data))
        while offset + entry <= end:
            tag, val = struct.unpack_from(fmt, data, offset)
            if tag == DT_NULL:
                break
            if tag == DT_BIND_NOW or (tag == DT_FLAGS and val & DF_BIND_NOW) or (
                tag == DT_FLAGS_1 and val & DF_1_NOW
            ):
                bind_now = True
            offset += entry
    relro = has_relro_segment and bind_now

    # Canary: the symbol name lives in .dynstr/.strtab, anywhere in the file.
    canary = any(sym in data for sym in CANARY_SYMBOLS)

    notes = []
    if not nx:
        notes.append("Missing NX/DEP stack protection: Compile with '-Wl,-z,noexecstack'.")
    if not pie:
        notes.append("Missing Position Independent Executable (PIE/ASLR): Compile with '-fPIE -pie'.")
    if not canary:
        notes.append("Stack canaries not detected: Compile with '-fstack-protector-strong'.")
    if not relro:
        notes.append("Missing Full RELRO: Compile with '-Wl,-z,relro,-z,now'.")
    return BinaryMitigations(path, "ELF", nx, pie, canary, relro, notes)


def _parse_pe(path: str, data: bytes) -> BinaryMitigations:
    if len(data) < 0x40:
        return _unknown(path, "PE", "Truncated DOS header")
    e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
    if data[e_lfanew:e_lfanew + 4] != b"PE\x00\x00" or len(data) < e_lfanew + 24 + 72:
        return _unknown(path, "PE", "Missing or truncated PE signature")
    opt = e_lfanew + 24  # optional header
    # DllCharacteristics sits at offset 70 in both PE32 and PE32+ optional headers.
    dll_chars = struct.unpack_from("<H", data, opt + 70)[0]

    aslr = bool(dll_chars & IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE)
    nx = bool(dll_chars & IMAGE_DLLCHARACTERISTICS_NX_COMPAT)
    cfg = bool(dll_chars & IMAGE_DLLCHARACTERISTICS_GUARD_CF)
    cookie = any(sym in data for sym in PE_COOKIE_SYMBOLS)

    notes = []
    if not nx:
        notes.append("Missing DEP (NX_COMPAT): Link with '/NXCOMPAT'.")
    if not aslr:
        notes.append("Missing ASLR (DYNAMIC_BASE): Link with '/DYNAMICBASE'.")
    if not cookie:
        notes.append("Stack cookie (/GS) not detected: Compile with '/GS'.")
    if not cfg:
        notes.append("Missing Control Flow Guard: Compile with '/guard:cf' and link with '/guard:cf'.")
    # RELRO is an ELF concept; for PE the slot reports Control Flow Guard instead.
    return BinaryMitigations(path, "PE", nx, aslr, cookie, cfg, notes)


def audit_binary_headers(binary_path: str) -> BinaryMitigations:
    """Safely inspects compiled executable headers without execution."""
    try:
        with open(binary_path, "rb") as handle:
            data = handle.read()
    except Exception as exc:
        return _unknown(binary_path, "UNKNOWN", f"Failed to open binary: {exc}")

    if data[:4] == b"\x7fELF":
        return _parse_elf(binary_path, data)
    if data[:2] == b"MZ":
        return _parse_pe(binary_path, data)
    return _unknown(binary_path, "RAW/OTHER", "Unrecognized binary executable header")
