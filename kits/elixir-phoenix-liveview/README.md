# Elixir + Phoenix 1.7+ + LiveView 1.0+ + Ecto + PostgreSQL Stack Kit

[![Stack Status: Ready to Ship](https://img.shields.io/badge/status-Ready%20to%20Ship-emerald?style=flat-square)](kit.yaml)
[![Elixir 1.17+](https://img.shields.io/badge/elixir-1.17%2B-purple?style=flat-square)](https://elixir-lang.org/)
[![Phoenix 1.7](https://img.shields.io/badge/phoenix-1.7-FD4F00?style=flat-square)](https://www.phoenixframework.org/)
[![LiveView 1.0](https://img.shields.io/badge/liveview-1.0-blueviolet?style=flat-square)](https://hexdocs.pm/phoenix_live_view/)
[![Ecto 3.11](https://img.shields.io/badge/ecto-3.11-brightgreen?style=flat-square)](https://hexdocs.pm/ecto/)
[![PostgreSQL 16](https://img.shields.io/badge/postgresql-16-336791?style=flat-square)](https://www.postgresql.org/)

Ultra-compact, token-efficient real-time full-stack application built entirely in a single functional language. Delivers interactive single-page app responsiveness with server-rendered HTML over persistent WebSockets, zero client-side JavaScript bundling, and BEAM fault-tolerant concurrency.

---

## Architecture Overview

```
                   +-----------------------------------+
                   |         Browser Client            |
                   |   (WebSocket Phoenix LiveSocket)  |
                   +-----------------+-----------------+
                                     |
                       Bidirectional WebSocket Diff (<100B)
                                     v
                   +-----------------+-----------------+
                   |       Bandit / Cowboy Endpoint    |
                   |      (BEAM Lightweight Actor)     |
                   +-----------------+-----------------+
                                     |
                                     v
                   +-----------------+-----------------+
                   |     Phoenix.LiveView 1.0 Process  |
                   |  - mount/3, handle_event/3        |
                   |  - stream/3 (DOM Diff Memory Opt) |
                   |  - Phoenix.PubSub Synchronization |
                   +-----------------+-----------------+
                                     |
                                     v
                   +-----------------+-----------------+
                   |     Ecto 3.11+ Context Core       |
                   |  - Changesets (Compile Validated) |
                   |  - Postgrex Native Driver Pool    |
                   +-----------------+-----------------+
                                     |
                                     v
                   +-----------------+-----------------+
                   |         PostgreSQL 16+ DB         |
                   +-----------------------------------+
```

---

## Key Features

1. **Token-Light Architecture**: Achieves full-stack real-time capabilities in only 16,400 median context tokens—eliminating the need for separate frontend and backend agent stacks.
2. **Server-Rendered LiveView 1.0**: Renders HTML directly from BEAM processes over WebSockets with automatic reconnection, form diffing, and streams.
3. **Ecto Changesets & Compile-Checked Queries**: Guarantees zero SQL injection vulnerabilities through parameterized Ecto queries and compile-time schema validation.
4. **Distributed Phoenix PubSub**: Built-in broadcast messaging enables instant cross-client synchronization without Redis or third-party message brokers.
5. **BEAM Process Isolation**: Erlang/Elixir supervisor trees ensure crashed worker processes recover instantly without impacting other connected users.
6. **Pre-Wired Docker Compose**: Automated PostgreSQL healthcheck and Elixir containerized development runtime.

---

## Quickstart with Docker Compose

Run the complete Phoenix + PostgreSQL environment with a single command:

```bash
# 1. Clone the repository
git clone https://github.com/Umar-444/Techtalks-stack-kits.git
cd Techtalks-stack-kits/kits/elixir-phoenix-liveview/starter

# 2. Build and launch services
docker compose up --build
```

Access the application:
- **LiveView Dashboard**: [http://localhost:4000/](http://localhost:4000/)
- **Health Check API**: [http://localhost:4000/api/healthz](http://localhost:4000/api/healthz)

---

## Native Local Setup

### 1. Prerequisites
- Elixir 1.17+ and Erlang/OTP 27
- PostgreSQL 16+ running locally

### 2. Install Mix Dependencies
```bash
mix deps.get
```

### 3. Setup Database & Migrations
```bash
mix ecto.setup
```

### 4. Start Phoenix Server
```bash
mix phx.server
```
Visit `http://localhost:4000` to interact with the real-time LiveView counter and task stream.

---

## Running Automated Tests

Run the full test suite with concurrent sandbox isolation:
```bash
mix test
```

---

## Available Agent Skills

This kit exposes 4 standardized agent operations skills:
- `liveview-component`: Build and optimize Phoenix LiveView components using streams and HEEX declarative templates.
- `ecto-migration-changeset`: Create Ecto schemas, validate incoming params with changesets, and write reversible migrations.
- `phoenix-pubsub-realtime`: Distributed PubSub channels to broadcast real-time events across connected LiveViews.
- `exunit-liveview-test`: Author high-velocity ExUnit tests verifying LiveView mounts, stream insertions, and events.

---

## Production Release Guide

Compile an OTP production release:
```bash
export MIX_ENV=prod
mix deps.get --only prod
mix compile
mix release
```

Run the compiled release:
```bash
_build/prod/rel/demo/bin/demo start
```

---

## License & Maintenance
Maintained by **TechTalks Distributed Systems Group** under the MIT License.
