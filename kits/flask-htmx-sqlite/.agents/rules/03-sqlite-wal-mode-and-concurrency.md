# 03 Sqlite Wal Mode And Concurrency

﻿---
id: sqlite-wal-mode-and-concurrency
title: SQLite WAL Mode & Concurrency Architecture
globs: "**/*.{py,sql}"
alwaysApply: true
---
# SQLite Production Concurrency & WAL Performance Standards

## 1. Mandatory SQLite PRAGMA Configuration
- SQLite must always be initialized with Write-Ahead Logging (WAL) and explicit busy timeout limits on every new connection:
  ```python
  import sqlite3
  from flask import g, current_app

  def get_db():
      if "db" not in g:
          g.db = sqlite3.connect(
              current_app.config["DATABASE"],
              detect_types=sqlite3.PARSE_DECLTYPES
          )
          g.db.row_factory = sqlite3.Row
          
          # Enforce production concurrency pragmas
          cursor = g.db.cursor()
          cursor.execute("PRAGMA journal_mode = WAL;")
          cursor.execute("PRAGMA synchronous = NORMAL;")
          cursor.execute("PRAGMA foreign_keys = ON;")
          cursor.execute("PRAGMA busy_timeout = 5000;")  # 5-second lock queue
          cursor.close()
      return g.db
  ```

## 2. Request Lifecycle Connection Teardown
- Register automatic connection closure via Flask's teardown callback:
  ```python
  def close_db(e=None):
      db = g.pop("db", None)
      if db is not None:
          db.close()

  def init_app(app):
      app.teardown_appcontext(close_db)
      app.cli.add_command(init_db_command)
  ```

## 3. Atomic Transactions & Write Contention Defenses
- When performing mutations involving multiple statements, use explicit transaction contexts:
  ```python
  db = get_db()
  try:
      with db:
          db.execute("INSERT INTO audit_logs (action) VALUES (?)", ("create",))
          db.execute("INSERT INTO items (title, content) VALUES (?, ?)", (title, content))
  except sqlite3.OperationalError as exc:
      if "database is locked" in str(exc):
          current_app.logger.warning("SQLite write contention encountered: %s", exc)
          # Handled by busy_timeout, fallback to 503 retry-after
      raise
  ```

