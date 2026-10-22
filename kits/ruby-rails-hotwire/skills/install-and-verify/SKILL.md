---
name: install-and-verify
description: Clean setup, dependency installation, migration execution, and verification for Ruby on Rails 8 Hotwire kit.
---

# Install and Verify Skill

## Overview
This skill executes a complete, clean installation and operational verification of the Ruby on Rails 8 Hotwire stack.

## Steps to Execute

### 1. Environment Verification
Verify that Ruby 3.3+ and Bundler are installed:
```bash
ruby -v
bundle -v
```

### 2. Dependency Installation
Install all gems specified in `Gemfile`:
```bash
bundle install
```

### 3. Database Initialization & Migration
Setup the database and run all migrations:
```bash
bin/rails db:prepare
```

### 4. Security Audit
Execute Brakeman static analysis to verify zero vulnerabilities:
```bash
bundle exec brakeman -q -z
```

### 5. Automated Test Suite
Run the test suite to confirm core endpoints and models pass:
```bash
bin/rails test
```

### 6. Health Probe Verification
Start the server and probe the `/healthz` endpoint:
```bash
bin/rails server -p 3000 &
sleep 3
curl -s http://localhost:3000/healthz
```
Expected output:
```json
{"status":"ok","app":"ruby-rails-hotwire","version":"1.0.0"}
```
