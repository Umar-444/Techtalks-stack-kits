defmodule App.MixProject do
  use Mix.Project

  def project do
    [
      app: :liveview_starter,
      version: "0.1.0",
      elixir: "~> 1.17",
      deps: deps()
    ]
  end

  defp deps do
    [
      {:phoenix, "~> 1.7.14"},
      {:phoenix_live_view, "~> 1.0.0"},
      {:ecto_sql, "~> 3.11"},
      {:postgrex, ">= 0.0.0"}
    ]
  end
end
