---
name: bola-authorization-testing
description: Methodology for testing and preventing Broken Object Level Authorization (BOLA/IDOR).
---

# BOLA Authorization Testing Skill

## Overview
Broken Object Level Authorization (BOLA) occurs when an application does not validate whether the currently authenticated user owns or is authorized to manipulate a requested object.

## Testing Protocol
1. **User A**: Authenticate as `user_alice` and obtain token `TOKEN_A`.
2. **User B**: Authenticate as `user_bob` and create a resource (e.g. `doc_123`).
3. **Exploit Verification**: Attempt to fetch, modify, or delete `doc_123` using `TOKEN_A`.
4. **Assert Status**: Server MUST respond with HTTP 403 Forbidden or HTTP 404 Not Found.
