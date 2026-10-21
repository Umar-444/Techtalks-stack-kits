# Laravel 12 + MongoDB (NoSQL) — Agent Operating Rules (AGENTS.md)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## Table of Contents
- [MongoDB Eloquent Conventions](#01-mongodb-eloquent)
- [Aggregation Pipelines](#02-aggregation-pipelines)
- [NoSQL Security & Injection Defense](#03-nosql-security)

---

<a id="01-mongodb-eloquent"></a>
## MongoDB Eloquent Conventions

# MongoDB Eloquent Conventions

1. **Model Inheritance:**
   - All MongoDB models must extend `MongoDB\Laravel\Eloquent\Model`.
   - Explicitly specify the collection name: `protected $collection = 'users';`.

2. **Embedded Relations:**
   - Use `embedsOne()` and `embedsMany()` for strictly co-located document data.
   - Define embedded models with strict attribute casting.

---

<a id="02-aggregation-pipelines"></a>
## Aggregation Pipelines

# Aggregation Pipelines

1. **Pipeline Syntax:**
   - Use `$collection->raw()->aggregate([ ... ])` or Eloquent aggregation helpers.
   - Always place `$match` filters as early as possible in the pipeline.

2. **Index Optimization:**
   - Ensure fields referenced in `$match` and `$sort` stages have corresponding compound indices.

---

<a id="03-nosql-security"></a>
## NoSQL Security & Injection Defense

# NoSQL Security & Injection Defense

1. **Operator Injection Defense:**
   - Never pass unfiltered `$request->all()` into `where()` clauses.
   - MongoDB interprets array inputs as operators (e.g. `['$gt' => '']`). Cast all inputs to scalar types.

2. **Prohibited Features:**
   - Usage of `$where` with JavaScript execution is strictly prohibited.

---

