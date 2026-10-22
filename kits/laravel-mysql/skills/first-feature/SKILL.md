---
name: first-feature
description: Guide for scaffolding a new resourceful feature with MySQL migrations, model, Form Request, Policy, and tests.
---

# First Feature Skill: Scaffolding a Full Resource with MySQL Fulltext

## Overview
Create an `articles` resource with full-text search, policy authorization, and validation.

## Implementation Guide

### 1. Migration with Fulltext Index
```php
Schema::create('articles', function (Blueprint $table) {
    $table->id();
    $table->foreignId('user_id')->constrained()->cascadeOnDelete();
    $table->string('title');
    $table->text('content');
    $table->string('status')->default('draft');
    $table->timestamps();

    $table->index(['status', 'created_at']);
    $table->fullText(['title', 'content']);
});
```

### 2. Model with Scopes
```php
class Article extends Model {
    protected $fillable = ['user_id', 'title', 'content', 'status'];

    public function scopeSearch($query, string $term) {
        return $query->whereRaw('MATCH(title, content) AGAINST(? IN BOOLEAN MODE)', [$term]);
    }
}
```

### 3. Form Request & Controller
Validate incoming payloads with `StoreArticleRequest` and authorize with `ArticlePolicy`.
