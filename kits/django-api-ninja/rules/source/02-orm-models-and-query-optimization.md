---
id: "02-orm-models-and-query-optimization"
title: "Django ORM Invariants & Query Optimization"
description: "Database standards for PostgreSQL models, N+1 query prevention with select_related/prefetch_related, explicit indexing, and tenant isolation."
globs: ["**/models.py", "**/migrations/*.py"]
alwaysApply: true
---

# 02 - Django ORM Invariants & Query Optimization

## 1. N+1 Query Elimination Invariants
- **Foreign Key Traversal:** Never access foreign key attributes inside loops or serializers without `select_related()`:
  ```python
  # CORRECT: Single SQL JOIN
  projects = Project.objects.select_related("organization", "owner").filter(is_active=True)
  ```
- **Many-to-Many & Reverse Relations:** Always use `prefetch_related()` for many-to-many sets or reverse foreign keys:
  ```python
  # CORRECT: Batch prefetch query
  projects = Project.objects.prefetch_related("tags", "collaborators").filter(is_active=True)
  ```

## 2. Explicit Database Indexing
- Define explicit composite or single-column indexes using `models.Index` inside model `Meta`:
  ```python
  class Project(models.Model):
      name = models.CharField(max_length=200, db_index=True)
      slug = models.SlugField(max_length=200, unique=True)
      tenant_id = models.CharField(max_length=64, db_index=True)
      is_active = models.BooleanField(default=True)
      created_at = models.DateTimeField(auto_now_add=True)

      class Meta:
          indexes = [
              models.Index(fields=["tenant_id", "is_active", "-created_at"]),
          ]
  ```

## 3. Multi-Tenant Query Scoping & BOLA Defense
- Every query accessing customer data must be explicitly scoped by the authenticated user's `tenant_id` or `owner`:
  ```python
  @router.get("/{project_id}", response=ProjectOut)
  def get_project(request, project_id: int):
      try:
          return Project.objects.get(id=project_id, tenant_id=request.auth.tenant_id)
      except Project.DoesNotExist:
          raise HttpError(404, "Project not found")
  ```
- Never execute naked `Project.objects.get(id=project_id)` lookups without tenant constraints.

## 4. Reversible, Backward-Compatible Migrations
- All Django migrations committed to source control must be fully reversible (`migrations.RunPython(forward_fn, reverse_fn)`).
- Never drop a column or rename a table in a single migration. Use a two-phase rollout to maintain backward compatibility during zero-downtime rolling deployments.
