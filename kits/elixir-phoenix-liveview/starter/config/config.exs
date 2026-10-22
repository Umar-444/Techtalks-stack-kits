import Config

config :demo,
  ecto_repos: [Demo.Repo],
  generators: [timestamp_type: :utc_datetime]

config :demo, DemoWeb.Endpoint,
  url: [host: "localhost"],
  adapter: Bandit.PhoenixAdapter,
  render_errors: [
    formats: [html: DemoWeb.ErrorHTML, json: DemoWeb.ErrorJSON],
    layout: false
  ],
  pubsub_server: Demo.PubSub,
  live_view: [signing_salt: "liveviewsalt12345"]

config :logger, :console,
  format: "$time $metadata[$level] $message\n",
  metadata: [:request_id]

config :phoenix, :json_library, Jason

import_config "#{config_env()}.exs"
