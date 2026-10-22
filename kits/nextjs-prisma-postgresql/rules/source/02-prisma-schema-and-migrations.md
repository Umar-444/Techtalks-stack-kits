---
id: 02-prisma-schema-and-migrations
title: Prisma Schema and Migration Standards
description: Declarative data modeling, relations, and migration hygiene.
globs: ["prisma/**/*.prisma"]
alwaysApply: true
---

# Prisma Schema and Migration Standards

## 1. Model Definitions & Relations
- Every model must define an `id` primary key (`@id @default(cuid())` or `@default(autoincrement())`).
- Include standard audit timestamps: `createdAt DateTime @default(now())` and `updatedAt DateTime @updatedAt`.
- Explicitly name foreign key relations and cascade delete rules where appropriate.

## 2. Index Optimization
- Add indexes on foreign keys, tenant IDs, and filtered query fields: `@@index([tenantId, status])`.
- Define composite unique constraints to enforce business invariants: `@@unique([tenantId, slug])`.

## 3. Migration Workflows
- Always generate migrations with descriptive names: `npx prisma migrate dev --name <description>`.
- In production, deploy migrations using `npx prisma migrate deploy`.
