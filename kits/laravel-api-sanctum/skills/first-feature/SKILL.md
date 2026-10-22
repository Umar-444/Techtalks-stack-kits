---
name: "first-feature"
description: "Guide for implementing a new RESTful endpoint with Form Request, Resource, Policy, and Test."
version: "1.0.0"
---

# First Feature Skill: Creating an API Resource

1. Generate Model and Migration:
   ```bash
   php artisan make:model Task -m
   ```
2. Generate Form Requests:
   ```bash
   php artisan make:request Task/StoreTaskRequest
   ```
3. Generate API Resource:
   ```bash
   php artisan make:resource TaskResource
   ```
4. Generate Policy:
   ```bash
   php artisan make:policy TaskPolicy --model=Task
   ```
5. Author Feature Test verifying BOLA prevention and Sanctum token validation.
