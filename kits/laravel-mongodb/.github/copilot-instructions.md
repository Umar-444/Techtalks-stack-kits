# GitHub Copilot Instructions for Laravel 12 + MongoDB (NoSQL)
# Auto-generated from rules/source/*.md by tools/transpiler.py. Do NOT edit directly.

## 01 Framework Conventions
# Rule 1: Laravel 12 + MongoDB Framework Conventions

## Context & Principles
- Utilize the official `mongodb/laravel-mongodb` package for seamless Eloquent integration with MongoDB 7+.
- All models interacting with MongoDB must extend `MongoDB\Laravel\Eloquent\Model` or `MongoDB\Laravel\Auth\User`.
- Enforce strict typing (`declare(strict_types=1);`) and treat MongoDB documents as schema-governed data structures rather than arbitrary key-value dictionaries.

## Standards
1. **Connection Config**: Set `DB_CONNECTION=mongodb` in `.env` and define the MongoDB driver in `config/database.php`.
2. **Collection Organization**: Explicitly declare `$collection` on every model to avoid naming ambiguity.
3. **Primary Key**: MongoDB uses `_id` (BSON ObjectId). Eloquent aliases `_id` to `$model->id`. Never override primary key semantics unless explicitly mapping external UUIDs.
4. **Dates & Timestamps**: Ensure all date fields cast to `datetime` or `MongoDB\BSON\UTCDateTime`.


## MongoDB Eloquent Conventions
# MongoDB Eloquent Conventions

1. **Model Inheritance:**
   - All MongoDB models must extend `MongoDB\Laravel\Eloquent\Model`.
   - Explicitly specify the collection name: `protected $collection = 'users';`.

2. **Embedded Relations:**
   - Use `embedsOne()` and `embedsMany()` for strictly co-located document data.
   - Define embedded models with strict attribute casting.

## Aggregation Pipelines
# Aggregation Pipelines

1. **Pipeline Syntax:**
   - Use `$collection->raw()->aggregate([ ... ])` or Eloquent aggregation helpers.
   - Always place `$match` filters as early as possible in the pipeline.

2. **Index Optimization:**
   - Ensure fields referenced in `$match` and `$sort` stages have corresponding compound indices.

## 02 Document Modeling And Relations
# Rule 2: Document Modeling, Embedded Documents & Relationships

## Context & Principles
- Design documents around query and access patterns: prefer embedded documents (`embedsMany`, `embedsOne`) for data that is always read together.
- Use referenced relations (`belongsTo`, `hasMany`) only when documents grow unbounded or are queried independently across boundaries.

## Standards
1. **Embedded Documents**: Use `embedsMany` for arrays of related records (e.g., items within an order or tags on an article).
2. **Document Bounding**: Never allow unbounded arrays inside a single document to prevent exceeding MongoDB's 16MB document limit.
3. **Cascading Operations**: Use MongoDB atomic array update operators (`$push`, `$pull`, `$set`) rather than rewriting full document arrays.
4. **Data Integrity**: Validate embedded data structure schemas before persisting to the collection.


## 03 Aggregation Pipelines
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


## NoSQL Security & Injection Defense
# NoSQL Security & Injection Defense

1. **Operator Injection Defense:**
   - Never pass unfiltered `$request->all()` into `where()` clauses.
   - MongoDB interprets array inputs as operators (e.g. `['$gt' => '']`). Cast all inputs to scalar types.

2. **Prohibited Features:**
   - Usage of `$where` with JavaScript execution is strictly prohibited.

## 04 Nosql Injection Security
# Rule 4: NoSQL Injection Defense & Authorization Policies

## Context & Principles
- Prevent NoSQL injection attacks resulting from unvalidated client input containing MongoDB query operator objects (e.g. `{"$gt": ""}`, `{"$where": "..."}`).
- Strictly validate and cast all client-supplied document identifiers.

## Standards
1. **Operator Stripping**: Sanitize all incoming request arrays to reject or escape keys starting with `$` or containing `.`.
2. **ObjectId Casting**: Always validate that string IDs match standard 24-character hexadecimal format (`/^[a-f\d]{24}$/i`) before querying:
   ```php
   if (!preg_match('/^[a-f0-9]{24}$/i', $id)) {
       abort(404);
   }
   ```
3. **Where Operator Prohibition**: Never use `$where` or arbitrary JavaScript execution in MongoDB queries.
4. **BOLA Document Policies**: Every document read or write must pass authorization gates verifying user ownership or role entitlements.


## 05 Testing And Verification
# Rule 5: Testing, Database Isolation & Transaction Verification

## Context & Principles
- All tests must run against an isolated MongoDB test database (e.g. `app_mongo_test`) with automatic collection dropping between test suites.
- Ensure test idempotency without cross-test state leakage.

## Standards
1. **Test Environment**: Set `DB_DATABASE=app_mongo_test` in `phpunit.xml`.
2. **Database Cleanliness**: Use database cleanup traits to truncate or drop test collections after each test run.
3. **Feature Test Coverage**: Verify CRUD operations, embedded relation mutations, and aggregation pipeline outputs.
4. **Policy Enforcement Testing**: Assert that non-owner users attempting cross-document mutations receive HTTP 403 Forbidden.


