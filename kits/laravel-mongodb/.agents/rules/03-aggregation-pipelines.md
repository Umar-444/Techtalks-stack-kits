# 03 Aggregation Pipelines

# Rule 3: Aggregation Pipelines & Query Performance

## Context & Principles
- Leverage MongoDB's Aggregation Pipeline framework (`$match`, `$group`, `$project`, `$unwind`, `$sort`) for analytics, reporting, and complex data transformations.
- Eliminate full collection scans (`COLLSCAN`) by enforcing index coverage.

## Standards
1. **Pipeline Ordering**: Always place `$match` and `$sort` stages as early in the pipeline as possible to utilize collection indexes.
2. **Compound Indexes**: Define compound indexes in migrations or collection setup scripts for frequently combined query attributes:
   ```php
   $collection->index(['user_id' => 1, 'status' => 1, 'created_at' => -1]);
   ```
3. **Projection Limiting**: Always project only required fields (`$project`) to minimize memory usage and network payload transfer.
4. **Pipeline Builder**: Use Eloquent's `raw(function($collection) { ... })` or native aggregation pipeline helpers to construct type-safe pipelines.

