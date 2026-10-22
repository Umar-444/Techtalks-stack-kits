---
name: sqlite-wal-and-concurrency
description: SQLite WAL mode configuration, connection concurrency tuning, and transaction locking patterns for Flask.
---
# SQLite WAL Mode and Concurrency Tuning Skill

## 1. Understanding SQLite Concurrency in Web Applications
By default, SQLite uses rollback journal mode which acquires an exclusive lock on the entire database during writes, blocking concurrent readers.
Write-Ahead Logging (WAL) decouples readers and writers:
- Readers do not block writers.
- Writers do not block readers.
- Only concurrent writers contend with each other.

## 2. Hardened Pragmas Implementation
In `app/db.py`:
```python
def configure_sqlite_pragmas(connection):
    cursor = connection.cursor()
    # 1. Enable WAL mode (persists in db header)
    cursor.execute("PRAGMA journal_mode = WAL;")
    
    # 2. Synchronous NORMAL is fully crash-safe in WAL mode and boosts write throughput 5-10x
    cursor.execute("PRAGMA synchronous = NORMAL;")
    
    # 3. Enforce relational integrity
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # 4. Wait up to 5,000ms for locks instead of throwing instant sqlite3.OperationalError: database is locked
    cursor.execute("PRAGMA busy_timeout = 5000;")
    
    # 5. Increase memory page cache for hot reads
    cursor.execute("PRAGMA cache_size = -64000;")  # 64MB cache
    cursor.close()
```

## 3. Safe WAL Checkpointing
In high-throughput environments, automatically checkpoint the WAL log or execute checkpoint on server shutdown:
```python
def checkpoint_db(db):
    # TRUNCATE flushes and shrinks WAL file back to 0 bytes
    db.execute("PRAGMA wal_checkpoint(TRUNCATE);")
```
