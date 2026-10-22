# Next.js 15+ + Supabase + shadcn/ui Stack Kit

[![Stack Status: Ready to Ship](https://img.shields.io/badge/status-Ready%20to%20Ship-emerald?style=flat-square)](kit.yaml)
[![TypeScript 5.5+](https://img.shields.io/badge/typescript-5.5%2B-blue?style=flat-square)](https://www.typescriptlang.org/)
[![Next.js 15](https://img.shields.io/badge/next.js-15-black?style=flat-square)](https://nextjs.org/)
[![React 19](https://img.shields.io/badge/react-19-61DAFB?style=flat-square)](https://react.dev/)
[![Supabase](https://img.shields.io/badge/supabase-postgres%2016-3ECF8E?style=flat-square)](https://supabase.com/)

Production fullstack React 19 / Next.js 15 App Router kit featuring Server Actions with Zod validation, Supabase Row-Level Security (RLS), and shadcn/ui design system tokens.

---

## Architecture Overview

```
                   +-----------------------------------+
                   |         Browser / Client          |
                   +-----------------+-----------------+
                                     |
                       HTTP / Server Action Mutation
                                     v
                   +-----------------+-----------------+
                   |     Next.js 15 App Router Core    |
                   |  - React 19 Server Components     |
                   |  - Zod Input Schema Validation    |
                   |  - revalidatePath() Cache Sync    |
                   +-----------------+-----------------+
                                     |
                                     v
                   +-----------------+-----------------+
                   |       Supabase SSR Client         |
                   |  - HttpOnly Cookie Sessions       |
                   |  - Middleware Token Refresh       |
                   +-----------------+-----------------+
                                     |
                                     v
                   +-----------------+-----------------+
                   |       Supabase PostgreSQL 16      |
                   |  - Row Level Security (RLS)       |
                   |  - auth.uid() = user_id Policies  |
                   |  - UUID Primary Keys              |
                   +-----------------------------------+
```

---

## Section 3: Installation Guide

### 1. Prerequisites Table
| Tool | Minimum Version | Check Command | Where to Get |
| :--- | :--- | :--- | :--- |
| Node.js | 20.0+ (LTS) | `node -v` | [nodejs.org](https://nodejs.org/) |
| npm | 10.0+ | `npm -v` | Bundled with Node.js |
| Docker Engine | 24.0+ (optional) | `docker --version` | [docker.com](https://www.docker.com/) |
| Supabase CLI | 1.190+ (optional) | `supabase --version` | [supabase.com/docs](https://supabase.com/docs) |

### 2. Quickstart Execution
```bash
git clone https://github.com/Umar-444/Techtalks-stack-kits.git
cd Techtalks-stack-kits/kits/nextjs-approuter-supabase/starter
cp .env.example .env.local
npm install
npm run build
npm run dev
```
- Interactive UI: [http://localhost:3000/](http://localhost:3000/)
- Health Check Probe: [http://localhost:3000/api/healthz](http://localhost:3000/api/healthz)

### 3. Environment Variables
| Variable | Purpose | Example Placeholder |
| :--- | :--- | :--- |
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase API Gateway URL | `https://your-project.supabase.co` |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Public anonymous API key | `eyJhbGciOiJIUzI1NiIsIn...` |
| `SUPABASE_SERVICE_ROLE_KEY` | Admin secret key (Server-only) | `your-service-role-key-never-expose` |

### 4. Per-Agent Setup
- **Claude Code**: Rules loaded from `CLAUDE.md`.
- **Cursor**: Granular `.mdc` rules auto-applied via `.cursor/rules/*.mdc`.
- **Codex / AGENTS.md**: Contextual instructions in `CODEX.md` and `AGENTS.md`.
- **Copilot**: Global instructions auto-loaded from `.github/copilot-instructions.md`.
- **Cline**: System prompts injected via `.clinerules`.
- **Antigravity**: Workspace rules discovered under `.agents/rules/*.md`.

### 5. Verification Probes
```bash
npm run build
curl -s http://localhost:3000/api/healthz
curl -s http://localhost:3000/ | grep "Next.js 15"
```

### 6. Troubleshooting Matrix
| Symptom | Probable Cause | Fix |
| :--- | :--- | :--- |
| `Your project's URL and Key are required` | Missing `.env.local` | Define `NEXT_PUBLIC_SUPABASE_URL` in `.env.local` |
| `new row violates row-level security policy` | Missing authenticated user session | Sign in or verify RLS INSERT policy matches user |
| `TypeError: Cannot read properties of headers` | Client instance used in Server Component | Use `createClient()` from `@/lib/supabase/server` |
| `Type error in Server Action` | Invalid FormData schema | Ensure Zod schema matches `formData.get(...)` |
| `Hydration failed because initial UI does not match` | Non-deterministic client renders | Use `useEffect` or compute values on server |

### 7. Updating the Kit
When updating:
- Do not overwrite `.env.local`, components in `src/components/`, or actions in `src/app/actions.ts`.
- Merge updates to `rules/` and `skills/`.

---

## Section 4: Frequently Asked Questions (FAQ)

### 1. What exactly is this kit, and what do I get when I clone it?
This kit is a production-ready fullstack React 19 and Next.js 15 App Router platform integrated with Supabase and shadcn/ui. You get a pre-wired Docker Compose container setup, 6 AI agent rule dialects, 5 operational skills, automated TypeScript checks, and a runnable Task management module.

### 2. Which versions does it pin, and why those?
It pins TypeScript 5.5+, Next.js 15, React 19, and Supabase / PostgreSQL 16. These versions deliver asynchronous Request APIs, Server Actions with automatic revalidation, and native PostgreSQL Row Level Security.

### 3. Which AI coding agents are supported, and how do the rules reach each one?
Claude Code, Cursor, Codex, GitHub Copilot, Cline, and Antigravity are supported via transpiled native dialect targets generated from canonical source rules.

### 4. What do I need installed before I start?
You only need Node.js 20+ (LTS) and npm 10+, or Docker Engine 24+ if running via Docker Compose.

### 5. How long does installation take, honestly, and what can slow it down?
A fresh install takes between 30 to 60 seconds on a standard broadband connection. Primary bottleneck is pulling npm dependencies.

### 6. Is the starter production-shaped or a demo? What must I change before real production?
The starter is production-shaped with strict security defaults. Before production release, link your real Supabase project credentials in .env.local, apply migrations, and verify RLS policies.

### 7. How is security handled in this kit, and where are its checks?
Security is enforced at multiple layers: database-level PostgreSQL Row Level Security, Zod Server Action input validation, HttpOnly SSR cookies, and automated secret scanning. The complete 12-control suite is in security/checks.json.

### 8. Can I change the design? Where do the design tokens live?
Yes. Design tokens are documented in DESIGN.md. You can customize Tailwind CSS classes and shadcn/ui component tokens directly in layout.tsx and components/.

### 9. How do I update when a new kit version releases?
Review CHANGELOG.md and merge updates to rules/ and skills/. Project-specific Server Actions, pages, and .env.local settings remain untouched.

### 10. Can I use it for commercial and client work?
Yes. The entire kit is licensed under the permissive MIT License with zero royalties.

### 11. How do I contribute a fix or a skill back?
Submit a PR to https://github.com/Umar-444/Techtalks-stack-kits adhering to the 18-checkpoint completeness standard.

### 12. Where do I get help or report a problem?
Open an issue on the repository or participate in community discussions at https://techtalks.itsumarfarooq.com.

### 13. How does Supabase Row Level Security protect user data?
PostgreSQL enforces RLS policies directly in the database engine using auth.uid() = user_id. Even if an attacker tampers with client-side query parameters, the database refuses to return or mutate cross-tenant records.

### 14. Why use Server Actions instead of API Route Handlers?
Server Actions eliminate client-side API boilerplate, provide seamless type safety from database to form, and automatically trigger cache revalidation via revalidatePath().

---

## License
Maintained by **Umar Farooq** under the MIT License.
