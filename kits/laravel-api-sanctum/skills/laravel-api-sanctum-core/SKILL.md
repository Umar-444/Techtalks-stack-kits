---
name: "laravel-api-sanctum-core"
description: "Core overview of Laravel 12/13 Sanctum REST API architecture, routing, and configuration."
version: "1.0.0"
---

# Laravel API Sanctum Core Skill

Provides foundational instructions for managing Laravel 12/13 REST APIs with Sanctum authentication, Spatie Query Builder, and rootless Docker containers.

## Core Directives
1. Use `routes/api.php` with `/api/v1/` prefix.
2. Authenticate routes via `Route::middleware('auth:sanctum')`.
3. Use Spatie Query Builder for safe parameter parsing.
4. Enforce strict Model Policies for BOLA protection.
