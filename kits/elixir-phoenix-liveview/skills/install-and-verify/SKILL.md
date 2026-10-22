---
name: install-and-verify
description: Install, orchestrate, and verify the Elixir + Phoenix 1.7+ LiveView + Ecto + PostgreSQL stack.
---

# Install & Verify Skill: Elixir + Phoenix LiveView

## Prerequisites
- Elixir 1.17+ and Erlang/OTP 27+
- PostgreSQL 16+
- Node.js (optional, Tailwind is pre-bundled or standalone)

## OS-Specific Commands

### Linux / macOS
```bash
mix local.hex --force
mix local.rebar --force
mix deps.get
mix ecto.setup
```

### Windows (PowerShell)
```powershell
mix local.hex --force
mix local.rebar --force
mix deps.get
mix ecto.setup
```

## Docker Compose Quickstart
```bash
docker compose up --build -d
```

## Post-Install Verification
Run the verification curl:
```bash
curl -X GET http://localhost:4000/api/healthz
```
Expected output:
```json
{"status":"ok","stack":"elixir-phoenix-liveview","version":"1.0.0"}
```

Access LiveView WebSocket Interface:
- Interactive LiveView: [http://localhost:4000/](http://localhost:4000/)

## Failure Recovery Matrix
| Symptom | Probable Cause | Resolution |
| :--- | :--- | :--- |
| `Postgrex.Error: connection refused` | PostgreSQL database service unreachable | Check `DATABASE_URL` in `.env` and ensure postgres container is running |
| `Phoenix.LiveView.ClientError` | WebSocket connection mismatch or stale CSRF | Refresh browser window to re-initialize LiveSocket with active CSRF token |
| `CompileError: undefined function` | Stale compile cache | Run `mix clean && mix compile` |

## Done Means
Phoenix 1.7+ server runs Bandit/Cowboy on port 4000, establishes live bidirectional WebSocket connections, and synchronizes real-time DOM updates.
