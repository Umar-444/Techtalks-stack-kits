---
name: eloquent-index-optimization
description: Compound index optimization, query execution plan analysis with EXPLAIN, and cursor pagination.
---

# Eloquent Index Optimization Skill

## Guidelines
1. **Index Column Ordering**:
   Equality columns first (`status = 'published'`), sort/range columns last (`created_at DESC`).
2. **Cursor Pagination for Large Datasets**:
   Use `Article::orderBy('id')->cursorPaginate(25);` to avoid memory-heavy `OFFSET` queries.
3. **Inspect Execution Plans**:
   `DB::table('articles')->where('status', 'published')->explain();`
   Verify `type` is `ref` or `range`, never `ALL`.
