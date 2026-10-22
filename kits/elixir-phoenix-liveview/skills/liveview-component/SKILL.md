---
name: liveview-component
description: Build, configure, and optimize Phoenix LiveView components with streams and HEEX declarative templates.
---

# Phoenix LiveView Component Skill

## Purpose
Enables creating high-velocity, memory-efficient real-time UI components in Phoenix 1.7+ using `Phoenix.LiveView` and `Phoenix.LiveComponent`.

## Key Workflows
1. **Initialize Streams on Mount**:
   ```elixir
   def mount(_params, _session, socket) do
     if connected?(socket) do
       Demo.Items.subscribe()
     end
     {:ok, stream(socket, :items, Demo.Items.list_items())}
   end
   ```
2. **Handling Events**:
   ```elixir
   def handle_event("save", %{"item" => item_params}, socket) do
     case Demo.Items.create_item(item_params) do
       {:ok, item} ->
         {:noreply, socket |> put_flash(:info, "Item created") |> stream_insert(:items, item, at: 0)}
       {:error, %Ecto.Changeset{} = changeset} ->
         {:noreply, assign(socket, :form, to_form(changeset))}
     end
   end
   ```
3. **Template Rendering with Streams**:
   ```heex
   <div id="items" phx-update="stream" class="divide-y divide-slate-100">
     <div :for={{id, item} <- @streams.items} id={id} class="py-3 flex justify-between">
       <span>{item.title}</span>
     </div>
   </div>
   ```
