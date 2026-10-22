---
name: phoenix-pubsub-realtime
description: Set up distributed Phoenix PubSub topics to broadcast and synchronize real-time state across clients.
---

# Phoenix PubSub Real-time Skill

## Purpose
Integrates distributed event messaging across BEAM nodes and connected client LiveViews.

## Topic Broadcasting Pattern
```elixir
defmodule Demo.Items do
  @topic "items:updates"

  def subscribe do
    Phoenix.PubSub.subscribe(Demo.PubSub, @topic)
  end

  def broadcast({:ok, item} = result, event) do
    Phoenix.PubSub.broadcast(Demo.PubSub, @topic, {event, item})
    result
  end
  def broadcast(error, _event), do: error

  def create_item(attrs \\ %{}) do
    %Item{}
    |> Item.changeset(attrs)
    |> Repo.insert()
    |> broadcast(:item_created)
  end
end
```
