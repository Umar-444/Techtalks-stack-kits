defmodule DemoWeb.HealthController do
  use Phoenix.Controller

  def check(conn, _params) do
    json(conn, %{status: "ok", stack: "elixir-phoenix-liveview", version: "1.0.0"})
  end
end
