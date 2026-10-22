---
name: prisma-multi-tenant-isolation
description: Implement multi-tenant data isolation and role-based access checks using Prisma Client extensions.
---

# Skill: Prisma Multi-Tenant Isolation

## Workflow
1. Enforce `tenantId` in model schema.
2. Inject tenant filter in all query operations.
3. Verify that querying non-owned records returns null.

## Done Means
- Cross-tenant data leaks impossible.
