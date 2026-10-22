FROM hexpm/elixir:1.17.3-erlang-27.1.2-alpine-3.20.3

# Install build dependencies
RUN apk add --no-cache build-base npm git inotify-tools curl postgresql-client

WORKDIR /app

# Install Hex and Rebar
RUN mix local.hex --force && \
    mix local.rebar --force

ENV MIX_ENV=dev

# Cache mix dependencies
COPY mix.exs mix.lock* ./
RUN mix deps.get

COPY . /app

EXPOSE 4000

CMD ["sh", "-c", "mix ecto.create && mix ecto.migrate && mix phx.server"]
