# 03 Restful Resources And Query Builder

# Rule 03: Query Builder & Resource Formatting

- Use `Spatie\QueryBuilder\QueryBuilder` for collection endpoints.
- Always declare strict whitelists:
  ```php
  QueryBuilder::for(Project::class)
      ->allowedFilters(['title', 'status', AllowedFilter::exact('priority')])
      ->allowedSorts(['created_at', 'title'])
      ->allowedIncludes(['user'])
      ->paginate(request()->input('per_page', 20));
  ```
- Disallow arbitrary or unfiltered joins that could cause denial of service.
- Eloquent API Resources must explicitly map all exposed fields without `...$this->toArray()`.
