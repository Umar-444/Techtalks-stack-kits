import express from 'express';
import cors from 'cors';
import { SSEServerTransport } from '@modelcontextprotocol/sdk/server/sse.js';
import { createMcpServer } from '../server.js';

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 8080;
let sseTransport: SSEServerTransport | null = null;

app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    protocol: 'mcp-1.0.0',
    transport: 'sse',
    tools_count: 3,
  });
});

app.get('/sse', async (req, res) => {
  console.error('[MCP-SSE] New incoming SSE client connection...');
  sseTransport = new SSEServerTransport('/messages', res);
  const server = createMcpServer();
  await server.connect(sseTransport);
});

app.post('/messages', async (req, res) => {
  if (!sseTransport) {
    res.status(400).json({ error: 'SSE connection not established' });
    return;
  }
  await sseTransport.handlePostMessage(req, res);
});

app.listen(PORT, () => {
  console.error(`[MCP-SSE] Server listening on http://0.0.0.0:${PORT}`);
});
