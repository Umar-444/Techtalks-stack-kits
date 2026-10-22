---
name: bun-performance-tuning
description: Optimizing Bun runtime execution, WAL mode configuration, and zero-copy JSON streaming.
---

# Bun Performance Tuning Skill

## Guidelines
1. **Enable WAL Mode**:
   ```typescript
   db.exec("PRAGMA journal_mode = WAL;");
   db.exec("PRAGMA synchronous = NORMAL;");
   db.exec("PRAGMA cache_size = -64000;"); // 64MB cache
   ```
2. **Prepared Queries**:
   Prepare SQL statements at boot to avoid parse and compile overhead on hot HTTP paths.
3. **Cluster Scaling**:
   Run Bun with cluster mode or multiple worker threads for multi-core scaling.
