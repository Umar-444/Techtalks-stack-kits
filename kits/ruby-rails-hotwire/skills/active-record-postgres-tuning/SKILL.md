---
name: active-record-postgres-tuning
description: ActiveRecord optimization, compound indexing, strict loading, and N+1 query elimination.
---

# ActiveRecord PostgreSQL Tuning Skill

## Guidelines

### 1. Preventing N+1 Queries
Always eager load referenced associations:
```ruby
# Correct
@posts = Post.includes(:user, :tags).where(published: true).order(created_at: :desc)

# Enforcing in config/environments/development.rb:
config.active_record.strict_loading_by_default = true
```

### 2. Compound Index Strategies
When filtering and sorting across multiple columns:
```ruby
# db/migrate/20261022000002_add_compound_index_to_posts.rb
class AddCompoundIndexToPosts < ActiveRecord::Migration[8.0]
  def change
    add_index :posts, [:status, :created_at], algorithm: :concurrently
  end
end
```

### 3. Partial Indexes for Filtered Queries
```ruby
add_index :posts, :created_at, where: "published = true", name: "idx_posts_published_recent"
```
