---
name: ssrf-defense-patterns
description: Safeguards against Server-Side Request Forgery and cloud metadata exfiltration.
---

# SSRF Defense Patterns Skill

## Overview
Server-Side Request Forgery (SSRF) occurs when an endpoint accepts a remote URL and fetches it without verifying the resolved destination IP address.

## Defense Checklist
1. Parse URL using `urllib.parse` and restrict scheme to `http` or `https`.
2. Resolve DNS hostname to IPv4/IPv6 address.
3. Check resolved IP against `ipaddress.ip_network`:
   - Reject private networks (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`).
   - Reject loopback (`127.0.0.0/8`, `::1`).
   - Reject cloud metadata (`169.254.169.254`).
