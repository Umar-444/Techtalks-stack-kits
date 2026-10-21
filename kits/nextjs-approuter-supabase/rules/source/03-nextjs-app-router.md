---
title: "Next.js App Router & Caching"
description: "React Server Components, revalidation, and streaming."
globs: ["app/**/*.tsx", "app/**/*.ts"]
---

# Next.js App Router & Caching

1. **Server Components by Default:**
   - Keep components as Server Components unless interactivity (`useState`, `useEffect`) is needed.
   - Use `'use client'` only at the leaves of the component tree.
