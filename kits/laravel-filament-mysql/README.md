# Laravel 12/13 + Filament 4 + MySQL 8.4 LTS Blueprint Kit

A production-grade, enterprise administrative platform combining Laravel 12/13, Filament 4 admin panel, and MySQL 8.4 LTS InnoDB. Features native full-text indexing, generated virtual columns, zero-trust BOLA authorization policies, and rootless container isolation.

---

## 1. Architecture Overview

```
                      +---------------------------------------+
                      |       Web Browser / Admin Staff       |
                      +---------------------------------------+
                                          |
                                          | HTTPS (Port 443 / 8000)
                                          v
+-----------------------------------------------------------------------------------+
| App Container (PHP 8.3 / 8.4 FPM + Nginx - UID 10001:10001 Rootless)             |
|                                                                                   |
|  +----------------------------+     +------------------------------------------+  |
|  | Filament 4 Admin Panel     |     | Laravel 12/13 Core                       |  |
|  | - Table Builder & Filters  |     | - Route Model Binding & BOLA Policies    |  |
|  | - Form Components & Schema | <-> | - Strict Eloquent Models & DTOs          |  |
|  | - Bulk Actions & Widgets   |     | - Pest Architecture & Feature Tests      |  |
|  +----------------------------+     +------------------------------------------+  |
+-----------------------------------------------------------------------------------+
                       |                                   |
                       | SQL (Port 3306)                   | RESP (Port 6379)
                       v                                   v
+---------------------------------------------+   +---------------------------------+
| MySQL 8.4 LTS Database (InnoDB Engine)      |   | Redis 7.2 Service               |
| - utf8mb4_0900_ai_ci Collation              |   | - Session Cache & Tags          |
| - Full-Text Search (MATCH ... AGAINST)      |   | - Rate Limit Counter            |
| - Generated Virtual Search Columns          |   | - Queue Processing              |
| - Deadlock Resilience with Lock Timeout     |   +---------------------------------+
+---------------------------------------------+
```

---

## 2. Quickstart

```bash
# 1. Clone repository
git clone https://github.com/Umar-444/Techtalks-stack-kits.git
cd Techtalks-stack-kits/kits/laravel-filament-mysql/starter

# 2. Configure environment
cp .env.example .env

# 3. Spin up rootless container stack
docker compose up -d --build

# 4. Run database migrations & seeders
docker compose exec app php artisan migrate --seed

# 5. Execute test suite
docker compose exec app php artisan test --compact
```

---

## 3. Seven-Part OS Installation Guide

### Part 1: Prerequisites
- Docker Engine 26+ and Docker Compose v2.27+
- PHP 8.3 or 8.4 with extensions: `pdo_mysql`, `mbstring`, `intl`, `bcmath`, `curl`, `redis`
- Composer 2.7+

### Part 2: macOS Setup (Homebrew)
```bash
brew install php@8.3 composer mysql-client redis
brew services start redis
```

### Part 3: Ubuntu / Debian Setup
```bash
sudo apt-get update && sudo apt-get install -y php8.3-cli php8.3-mysql php8.3-mbstring php8.3-intl php8.3-xml php8.3-curl php8.3-redis composer
```

### Part 4: Fedora / RHEL Setup
```bash
sudo dnf install -y php-cli php-mysqlnd php-mbstring php-intl php-xml composer redis
```

### Part 5: Arch Linux Setup
```bash
sudo pacman -S php php-intl composer redis mariadb-clients
```

### Part 6: Windows (WSL2 Ubuntu)
```bash
wsl --install -d Ubuntu
sudo apt-get update && sudo apt-get install -y php8.3-cli php8.3-mysql composer
```

### Part 7: Verification Command
```bash
curl -f http://localhost:8000/api/health || exit 1
```

---

## 4. Skills Inventory

| Skill Name | Purpose | Location |
|---|---|---|
| `install-and-verify` | Boot environment, run migrations, and verify probes | `skills/install-and-verify/SKILL.md` |
| `first-feature` | Customer Resource with MySQL full-text search & BOLA policy | `skills/first-feature/SKILL.md` |
| `filament-resource` | Scaffold Filament tables, forms, filters, and actions | `skills/filament-resource/SKILL.md` |
| `mysql-innodb-optimization` | MySQL 8.4 tuning, full-text indexes, and deadlock retry | `skills/mysql-innodb-optimization/SKILL.md` |
| `laravel-policy` | BOLA zero-trust authorization policies | `skills/laravel-policy/SKILL.md` |
| `laravel-filament-mysql-core` | Operational workflows and artisan conventions | `skills/laravel-filament-mysql-core/SKILL.md` |

---

## 5. Security & Verification Evidence

All 18 checkpoints verified in `VERIFICATION.md`. Zero-drift transpiled across all 6 AI coding agent formats.
