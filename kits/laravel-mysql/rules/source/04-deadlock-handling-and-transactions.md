---
id: 04-deadlock-handling-and-transactions
title: Deadlock-Resilient Transactions, Locking, and Read/Write Splitting
globs: "starter/app/**/*.php,starter/config/database.php"
alwaysApply: true
---

# Deadlock-Resilient Transactions, Locking, and Read/Write Splitting

## 1. Deadlock Retry Protocol
- MySQL InnoDB row-level locking can encounter deadlocks (Error 1213) under high write concurrency.
- Wrap critical mutations in `DB::transaction()` with automatic retry attempts:
  ```php
  DB::transaction(function () use ($orderId, $amount) {
      $account = Account::where('id', $accountId)->lockForUpdate()->firstOrFail();
      $account->decrement('balance', $amount);
  }, attempts: 5);
  ```

## 2. Pessimistic vs Optimistic Locking
- Use `lockForUpdate()` exclusively inside active transactions when updating balances, inventory, or reservations.
- Keep transaction execution windows under 50ms to prevent lock wait timeouts.

## 3. Read/Write Connection Splitting
- Configure dedicated read replica pools in `config/database.php`:
  ```php
  'mysql' => [
      'read' => ['host' => [env('DB_READ_HOST_1'), env('DB_READ_HOST_2')]],
      'write' => ['host' => [env('DB_HOST')]],
      'sticky' => true,
  ],
  ```
  Ensures immediate read-after-write consistency within the same request lifecycle.
