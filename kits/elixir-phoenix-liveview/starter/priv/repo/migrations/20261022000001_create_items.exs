defmodule Demo.Repo.Migrations.CreateItems do
  use Ecto.Migration

  def change do
    create table(:items) do
      add :title, :string, null: false
      add :description, :text, default: ""
      add :priority, :string, default: "medium", null: false
      add :is_completed, :boolean, default: false, null: false

      timestamps(type: :utc_datetime)
    end

    create index(:items, [:inserted_at])
    create index(:items, [:is_completed])
  end
end
