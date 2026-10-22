# Testing Verification and CI Standards

# Testing Verification and CI Standards

## 1. Mocking AI Providers
- Never make outbound HTTP requests to paid APIs during automated tests.
- Use `MockAiProvider` returning deterministic responses for feature tests.

## 2. Pest Feature Assertions
- Assert that prompt injection attempts trigger `SecurityException`.
- Assert that cosine similarity correctly ranks relevant documents highest.

## 3. CI Pipeline
- Every commit must pass Pest test suite, Gitleaks, and Semgrep SAST scans.
