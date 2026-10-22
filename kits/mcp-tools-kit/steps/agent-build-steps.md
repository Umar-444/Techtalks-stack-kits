# Step-by-Step Agent Build Guide

### Step 1: Environment & Dependency Installation
- Action: Install `@modelcontextprotocol/sdk` and TypeScript dependencies.
- Command: `npm install && npm run build`
- Verification: Directory `dist/` contains compiled JavaScript files.

### Step 2: Protocol Handshake & Server Initialization
- Action: Instantiate `McpServer` and register server capabilities (tools, resources, prompts).
- Command: `node dist/transports/stdio.js --test`
- Verification: Outputs valid JSON-RPC 2.0 capabilities response.

### Step 3: Tool Implementation & Zod Schema Declaration
- Action: Define tool `read_secure_file` with path boundary verification and Zod schema.
- Command: `npm test -- tests/mcp-tools.test.ts`
- Verification: Tool tests exit 0.

### Step 4: Security Sandbox Assertion
- Action: Test adversarial path traversal payloads (e.g. `../../etc/passwd`).
- Command: `npm test -- tests/security-sandbox.test.ts`
- Verification: Traversal attempts throw `SecurityError` with code -32602.

### Step 5: SSE HTTP Transport Verification
- Action: Start server in SSE mode and query health endpoint.
- Command: `curl -f http://localhost:8080/api/health`
- Verification: Returns JSON payload with `status: ok` and `protocol: mcp-1.0.0`.

### Step 6: Architecture & Static Security Scan
- Action: Run ESLint, TypeScript compiler check, and Semgrep scan.
- Command: `npm run build && semgrep scan`
- Verification: 0 errors, 0 SAST findings.
