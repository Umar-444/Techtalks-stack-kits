---
name: sqlx-compile-time-queries
description: Authoring compile-time verified queries, preparing offline query metadata, and tuning connection pools.
---

# SQLx Compile-Time Queries Skill

## Overview
SQLx verifies SQL queries at compile time against a live PostgreSQL instance or cached query metadata.

## Core Directives
1. **Prepare Offline Metadata**:
   ```bash
   cargo sqlx prepare -- --all-targets
   ```
   Commits query schemas to `.sqlx/` so CI pipelines can build without live database connections.
2. **Prepared Query Macros**:
   Use `query!` for raw tuples and `query_as!` for mapped structs.
