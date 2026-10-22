# Model Context Protocol (MCP) Server Blueprint Kit (stdio + SSE)

A production-grade, hardened Model Context Protocol (MCP) server reference kit supporting `stdio` transport for local AI assistants (Claude Desktop, Cursor, Antigravity) and Server-Sent Events (`SSE`) HTTP transport for remote microservices and agent swarms.

---

## 1. Architecture Overview

```
  +---------------------------------------------------------------------------------+
  | Local AI Desktop Client (Claude Desktop / Cursor IDE / Antigravity Agent)       |
  +---------------------------------------------------------------------------------+
                                     |
                                     | stdio (JSON-RPC 2.0 pipe)
                                     v
+-----------------------------------------------------------------------------------+
| MCP Server (Node.js 22 LTS Alpine - UID 10001:10001 Rootless)                     |
|                                                                                   |
|  +----------------------------+     +------------------------------------------+  |
|  | Transport Layer            |     | Protocol Engine                          |  |
|  | - StdioServerTransport     |     | - JSON-RPC 2.0 Handshake & Capabilities  |  |
|  | - SSEServerTransport (HTTP)| <-> | - Request Routing & Error Serialization  |  |
|  +----------------------------+     | - Zod Input Schema Sanitizer             |  |
|                                     +------------------------------------------+  |
|                                                      |                            |
|       +----------------------------------------------+--------------------+       |
|       |                                              |                    |       |
|       v                                              v                    v       |
|  +-----------------------+              +-----------------------+   +-----------+ |
|  | Tools System          |              | Resources Provider    |   | Prompts   | |
|  | - system_info         |              | - file:// sandboxed   |   | - code    | |
|  | - read_secure_file    |              | - internal:// config  |   |   review  | |
|  | - query_runner        |              |   templates           |   |   agent   | |
|  +-----------------------+              +-----------------------+   +-----------+ |
+-----------------------------------------------------------------------------------+
                                     |
                                     | SSE / HTTP (Port 8080)
                                     v
  +---------------------------------------------------------------------------------+
  | Distributed Agent Swarm / Web Client (LangGraph / CrewAI / Remote Services)     |
  +---------------------------------------------------------------------------------+
```

---

## 2. Quickstart

### Option A: Local Stdio Transport (Claude Desktop / CLI)
```bash
# 1. Clone repository
git clone https://github.com/Umar-444/Techtalks-stack-kits.git
cd Techtalks-stack-kits/kits/mcp-tools-kit/starter

# 2. Install dependencies & build
npm install
npm run build

# 3. Add to claude_desktop_config.json:
# {
#   "mcpServers": {
#     "techtalks-mcp": {
#       "command": "node",
#       "args": ["/absolute/path/to/kits/mcp-tools-kit/starter/dist/transports/stdio.js"]
#     }
#   }
# }
```

### Option B: Remote SSE HTTP Transport (Docker)
```bash
docker compose up -d --build
curl -f http://localhost:8080/api/health
```

---

## 3. Seven-Part OS Installation Guide

### Part 1: Prerequisites
- Docker Engine 26+ and Docker Compose v2.27+
- Node.js 22 LTS with `npm` or `pnpm`

### Part 2: macOS Setup (Homebrew)
```bash
brew install node@22
npm install
npm run build
```

### Part 3: Ubuntu / Debian Setup
```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs
npm install && npm run build
```

### Part 4: Fedora / RHEL Setup
```bash
sudo dnf install -y nodejs
npm install && npm run build
```

### Part 5: Arch Linux Setup
```bash
sudo pacman -S nodejs npm
npm install && npm run build
```

### Part 6: Windows (WSL2 Ubuntu)
```bash
wsl --install -d Ubuntu
sudo apt-get update && sudo apt-get install -y nodejs npm
npm install && npm run build
```

### Part 7: Verification Command
```bash
npm test
```

---

## 4. Skills Inventory

| Skill Name | Purpose | Location |
|---|---|---|
| `install-and-verify` | Boot environment, configure stdio/SSE, verify probes | `skills/install-and-verify/SKILL.md` |
| `first-feature` | Author canonical sandboxed tools with Zod validation | `skills/first-feature/SKILL.md` |
| `mcp-tool-authoring` | Step-by-step tool definition, error codes, and progress | `skills/mcp-tool-authoring/SKILL.md` |
| `mcp-transport-configuration` | Stdio vs. SSE configuration and connection management | `skills/mcp-transport-configuration/SKILL.md` |
| `mcp-security-sandboxing` | Path traversal prevention, shell injection defense | `skills/mcp-security-sandboxing/SKILL.md` |
| `mcp-tools-kit-core` | Operational workflows, MCP Inspector debugging | `skills/mcp-tools-kit-core/SKILL.md` |

---

## 5. Security & Verification Evidence

All 18 checkpoints verified in `VERIFICATION.md`. Zero-drift transpiled across all 6 AI coding agent formats.
