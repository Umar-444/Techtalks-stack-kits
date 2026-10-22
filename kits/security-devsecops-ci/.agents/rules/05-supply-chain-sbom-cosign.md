# Supply Chain Security, SBOM Generation, and Cosign Verification

# Supply Chain Security, SBOM Generation, and Cosign Verification

## 1. Software Bill of Materials (SBOM) Generation
- Automatically generate machine-readable SBOMs for every production release using Anchore Syft:
  ```bash
  syft packages dir:. -o cyclonedx-json=cyclonedx.json -o spdx-json=spdx.json
  ```
- Archive SBOM artifacts alongside container images for regulatory and audit compliance.

## 2. Container Signing with Sigstore Cosign
- Sign container images in GitHub Actions using keyless OIDC identity:
  ```bash
  cosign sign --yes "${IMAGE_NAME}@${IMAGE_DIGEST}"
  ```
- Enforce signature verification before deploying images to Kubernetes or production runtimes.

## 3. Automated Dependency Updates
- Maintain `.github/dependabot.yml` configured for weekly security version bump PRs with automated testing.
