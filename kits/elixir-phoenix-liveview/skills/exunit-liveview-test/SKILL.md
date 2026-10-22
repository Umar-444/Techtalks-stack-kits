---
name: exunit-liveview-test
description: Write comprehensive ExUnit unit and integration tests using Phoenix.LiveViewTest.
---

# ExUnit LiveView Test Skill

## Purpose
Provides ready-to-run test templates verifying LiveView rendering, form submissions, and WebSocket streams.

## Example Test
```elixir
defmodule DemoWeb.ItemLiveTest do
  use DemoWeb.ConnCase
  import Phoenix.LiveViewTest

  test "renders item list and creates item via live form", %{conn: conn} do
    {:ok, view, html} = live(conn, ~p"/")
    assert html =~ "Phoenix LiveView"

    assert view
           |> form("#item-form", item: %{title: "Real-time task", priority: "high"})
           |> render_submit() =~ "Real-time task"
  end
end
```
