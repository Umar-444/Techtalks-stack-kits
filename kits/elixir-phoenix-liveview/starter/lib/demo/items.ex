defmodule Demo.Items do
  import Ecto.Query, warn: false
  alias Demo.Repo
  alias Demo.Items.Item

  @topic "items:updates"

  def subscribe do
    Phoenix.PubSub.subscribe(Demo.PubSub, @topic)
  end

  def broadcast({:ok, item} = result, event) do
    Phoenix.PubSub.broadcast(Demo.PubSub, @topic, {event, item})
    result
  end
  def broadcast(error, _event), do: error

  def list_items do
    Repo.all(from i in Item, order_by: [desc: i.inserted_at])
  end

  def get_item!(id), do: Repo.get!(Item, id)

  def change_item(%Item{} = item, attrs \\ %{}) do
    Item.changeset(item, attrs)
  end

  def create_item(attrs \\ %{}) do
    %Item{}
    |> Item.changeset(attrs)
    |> Repo.insert()
    |> broadcast(:item_created)
  end

  def toggle_item(%Item{} = item) do
    item
    |> Item.changeset(%{is_completed: not item.is_completed})
    |> Repo.update()
    |> broadcast(:item_updated)
  end

  def delete_item(%Item{} = item) do
    item
    |> Repo.delete()
    |> broadcast(:item_deleted)
  end
end
