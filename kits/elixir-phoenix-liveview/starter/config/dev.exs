import Config

config :demo, Demo.Repo,
  url: System.get_env("DATABASE_URL") || "ecto://postgres:postgres@localhost:5432/demo_dev",
  stacktrace: true,
  show_sensitive_data_on_connection_error: true,
  pool_size: 10

config :demo, DemoWeb.Endpoint,
  http: [ip: {0, 0, 0, 0}, port: 4000],
  check_origin: false,
  code_reloader: true,
  debug_errors: true,
  secret_key_base: "insecuresecretkeyforlocaldevdevelopmentpurposesonly1234567890abcdef"
