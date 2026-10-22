defmodule Demo.DataCase do
  use ExUnit.CaseTemplate

  using do
    quote do
      alias Demo.Repo
      import Ecto
      import Ecto.Changeset
      import Ecto.Query
      import Demo.DataCase
    end
  end

  setup tags do
    Demo.DataCase.setup_sandbox(tags)
    :ok
  end

  def setup_sandbox(tags) do
    pid = Ecto.Adapters.SQL.Sandbox.start_owner!(Demo.Repo, shared: not tags[:async])
    on_exit(fn -> Ecto.Adapters.SQL.Sandbox.stop_owner(pid) end)
  end
end
