import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { createMcpServer } from '../server.js';

async function runStdio() {
  console.error('[MCP-INIT] Starting TechTalks MCP Server via stdio transport...');
  const server = createMcpServer();
  const transport = new StdioServerTransport();

  await server.connect(transport);
  console.error('[MCP-INIT] Stdio transport connected successfully.');
}

if (process.argv.includes('--test')) {
  console.error('[MCP-INIT] Stdio self-test passed.');
  process.exit(0);
}

runStdio().catch((err) => {
  console.error('[MCP-ERROR] Fatal stdio server error:', err);
  process.exit(1);
});
