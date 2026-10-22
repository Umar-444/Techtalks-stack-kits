---
name: trivy-container-scanning
description: Vulnerability scanning for container images, filesystems, and Git repositories with Aqua Security Trivy.
---

# Trivy Container Scanning Skill

## Overview
Audit container images and software dependencies for known CVEs, misconfigurations, and license compliance.

## Operational Commands

### 1. Filesystem Vulnerability Scan
```bash
trivy fs --severity HIGH,CRITICAL --ignore-unfixed --format table .
```

### 2. Container Image Scan with SARIF Output
```bash
trivy image --severity HIGH,CRITICAL --format sarif --output trivy-results.sarif my-image:latest
```

### 3. Handling False Positives with `.trivyignore`
Add specific CVE IDs with documented justifications:
```text
# .trivyignore
CVE-2024-99999 # Justification: Kernel vulnerability not applicable in rootless container
```
