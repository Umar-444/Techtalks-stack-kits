---
name: turbo-streams-broadcast
description: Real-time DOM mutations and WebSockets broadcasting via Turbo Streams and Solid Cable.
---

# Turbo Streams Broadcast Skill

## Overview
Configure and broadcast live DOM updates over WebSockets using Rails 8 Solid Cable without requiring Redis.

## Core Directives

### 1. Solid Cable Setup
Ensure `config/cable.yml` uses the Solid Cable adapter:
```yaml
production:
  adapter: solid_cable
  connects_to:
    writing: primary
```

### 2. Granular Stream Actions
Turbo Streams supports 7 native DOM mutation actions:
1. `append`: Appends content to the target element.
2. `prepend`: Inserts content at the beginning of the target element.
3. `replace`: Swaps the entire target element with the replacement template.
4. `update`: Replaces the inner HTML of the target element.
5. `remove`: Removes the target element from the DOM.
6. `before`: Inserts content immediately before the target element.
7. `after`: Inserts content immediately after the target element.

### 3. Morphing Page Refreshes
For complex layouts, trigger a morphing refresh rather than manual stream segments:
```ruby
class Post < ApplicationRecord
  broadcasts_refreshes
end
```
