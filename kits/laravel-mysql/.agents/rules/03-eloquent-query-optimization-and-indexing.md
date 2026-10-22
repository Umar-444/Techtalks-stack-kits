# Eloquent Query Tuning, MySQL Full-Text Search, and N+1 Prevention

# Eloquent Query Tuning, MySQL Full-Text Search, and N+1 Prevention

## 1. N+1 Query Elimination
- Prohibit accessing relationships within loops without eager loading.
- Always use `Article::with(['author', 'category'])->paginate(20)`.
- Enable strict loading in development to catch un-eager-loaded queries:
  `Model::preventLazyLoading(!app()->isProduction());`

## 2. MySQL Full-Text Search
- Define native MySQL full-text indexes in migrations:
  `$table->fullText(['title', 'content']);`
- Query using MySQL boolean or natural language mode:
  ```php
  Article::whereRaw('MATCH(title, content) AGAINST(? IN BOOLEAN MODE)', [$searchTerm])->get();
  ```

## 3. Compound Index Order Strategies
- Order compound index columns by: Equality filters first, Range/Inequality filters next, Sort columns last.
- Verify index usage using `DB::table(...)->explain()` to prevent full-table scans.
