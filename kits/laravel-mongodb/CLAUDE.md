# Laravel 12 + MongoDB (NoSQL) — Claude Code Guidelines (CLAUDE.md)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Quick Reference & Non-Negotiable Standards
### MongoDB Eloquent Conventions
> Model inheritance, embedded documents, and collection naming.

# MongoDB Eloquent Conventions

1. **Model Inheritance:**
   - All MongoDB models must extend `MongoDB\Laravel\Eloquent\Model`.
   - Explicitly specify the collection name: `protected $collection = 'users';`.

2. **Embedded Relations:**
   - Use `embedsOne()` and `embedsMany()` for strictly co-located document data.
   - Define embedded models with strict attribute casting.

### Aggregation Pipelines
> Safe construction of aggregation queries in Laravel.

# Aggregation Pipelines

1. **Pipeline Syntax:**
   - Use `$collection->raw()->aggregate([ ... ])` or Eloquent aggregation helpers.
   - Always place `$match` filters as early as possible in the pipeline.

2. **Index Optimization:**
   - Ensure fields referenced in `$match` and `$sort` stages have corresponding compound indices.

### NoSQL Security & Injection Defense
> Preventing operator injection, $where execution, and unauthorized collection access.

# NoSQL Security & Injection Defense

1. **Operator Injection Defense:**
   - Never pass unfiltered `$request->all()` into `where()` clauses.
   - MongoDB interprets array inputs as operators (e.g. `['$gt' => '']`). Cast all inputs to scalar types.

2. **Prohibited Features:**
   - Usage of `$where` with JavaScript execution is strictly prohibited.

