# Laravel 12/13 + AI Features (LLM Orchestration, Embeddings & RAG)

A production-grade enterprise Laravel blueprint kit for shipping AI-powered capabilities with strict engineering discipline. Features structured LLM output generation, function/tool execution, PostgreSQL pgvector embeddings, semantic search, prompt injection screening, and asynchronous queue workers.

---

## 1. Architecture Overview

```
                      +---------------------------------------+
                      |       Web / API Client / Agent        |
                      +---------------------------------------+
                                          |
                                          | HTTPS / SSE (Port 8000)
                                          v
+-----------------------------------------------------------------------------------+
| App Container (PHP 8.3 / 8.4 FPM - UID 10001:10001 Rootless)                      |
|                                                                                   |
|  +----------------------------+     +------------------------------------------+  |
|  | AI Gateway & Guardrails    |     | Laravel 12/13 Core                       |  |
|  | - Prompt Injection Screen  |     | - Asynchronous Queue Dispatch (Redis)    |  |
|  | - JSON Schema Enforcer     | <-> | - Eloquent Model with pgvector Cast      |  |
|  | - Tool / Function Dispatch |     | - Pest Architecture & Feature Tests      |  |
|  +----------------------------+     +------------------------------------------+  |
+-----------------------------------------------------------------------------------+
                       |                                   |
                       | SQL / pgvector (Port 5432)        | RESP (Port 6379)
                       v                                   v
+---------------------------------------------+   +---------------------------------+
| PostgreSQL 16 + pgvector Database           |   | Redis 7.2 Service               |
| - Extension: vector                         |   | - Horizon Queue Processing      |
| - HNSW Index on embedding vector(1536)      |   | - Token Usage Rate Limiting     |
| - Cosine Distance (<=> operator)            |   | - Cache-aside Vector Embeddings |
| - Strict Row-Level Multi-Tenancy            |   +---------------------------------+
+---------------------------------------------+
```

---

## 2. Quickstart

```bash
# 1. Clone repository
git clone https://github.com/Umar-444/Techtalks-stack-kits.git
cd Techtalks-stack-kits/kits/laravel-ai-features/starter

# 2. Configure environment
cp .env.example .env

# 3. Spin up rootless container stack
docker compose up -d --build

# 4. Run database migrations & seeders (enables pgvector)
docker compose exec app php artisan migrate --seed

# 5. Execute test suite
docker compose exec app php artisan test --compact
```

---

## 3. Seven-Part OS Installation Guide

### Part 1: Prerequisites
- Docker Engine 26+ and Docker Compose v2.27+
- PHP 8.3 or 8.4 with extensions: `pdo_pgsql`, `mbstring`, `intl`, `bcmath`, `curl`, `redis`
- Composer 2.7+

### Part 2: macOS Setup (Homebrew)
```bash
brew install php@8.3 composer libpq redis
brew services start redis
```

### Part 3: Ubuntu / Debian Setup
```bash
sudo apt-get update && sudo apt-get install -y php8.3-cli php8.3-pgsql php8.3-mbstring php8.3-intl php8.3-xml php8.3-curl php8.3-redis composer
```

### Part 4: Fedora / RHEL Setup
```bash
sudo dnf install -y php-cli php-pgsql php-mbstring php-intl php-xml composer redis
```

### Part 5: Arch Linux Setup
```bash
sudo pacman -S php php-pgsql php-intl composer redis postgresql-libs
```

### Part 6: Windows (WSL2 Ubuntu)
```bash
wsl --install -d Ubuntu
sudo apt-get update && sudo apt-get install -y php8.3-cli php8.3-pgsql composer
```

### Part 7: Verification Command
```bash
curl -f http://localhost:8000/api/health || exit 1
```

---

## 4. Skills Inventory

| Skill Name | Purpose | Location |
|---|---|---|
| `install-and-verify` | Boot environment, run pgvector migrations, verify health | `skills/install-and-verify/SKILL.md` |
| `first-feature` | Semantic Document Search & RAG Q&A with pgvector | `skills/first-feature/SKILL.md` |
| `llm-structured-output` | Strict JSON Schema validation & typed DTO parsing | `skills/llm-structured-output/SKILL.md` |
| `pgvector-semantic-search` | Chunking, embeddings calculation, and HNSW cosine queries | `skills/pgvector-semantic-search/SKILL.md` |
| `prompt-injection-defense` | Multi-layered input screening and canary leak detection | `skills/prompt-injection-defense/SKILL.md` |
| `laravel-ai-features-core` | Operational workflows, queue workers, and test mocks | `skills/laravel-ai-features-core/SKILL.md` |

---

## 5. Security & Verification Evidence

All 18 checkpoints verified in `VERIFICATION.md`. Zero-drift transpiled across all 6 AI coding agent formats.
