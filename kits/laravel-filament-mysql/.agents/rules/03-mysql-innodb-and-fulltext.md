# MySQL 8.4 InnoDB and Full-Text Optimization

# MySQL 8.4 InnoDB and Full-Text Optimization

## 1. Storage Engine & Collation
- All tables must use `ENGINE=InnoDB` with `utf8mb4_0900_ai_ci` collation.
- Use `bigIncrements('id')` or ULID/UUID primary keys.

## 2. Native Full-Text Search
- Define composite full-text indexes in migrations:
  ```php
  $table->fullText(['name', 'email', 'company_name'], 'customers_fulltext_idx');
  ```
- Query using MATCH AGAINST in Boolean Mode via parameterized bindings:
  ```php
  $query->whereRaw('MATCH(name, email, company_name) AGAINST(? IN BOOLEAN MODE)', [$searchTerm]);
  ```

## 3. Deadlock Handling
- Always catch `\Illuminate\Database\QueryException` with error code 1213 (Deadlock found).
- Wrap concurrent operations in `DB::transaction(fn() => ..., 3)`.
