---
name: "rag-local-private-core"
description: "Core operational workflows, zero-egress network firewall assertion, health checking, and offline mock fallback for Local Private RAG."
---

# Skill: Local Private RAG Core Operations

Use this skill for day-to-day operations, airgap verification, health checks, and CI/CD test automation.

## 1. Zero-Egress Network Assertion
Verify that the service is running in airgapped mode and has blocked all third-party external host resolution:
```bash
# Check application status
curl -s http://localhost:8000/healthz | jq '{airgap_safe, cloud_egress_blocked, model}'
```

To test airgap network isolation at the Docker container level:
```bash
# Verify internal container has no default route to external WAN
docker exec -it starter-rag-app-1 ping -c 1 -W 2 8.8.8.8 || echo "Zero-egress confirmed: external traffic dropped"
```

## 2. In-Memory CI/CD Fallback Mode
In automated test runners where Ollama daemon and GPU acceleration are unavailable, set:
```bash
export TEST_MODE=true
pytest starter/tests/test_rag.py -v
```
When `TEST_MODE=true`:
1. ChromaDB runs with ephemeral in-memory configuration.
2. Embedding generation uses deterministic normalized synthetic vectors.
3. Ollama queries are synthesized deterministically based on matched chunk text.
All assertion contracts and security scans pass without external network calls or GPU dependencies.

## 3. Health Probe & Monitoring Metrics
Query the internal monitoring metrics:
```bash
curl -s http://localhost:8000/api/v1/metrics
```
Output exposes:
- Active Chroma collection count and total vectors indexed.
- Local model inference latency (p50, p95).
- Airgap violation attempt counter (must remain strictly 0).
