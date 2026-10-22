# 02 Document Modeling And Relations

# Rule 2: Document Modeling, Embedded Documents & Relationships

## Context & Principles
- Design documents around query and access patterns: prefer embedded documents (`embedsMany`, `embedsOne`) for data that is always read together.
- Use referenced relations (`belongsTo`, `hasMany`) only when documents grow unbounded or are queried independently across boundaries.

## Standards
1. **Embedded Documents**: Use `embedsMany` for arrays of related records (e.g., items within an order or tags on an article).
2. **Document Bounding**: Never allow unbounded arrays inside a single document to prevent exceeding MongoDB's 16MB document limit.
3. **Cascading Operations**: Use MongoDB atomic array update operators (`$push`, `$pull`, `$set`) rather than rewriting full document arrays.
4. **Data Integrity**: Validate embedded data structure schemas before persisting to the collection.

