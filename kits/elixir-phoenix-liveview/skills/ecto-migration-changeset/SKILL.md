---
name: ecto-migration-changeset
description: Create Ecto schemas, validate incoming params with changesets, and generate reversible PostgreSQL migrations.
---

# Ecto Migration & Changeset Skill

## Purpose
Provides automated scaffolding and best practices for defining database schemas, constraints, and migrations in Elixir with Ecto 3.11+.

## Example Pattern
```elixir
defmodule Demo.Items.Item do
  use Ecto.Schema
  import Ecto.Changeset

  schema "items" do
    field :title, :string
    field :description, :string
    field :priority, :string, default: "medium"
    field :is_completed, :boolean, default: false

    timestamps(type: :utc_datetime)
  end

  def changeset(item, attrs) do
    item
    |> cast(attrs, [:title, :description, :priority, :is_completed])
    |> validate_required([:title])
    |> validate_length(:title, min: 3, max: 200)
    |> validate_inclusion(:priority, ["low", "medium", "high"])
  end
end
```
