---
name: mysql-fulltext-search
description: Configuring and querying MySQL full-text indexes with Boolean and Natural Language modes in Eloquent.
---

# MySQL Full-Text Search Skill

## Directives
1. **Migration Index**:
   ```php
   $table->fullText(['title', 'content'], 'idx_articles_fulltext');
   ```
2. **Boolean Mode Querying**:
   ```php
   $results = Article::whereRaw(
       'MATCH(title, content) AGAINST(? IN BOOLEAN MODE)',
       ['+laravel +mysql -deprecated']
   )->get();
   ```
3. **Relevance Scoring**:
   ```php
   Article::selectRaw('*, MATCH(title, content) AGAINST(?) AS score', [$term])
       ->whereRaw('MATCH(title, content) AGAINST(?)', [$term])
       ->orderByDesc('score')
       ->paginate(20);
   ```
