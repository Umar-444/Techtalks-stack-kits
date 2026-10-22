---
name: install-and-verify
description: Clean install, database initialization, automated test run, and health probe verification for Hono Bun SQLite kit.
---

# Install and Verify Skill: Hono + Bun + SQLite

## Overview
Install project dependencies with Bun, execute database migrations, run unit and integration tests, and probe the live health endpoint.

## Step-by-Step Verification

### 1. Verify Bun Installation
```bash
bun --version
```
Ensure Bun 1.1+ is installed.

### 2. Install Dependencies
```bash
bun install
```

### 3. Run Native Bun Test Suite
```bash
bun test
```
Expected output:
```text
bun test v1.1.29 (x64-linux)
✓ GET /healthz returns 200 OK JSON [0.42ms]
✓ POST /api/messages creates message with valid payload [1.12ms]
✓ POST /api/messages rejects invalid payload (400 Bad Request) [0.35ms]
✓ GET /api/messages returns message collection with pagination [0.65ms]

4 pass, 0 fail
Ran 4 tests across 1 file. [4.80ms]
```

### 4. Start Development Server
```bash
bun run dev &
sleep 1
curl -s http://localhost:3000/healthz
```
Expected response:
```json
{"status":"ok","app":"ts-hono-bun-sqlite","version":"1.0.0","runtime":"bun"}
```
