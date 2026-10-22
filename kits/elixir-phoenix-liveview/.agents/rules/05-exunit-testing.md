# Rule 5: ExUnit Testing & LiveView Assertions

## Context & Principles
- Write fast, concurrent unit and integration tests using ExUnit and `Phoenix.LiveViewTest`.
- Run tests in isolated PostgreSQL transactions using `Ecto.Adapters.SQL.Sandbox`.

## Standards
1. **LiveView Test Lifecycle**: Test mount, initial render, form submission, and event dispatches using `live/2`, `element/3`, and `render_submit/2`.
2. **Stream Assertions**: Verify stream items using `has_element?(view, "#items-#{item.id}")`.
3. **Data Isolation**: Run tests with `async: true` whenever possible, utilizing the SQL sandbox checkout.
4. **PubSub Broadcast Tests**: Test that external broadcasts trigger real-time DOM updates in the connected test view.
