---
name: "spatie-query-builder"
description: "Patterns for advanced filtering, sorting, relation inclusion, and pagination using Spatie Query Builder."
version: "1.0.0"
---

# Spatie Query Builder Skill

## Controller Implementation Pattern
```php
use Spatie\QueryBuilder\QueryBuilder;
use Spatie\QueryBuilder\AllowedFilter;

$projects = QueryBuilder::for(Project::where('user_id', auth()->id()))
    ->allowedFilters([
        'title',
        'status',
        AllowedFilter::scope('search'),
    ])
    ->allowedSorts(['created_at', 'title', 'priority'])
    ->allowedIncludes(['tasks', 'user'])
    ->defaultSort('-created_at')
    ->paginate(request()->input('per_page', 15));

return ProjectResource::collection($projects);
```
