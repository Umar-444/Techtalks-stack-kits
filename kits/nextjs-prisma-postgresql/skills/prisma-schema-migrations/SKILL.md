---
name: prisma-schema-migrations
description: Author Prisma schemas, execute declarative migrations, and optimize connection pool parameters.
---

# Skill: Prisma Schema Migrations

## Workflow
1. Update `prisma/schema.prisma`.
2. Generate migration: `npx prisma migrate dev --name <feature>`.
3. Generate client: `npx prisma generate`.

## Done Means
- Clean migration history and synchronized TypeScript types.
