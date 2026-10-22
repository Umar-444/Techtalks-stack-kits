---
name: install-and-verify
description: Install, configure, and verify the MCP Server across stdio and SSE transports with healthchecks.
---

# Skill: Install and Verify

## 1. Multi-OS Installation Commands

### macOS (Homebrew)
```bash
brew install node@22
npm install
npm run build
npm test
```

### Ubuntu / Debian
```bash
sudo apt-get update && sudo apt-get install -y nodejs npm
npm install
npm run build
npm test
```

### Windows (WSL2)
```bash
wsl --install -d Ubuntu
sudo apt-get update && sudo apt-get install -y nodejs npm
npm install
npm run build
npm test
```

## 2. Five-Row Failure Recovery Table

| Error / Failure Symptom | Underlying Cause | Concrete Recovery Command |
|---|---|---|
| `SyntaxError: Unexpected token in JSON at position 0` | Non-JSON text printed to stdout in stdio mode | Ensure all logging uses `console.error()`, never `console.log()` |
| `EACCES: permission denied, open '/app/dist'` | Non-root container UID mismatch | `docker compose exec app chown -R 10001:10001 dist` |
| `Claude Desktop fails to detect tools` | Invalid absolute path in config | Verify node path using `which node` and verify absolute path to `dist/transports/stdio.js` |
| `SSE connection timeout` | Port 8080 blocked or container halted | `docker compose ps` and `curl -v http://localhost:8080/api/health` |
| `Error: Cannot find module '@modelcontextprotocol/sdk'` | Build step skipped or node_modules missing | `npm install && npm run build` |

## 3. Done Means
- `npm test` passes with 0 test failures.
- `curl -f http://localhost:8080/api/health` returns status `ok`.
- Clean stdio handshake tested.
