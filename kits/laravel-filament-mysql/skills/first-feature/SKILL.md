---
name: first-feature
description: Build the canonical Customer Resource module featuring MySQL full-text search, Filament form/table schema, BOLA policy, and Pest tests.
---

# Skill: First Feature (Customer Resource)

## 1. Model & Migration
Create `Customer` model with `name`, `email`, `company_name`, `status`, and full-text index on MySQL 8.4 InnoDB.

## 2. Filament Resource
Implement `CustomerResource` in `app/Filament/Resources/CustomerResource.php`:
- Form: Grid with name, email, company, and status select.
- Table: Text columns with MySQL full-text search override.

## 3. BOLA Policy
Implement `CustomerPolicy` verifying user authorization before any viewing or mutation.

## 4. Done Means
- Admin can log in to `/admin` and view customer listings.
- Typing search query triggers `MATCH ... AGAINST` query in MySQL.
- Feature test passes with code 0.
