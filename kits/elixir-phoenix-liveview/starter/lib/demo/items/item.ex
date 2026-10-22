defmodule Demo.Items.Item do
  use Ecto.Schema
  import Ecto.Changeset

  schema "items" do
    field :title, :string
    field :description, :string, default: ""
    field :priority, :string, default: "medium"
    field :is_completed, :boolean, default: false

    timestamps(type: :utc_datetime)
  end

  @doc false
  def changeset(item, attrs) do
    item
    |> cast(attrs, [:title, :description, :priority, :is_completed])
    |> validate_required([:title])
    |> validate_length(:title, min: 3, max: 200)
    |> validate_inclusion(:priority, ["low", "medium", "high"])
  end
end
