/**
 * Server entrypoint.
 *
 * server.ts exports the Hono app only. Bun can serve that default export
 * directly, but this kit's image is node:22, and Node has no built-in fetch
 * server — it needs @hono/node-server. Without this file the Dockerfile's CMD
 * starts a process that binds nothing and exits.
 *
 * Keeping the app and the listener in separate modules also lets the test
 * suite import `app` and drive it with fetch, without ever opening a port.
 */

import { serve } from "@hono/node-server";

import app from "./server.js";

const port = Number(process.env.PORT ?? 8080);

const server = serve({ fetch: app.fetch, port, hostname: "0.0.0.0" }, (info) => {
  console.log(
    JSON.stringify({
      level: "info",
      message: "passkeys server listening",
      port: info.port,
      rpID: process.env.RP_ID ?? "localhost",
    }),
  );
});

// Containers stop with SIGTERM. Without these handlers the process is killed
// after the grace period instead of draining in-flight requests.
for (const signal of ["SIGTERM", "SIGINT"] as const) {
  process.on(signal, () => {
    console.log(JSON.stringify({ level: "info", message: `${signal} received, draining` }));
    server.close(() => process.exit(0));
  });
}
