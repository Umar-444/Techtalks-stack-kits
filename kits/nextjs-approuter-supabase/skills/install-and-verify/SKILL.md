---
name: install-and-verify
description: Install, configure, and verify the Next.js 15 + Supabase + shadcn/ui fullstack application.
---

# Install & Verify Skill: Next.js + Supabase

## Prerequisites
- Node.js 20+ (LTS) & npm 10+
- Docker Engine 24+ (if running Supabase CLI locally)
- A Supabase project URL and anon public API key

## OS-Specific Commands

### Linux / macOS
```bash
cp .env.example .env.local
npm install
npm run build
npm run dev
```

### Windows (PowerShell)
```powershell
Copy-Item .env.example .env.local
npm install
npm run build
npm run dev
```

## Docker Compose Alternative
```bash
docker compose up --build -d
```

## Post-Install Verification Probes
1. Verify Next.js compilation:
   ```bash
   npm run build
   ```
   Expected: Generates `.next/` directory with static and dynamic App Router routes, zero TypeScript errors.

2. Verify health check API route:
   ```bash
   curl -s http://localhost:3000/api/healthz
   ```
   Expected: `{"status":"ok","app":"nextjs-approuter-supabase","version":"1.0.0"}` with HTTP 200 OK.

3. Verify dashboard interface:
   ```bash
   curl -s http://localhost:3000/ | grep "Next.js 15"
   ```
   Expected: Matches rendered Server Component dashboard HTML.

## Failure-Recovery Matrix
| Symptom | Probable Cause | Resolution |
| :--- | :--- | :--- |
| `Error: Your project's URL and Key are required to create a Supabase client!` | Missing `.env.local` configuration | Copy `.env.example` to `.env.local` and define `NEXT_PUBLIC_SUPABASE_URL` |
| `new row violates row-level security policy for table "items"` | Missing authenticated session or invalid user_id | Authenticate user via Supabase Auth or ensure policy grants INSERT |
| `TypeError: Cannot read properties of undefined (reading 'headers')` | Using client Supabase instance in Server Component | Import server client from `@/lib/supabase/server` instead |
| `Failed to compile: Type error in Server Action` | Mismatched FormData or Zod schema types | Ensure action schema parses `formData.get(...)` strictly |
| `Hydration failed because the initial UI does not match` | Non-deterministic client renders (e.g. `Date.now()`) | Wrap dynamic time or random values in `useEffect` or pass from server |
| `Port 3000 is already in use` | Existing local dev process | Run on another port: `npm run dev -- -p 3001` |

## Done Means
The application compiles cleanly with TypeScript, `/api/healthz` returns HTTP 200 OK, and Server Actions successfully mutate Supabase tables with RLS enforcement.
