# 04 Software Supply Chain And Sbom Validation

# Software Supply Chain and SBOM Validation

1. **CycloneDX and SPDX Parsing**: Ingest and validate Software Bill of Materials (SBOM) documents in CycloneDX 1.5+ and SPDX 2.3+ JSON formats to maintain complete inventory of software dependencies.
2. **Cryptographic Hash Pinning**: Verify that all package dependencies declared in requirements, lockfiles, or SBOMs have associated SHA-256 integrity hashes to prevent dependency substitution and supply-chain tampering.
3. **Vulnerability Advisory Correlation**: Correlate package names and pinned versions against the OSV (Open Source Vulnerabilities) database and CVE feeds to detect known disclosed vulnerabilities.
4. **License Compliance Verification**: Inspect declared dependency licenses against organizational whitelist policies (e.g. MIT, Apache-2.0, BSD-3-Clause) and flag copyleft licenses (GPL, AGPL) that may pose compliance concerns.
5. **Zero Outdated Packages Policy**: Require automated checks for unmaintained or deprecated upstream packages, generating alerts for dependencies with unresolved security advisories.

