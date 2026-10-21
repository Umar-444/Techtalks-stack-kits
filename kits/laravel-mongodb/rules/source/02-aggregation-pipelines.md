---
title: "Aggregation Pipelines"
description: "Safe construction of aggregation queries in Laravel."
globs: ["app/Services/**/*.php", "app/Repositories/**/*.php"]
---

# Aggregation Pipelines

1. **Pipeline Syntax:**
   - Use `$collection->raw()->aggregate([ ... ])` or Eloquent aggregation helpers.
   - Always place `$match` filters as early as possible in the pipeline.

2. **Index Optimization:**
   - Ensure fields referenced in `$match` and `$sort` stages have corresponding compound indices.
