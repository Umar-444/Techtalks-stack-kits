import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import {
  handleSystemInfo,
  systemInfoSchema,
  handleReadSecureFile,
  readSecureFileSchema,
  handleCalculator,
  calculatorSchema,
} from './tools/index.js';

export function createMcpServer() {
  const server = new McpServer({
    name: 'techtalks-mcp-server',
    version: '1.0.0',
  });

  // Tool 1: System Info
  server.tool(
    'system_info',
    'Retrieve host system metrics and platform telemetry',
    systemInfoSchema.shape,
    async () => {
      const data = handleSystemInfo();
      return {
        content: [{ type: 'text', text: JSON.stringify(data, null, 2) }],
      };
    }
  );

  // Tool 2: Read Secure File
  server.tool(
    'read_secure_file',
    'Read files strictly bounded within the application sandbox directory',
    readSecureFileSchema.shape,
    async ({ filepath }) => {
      try {
        const data = handleReadSecureFile(filepath);
        return {
          content: [{ type: 'text', text: JSON.stringify(data, null, 2) }],
        };
      } catch (err: any) {
        return {
          content: [{ type: 'text', text: `ERROR: ${err.message}` }],
          isError: true,
        };
      }
    }
  );

  // Tool 3: Safe Calculator
  server.tool(
    'calculator',
    'Perform safe arithmetic operations without eval()',
    calculatorSchema.shape,
    async ({ a, b, operation }) => {
      try {
        const result = handleCalculator(a, b, operation);
        return {
          content: [{ type: 'text', text: JSON.stringify({ a, b, operation, result }) }],
        };
      } catch (err: any) {
        return {
          content: [{ type: 'text', text: `ERROR: ${err.message}` }],
          isError: true,
        };
      }
    }
  );

  return server;
}
