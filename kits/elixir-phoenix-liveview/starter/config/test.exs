import Config

config :demo, Demo.Repo,
  url: System.get_env("DATABASE_URL") || "ecto://postgres:postgres@localhost:5432/demo_test",
  pool: Ecto.Adapters.SQL.Sandbox,
  pool_size: 10

config :demo, DemoWeb.Endpoint,
  http: [ip: {127, 0, 0, 1}, port: 4002],
  secret_key_base: "testsecretkeyforunitandintegrationtestpurposesonly1234567890abcdef",
  server: false

config :logger, level: :warning
