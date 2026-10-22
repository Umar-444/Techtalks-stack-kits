---
name: binary-mitigation-auditing
description: Verify compiled Linux ELF and Windows PE binary hardening protections (NX, ASLR, Canaries, RELRO).
---

# Binary Hardening and Mitigation Auditing

## Exploit Mitigations Checklist
When auditing compiled native applications (C, C++, Rust, Go), verify that essential compiler defenses are active:

| Protection | Purpose | Remediation Flag |
|:---|:---|:---|
| **NX / DEP** | Prevents execution of shellcode on stack/heap | GCC/Clang: `-Wl,-z,noexecstack` |
| **PIE / ASLR** | Randomizes code memory addresses on launch | GCC/Clang: `-fPIE -pie` |
| **Stack Canary** | Detects stack buffer overflows before return | GCC/Clang: `-fstack-protector-strong` |
| **Full RELRO** | Makes Global Offset Table (GOT) read-only | GCC/Clang: `-Wl,-z,relro,-z,now` |
| **FORTIFY** | Replaces unsafe libc functions with bounded versions | GCC/Clang: `-D_FORTIFY_SOURCE=2 -O2` |

## Inspection Workflow
Execute the binary checker tool:
```bash
python cli.py checksec --binary /path/to/executable
```
