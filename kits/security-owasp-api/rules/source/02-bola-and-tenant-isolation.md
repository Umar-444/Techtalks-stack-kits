---
id: 02-bola-and-tenant-isolation
title: BOLA Prevention, Object Ownership, and Tenant Isolation
globs: "starter/**/*.py,tests/**/*.py"
alwaysApply: true
---

# BOLA Prevention, Object Ownership, and Tenant Isolation

## 1. Mandatory Object Ownership Verification
- Every resourceful query retrieving an object by an ID from a URL path (`/api/v1/documents/{document_id}`) must verify tenant ownership:
  ```python
  document = db.get_document(document_id)
  if not document:
      raise HTTPException(status_code=404, detail="Document not found")
  if document.owner_id != current_user.user_id and current_user.role != "admin":
      raise HTTPException(status_code=403, detail="BOLA protection: Forbidden access to requested resource")
  ```

## 2. Opaque & Non-Sequential Identifiers
- Prohibit sequential auto-incrementing integers (`/users/1`, `/users/2`) as public identifiers.
- Use UUIDv4 or KSUID (`doc_01H1V83...`) to eliminate enumeration attacks.

## 3. Composite Scoped Queries
- Prefer querying database tables using compound conditions:
  `SELECT * FROM documents WHERE id = :doc_id AND owner_id = :current_user_id`
  This guarantees that even with a guessed ID, cross-tenant records cannot be selected.
