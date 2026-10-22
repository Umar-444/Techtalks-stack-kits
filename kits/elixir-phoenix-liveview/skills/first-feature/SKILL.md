---
name: first-feature
description: Build the canonical first feature: real-time live synchronized stream list with PubSub broadcast.
---

# First Feature Skill: Real-time LiveView Stream with PubSub

## Objective
Construct a real-time reactive task stream where items created by one browser tab instantly appear across all connected browser tabs via Phoenix.PubSub.

## Implementation Steps
1. Define Ecto Schema and Changeset in `lib/demo/items/item.ex`.
2. Implement PubSub broadcast in Context `lib/demo/items.ex`.
3. Implement `Index` LiveView with `stream/3` and `handle_info/2` in `lib/demo_web/live/item_live/index.ex`.
4. Render HEEX declarative template in `lib/demo_web/live/item_live/index.html.heex`.

## Done Means
Submitting a task in Tab A immediately renders in Tab B via WebSocket push without reloading the page.
