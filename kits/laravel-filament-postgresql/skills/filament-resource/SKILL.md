---
name: "filament-resource"
description: "Scaffold and customize Filament administration resources, tables, and form schemas with strict authorization."
version: "1.0.0"
author: "TechTalks Stack Kits"
---

# Filament Resource Generator Skill

Use this skill whenever tasked with creating or updating an administrative resource in Filament 4/3.

## Workflow

1. **Verify Model & Policy Existence:**
   - Ensure the Eloquent model exists under `app/Models/` with the `HasUuids` trait.
   - Ensure a dedicated Policy exists under `app/Policies/` with all standard actions defined.

2. **Generate the Resource:**
   ```bash
   php artisan make:filament-resource {ModelName} --generate
   ```

3. **Form Schema Guidelines:**
   - Group fields into logical sections using `Filament\Forms\Components\Section`.
   - Apply explicit validation matching database schema constraints.
   - Use `TextInput::make('email')->email()->required()->unique(ignoreRecord: true)`.

4. **Table Column Standards:**
   - Primary identifier column must link to the view/edit page.
   - Enable sorting and searching explicitly on high-cardinality index columns.
   - Use badge columns (`TextColumn::make('status')->badge()`) with color mappings.

5. **Action Policies:**
   - Enforce that bulk delete actions require confirmation with an explanation of consequences.
