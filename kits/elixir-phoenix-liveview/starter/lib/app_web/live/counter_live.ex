defmodule AppWeb.CounterLive do
  use AppWeb, :live_view

  def mount(_params, _session, socket) do
    {:ok, assign(socket, :val, 0)}
  end

  def handle_event("inc", _params, socket) do
    {:noreply, update(socket, :val, &(&1 + 1))}
  end

  def render(assigns) do
    ~H"""
    <div class="p-6 max-w-sm mx-auto bg-white rounded-xl shadow-md">
      <h2 class="text-xl font-bold">Phoenix LiveView: <%= @val %></h2>
      <button phx-click="inc" class="mt-4 px-4 py-2 bg-[#E85D26] text-white rounded">Increment</button>
    </div>
    """
  end
end
