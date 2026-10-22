---
name: first-feature
description: Build the canonical first feature: a full CRUD task list module with Tailwind UI cards and atomic PostgreSQL persistence.
---

# First Feature Skill: Responsive CRUD Module

## Objective
Construct a responsive item management dashboard with creation form, priority filters, and status toggles.

## Implementation Steps
1. Define the PostgreSQL Item model in `app/models.py`.
2. Define the Tailwind-styled ModelForm in `app/forms.py`.
3. Implement `ListView`, `CreateView`, and `ItemToggleView` in `app/views.py`.
4. Render using Tailwind card grid layout in `templates/index.html`.

## Done Means
A user creates a new task in the browser form, receives instant visual feedback via flash message, and task persists across PostgreSQL restarts.
