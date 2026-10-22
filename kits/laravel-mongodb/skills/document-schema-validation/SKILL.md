---
name: document-schema-validation
description: Enforce MongoDB collection JSON schema validation, compound indexes, and BSON ObjectId validation.
---

# Document Schema Validation Skill

## Purpose
Guarantees MongoDB collections enforce strict structural constraints and index coverage.

## Standards
- Validate all incoming document IDs against 24-char hex format.
- Create compound indexes on collection initialization:
  ```php
  $collection->createIndex(['user_id' => 1, 'category' => 1, 'created_at' => -1]);
  ```
- Reject any document containing unescaped `$` keys in user-supplied payloads.

## Done Means
Collection validates incoming BSON document structures, prevents NoSQL operator injection, and uses indexes for all reads.
