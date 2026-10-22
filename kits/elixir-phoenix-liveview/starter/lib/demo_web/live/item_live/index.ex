defmodule DemoWeb.ItemLive.Index do
  use Phoenix.LiveView
  alias Demo.Items
  alias Demo.Items.Item

  @impl true
  def mount(_params, _session, socket) do
    if connected?(socket) do
      Items.subscribe()
    end

    items = Items.list_items()

    socket =
      socket
      |> assign(:form, to_form(Items.change_item(%Item{})))
      |> assign(:total_count, length(items))
      |> stream(:items, items)

    {:ok, socket}
  end

  @impl true
  def handle_event("validate", %{"item" => item_params}, socket) do
    changeset = Items.change_item(%Item{}, item_params)
    {:noreply, assign(socket, :form, to_form(changeset, action: :validate))}
  end

  @impl true
  def handle_event("save", %{"item" => item_params}, socket) do
    case Items.create_item(item_params) do
      {:ok, item} ->
        socket =
          socket
          |> put_flash(:info, "Item created successfully.")
          |> assign(:form, to_form(Items.change_item(%Item{})))
          |> update(:total_count, &(&1 + 1))
          |> stream_insert(:items, item, at: 0)

        {:noreply, socket}

      {:error, %Ecto.Changeset{} = changeset} ->
        {:noreply, assign(socket, :form, to_form(changeset))}
    end
  end

  @impl true
  def handle_event("toggle", %{"id" => id}, socket) do
    item = Items.get_item!(id)
    {:ok, updated} = Items.toggle_item(item)
    {:noreply, stream_insert(socket, :items, updated)}
  end

  @impl true
  def handle_event("delete", %{"id" => id}, socket) do
    item = Items.get_item!(id)
    {:ok, _} = Items.delete_item(item)
    {:noreply, stream_delete(socket, :items, item)}
  end

  @impl true
  def handle_info({:item_created, item}, socket) do
    {:noreply, socket |> update(:total_count, &(&1 + 1)) |> stream_insert(:items, item, at: 0)}
  end

  @impl true
  def handle_info({:item_updated, item}, socket) do
    {:noreply, stream_insert(socket, :items, item)}
  end

  @impl true
  def handle_info({:item_deleted, item}, socket) do
    {:noreply, stream_delete(socket, :items, item)}
  end
end
