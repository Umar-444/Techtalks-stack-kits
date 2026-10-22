---
name: sqlite-wal-optimization
description: Configure SQLite Write-Ahead Logging (WAL), busy timeout, and memory pragmas for zero-lock concurrency.
---

# SQLite WAL Mode & Concurrency Optimization

## Why WAL Mode in SQLite?
Standard SQLite locking locks the entire database file during writes, blocking readers and triggering `database is locked` errors under concurrent web traffic.
WAL (Write-Ahead Logging) decouples readers and writers:
- Readers never block writers.
- Writers never block readers.
- Multiple readers read simultaneously while one writer appends to the WAL log.

## Configuring SQLite Pragmas
In Loco's database initializer or connection options:
```rust
use sea_orm::ConnectOptions;
use std::time::Duration;

pub fn configure_sqlite_options(db_url: &str) -> ConnectOptions {
    let mut opt = ConnectOptions::new(db_url);
    opt.max_connections(10)
        .min_connections(1)
        .connect_timeout(Duration::from_secs(5))
        .acquire_timeout(Duration::from_secs(3))
        .idle_timeout(Duration::from_secs(600))
        .sqlx_logging(true);
    
    // SQLite connection string should include:
    // sqlite://storage/db.sqlite?mode=rwc&_journal_mode=WAL&_busy_timeout=5000&_synchronous=NORMAL
    opt
}
```

## Verification Query
Execute in sqlite3 CLI to confirm WAL mode is active:
```sql
PRAGMA journal_mode;
-- Returns: wal

PRAGMA busy_timeout;
-- Returns: 5000
```
