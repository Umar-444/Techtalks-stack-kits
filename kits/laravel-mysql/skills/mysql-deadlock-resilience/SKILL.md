---
name: mysql-deadlock-resilience
description: Managing row-level locks, transaction retry loops, and connection pool timeouts in MySQL InnoDB.
---

# MySQL Deadlock Resilience Skill

## Overview
Prevent lock wait timeouts and deadlocks in concurrent write environments.

## Pattern
```php
DB::transaction(function () {
    $wallet = Wallet::where('id', $walletId)->lockForUpdate()->firstOrFail();
    $wallet->balance += $credit;
    $wallet->save();
}, attempts: 5);
```
