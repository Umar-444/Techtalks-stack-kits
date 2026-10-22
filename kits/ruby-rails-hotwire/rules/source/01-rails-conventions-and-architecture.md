---
id: 01-rails-conventions-and-architecture
title: Rails 8 Architecture and Solid Stack Standards
globs: "app/**/*.rb,config/**/*.rb,Gemfile"
alwaysApply: true
---

# Rails 8 Architecture and Solid Stack Standards

## 1. Directory Structure & Omakase Patterns
- Adhere strictly to default Rails 8 directory layout:
  - `app/models/`: Domain models inheriting from `ApplicationRecord`, containing business validations and associations.
  - `app/controllers/`: Resourceful controllers inheriting from `ApplicationController`.
  - `app/views/`: Semantic HTML templates using Turbo Frames and Turbo Stream formats.
  - `app/javascript/controllers/`: Lightweight Stimulus controllers for client-side progressive enhancement.
  - `config/`: Application configuration, environment settings, and routes.
  - `db/migrate/`: Immutable schema migrations.

## 2. Rails 8 Solid Suite Conventions
- Leverage native Solid Stack gems for zero-external-dependency infrastructure:
  - **Solid Cache**: Database-backed caching adapter replacing Redis for key-value stores.
  - **Solid Queue**: Database-backed active job queuing system with concurrent worker execution.
  - **Solid Cable**: Database-backed WebSockets connection hub powering ActionCable and Turbo Streams.
- Do NOT introduce external Redis or Sidekiq dependencies unless explicitly required by enterprise streaming volume.

## 3. Controller Actions & Responders
- Keep controller actions minimal and RESTful (Index, Show, New, Create, Edit, Update, Destroy).
- Respond with standard format negotiation:
  ```ruby
  respond_to do |format|
    format.html { redirect_to @post, notice: "Post created successfully." }
    format.turbo_stream
  end
  ```
- Reject business logic inside controllers; delegate to domain models or service objects.
