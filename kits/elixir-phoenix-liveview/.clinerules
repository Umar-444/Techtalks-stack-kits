# Elixir + Phoenix 1.7+ + LiveView + PostgreSQL - Agent Architecture & Rules

This project adheres to the TechTalks production standards for Elixir, Phoenix 1.7+, LiveView 1.0+, and Ecto.

# Rule 1: Phoenix 1.7+ Architecture & Context Conventions

## Context & Principles
- Strictly adhere to Phoenix Context boundaries: encapsulate business operations in `lib/demo/` and web transport layer in `lib/demo_web/`.
- Treat all Elixir data as immutable; favor pure functions and pattern matching in function heads over nested conditionals.

## Standards
1. **Context Boundary**: All database queries must run through Context modules (e.g. `Demo.Items`). Never call `Repo` directly inside LiveView or Controller modules.
2. **HEEX Formatting**: Use verified HTML HEEX syntax (`~H"""`) with component tags `<.component />` and attribute assignments.
3. **Core Components**: Rely on `DemoWeb.CoreComponents` for flash messages, tables, inputs, buttons, and modals.
4. **Endpoint Hygiene**: Always route incoming requests through the verified endpoint pipeline with security plugs.

# Rule 2: Phoenix LiveView Lifecycle & Stream State

## Context & Principles
- Keep the server-side process lightweight. Avoid storing large lists in assigns; always use `stream/3` and `stream_insert/3` for collections.
- Leverage DOM diffing over WebSockets to minimize payload size (typically < 100 bytes per event).

## Standards
1. **Mount Callback**: In `mount/3`, initialize assigns and streams. Check `connected?(socket)` before subscribing to PubSub topics to prevent duplicate work during static HTTP prerendering.
2. **Event Handling**: Implement `handle_event/3` with pattern matching for user interactions. Return `{:noreply, socket}`.
3. **PubSub Subscriptions**: Handle broadcast messages via `handle_info/2` and apply delta updates to streams via `stream_insert(socket, :items, item)`.
4. **Form Handling**: Use `phx-change="validate"` and `phx-submit="save"` with Ecto Changeset backing to provide instant inline validation.

# Rule 3: Ecto 3.11+ Schema, Changesets & Migrations

## Context & Principles
- Validate all incoming data at the application boundary using Ecto Changesets before writing to PostgreSQL.
- Keep database queries compile-time checked using Ecto.Query macros.

## Standards
1. **Changeset Validation**: Never bypass `cast/4` and `validate_required/3`. Apply custom validators for format, constraints, and business logic.
2. **Migrations**: Write reversible migrations using `change/0` with proper `null: false` constraints, default values, and foreign key references with `on_delete: :delete_all` or `:nothing`.
3. **Indexes**: Explicitly create indexes in migrations for foreign keys and timestamp sort columns (`create index(:items, [:inserted_at])`).
4. **Transactions**: Use `Ecto.Multi` for coordinated writes across multiple tables to ensure atomicity.

# Rule 4: Security, CSRF & LiveView Session Hardening

## Context & Principles
- Protect WebSocket connections from cross-site hijacking and guarantee zero data leakage.
- Enforce strict parameter filtering and sanitization.

## Standards
1. **LiveView CSRF**: Ensure the root layout embeds `<meta name="csrf-token" content={get_csrf_token()} />` and LiveSocket passes the token on connect.
2. **Session Verification**: Always verify user tokens on both the initial HTTP request and the LiveView WebSocket mount.
3. **Parameter Safety**: Pattern match expected keys in `handle_event/3` and cast through Ecto changesets to prevent parameter pollution.
4. **Content Security Policy**: Configure strict CSP and frame options in `endpoint.ex` (`put_secure_browser_headers`).

# Rule 5: ExUnit Testing & LiveView Assertions

## Context & Principles
- Write fast, concurrent unit and integration tests using ExUnit and `Phoenix.LiveViewTest`.
- Run tests in isolated PostgreSQL transactions using `Ecto.Adapters.SQL.Sandbox`.

## Standards
1. **LiveView Test Lifecycle**: Test mount, initial render, form submission, and event dispatches using `live/2`, `element/3`, and `render_submit/2`.
2. **Stream Assertions**: Verify stream items using `has_element?(view, "#items-#{item.id}")`.
3. **Data Isolation**: Run tests with `async: true` whenever possible, utilizing the SQL sandbox checkout.
4. **PubSub Broadcast Tests**: Test that external broadcasts trigger real-time DOM updates in the connected test view.
