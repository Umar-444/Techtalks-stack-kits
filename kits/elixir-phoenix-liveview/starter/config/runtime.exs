import Config

if System.get_env("PHX_SERVER") do
  config :demo, DemoWeb.Endpoint, server: true
end
