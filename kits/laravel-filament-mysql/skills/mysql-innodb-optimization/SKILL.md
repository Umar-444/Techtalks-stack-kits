---
name: mysql-innodb-optimization
description: Tune MySQL 8.4 InnoDB buffer pools, full-text boolean search, generated column indexing, and transaction deadlock retries.
---

# Skill: MySQL InnoDB Optimization

## Workflow
1. Add full-text indexes in migrations using `$table->fullText([...])`.
2. Implement scope in model:
```php
public function scopeFullTextSearch(Builder $query, string $term): Builder
{
    return $query->whereRaw("MATCH(name, email, company_name) AGAINST(? IN BOOLEAN MODE)", [$term . '*']);
}
```
3. Use generated virtual columns for JSON key indexing.

## Done Means
- EXPLAIN query confirms `type: fulltext` index utilization.
