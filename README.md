# UmarTechTalks — techtalks.itsumarfarooq.com

Official repository for **UmarTechTalks** (`techtalks.itsumarfarooq.com`), a modern static knowledge hub delivering production-grade engineering guides, web application security playbooks, and AI threat defense masterclasses.

- **Author:** Umar Farooq (Senior Full-Stack & Security Engineer)
- **Portfolio & Brand:** [itsumarfarooq.com](https://itsumarfarooq.com)
- **Email:** [contact@itsumarfarooq.com](mailto:contact@itsumarfarooq.com)
- **Company:** [Worldwebtree.com](https://worldwebtree.com)
- **Content Companion Repo:** [github.com/Umar-444/Techtalks-stack-kits](https://github.com/Umar-444/Techtalks-stack-kits)
- **Socials:** [X (@umartechtalks)](https://x.com/umartechtalks) &bull; [LinkedIn](https://linkedin.com/in/umar444) &bull; [GitHub](https://github.com/umar-444)

---

## 1. Architecture & Performance Philosophy

This website is engineered for speed, clean reading, and maximum cite-ability by both human developers and AI answer engines (ChatGPT, Perplexity, Claude, Gemini):

- **Zero JS Frameworks:** Pure semantic HTML5 + vanilla JavaScript (`assets/js/main.js`, ~6 KB) for dark mode, code copying, prompt copying, checklist persistence, and FAQ accordions.
- **Compiled Tailwind CSS:** Pre-compiled and minified into `assets/css/styles.css`. No bloated runtime CDNs. Total page weight under ~150 KB.
- **Answer-Shaped Content:** Definition-first Quick Answer blocks, Threat Models, [INSECURE] vs [SECURE] code blocks, Prompt Templates, and structured FAQs.
- **Machine Discovery (AEO):** `robots.txt` explicitly permitting AI crawlers, `llms.txt` summary file, `llms-full.txt` one-shot full text, and rich JSON-LD schemas (`TechArticle`, `Course`, `FAQPage`, `BreadcrumbList`).

---

## 2. Site Directory Structure

```
techtalks-site/
├── index.html                      # UmarTechTalks hub: hero, tracks, author bio, stats
├── security/
│   ├── index.html                  # Security Masterclass Hub: tracks & curriculum overview
│   └── laravel/
│       ├── index.html              # Track 05: Laravel AI Security landing & syllabus
│       ├── checklist.html          # Interactive, printable 28-point security checklist
│       ├── prompt-injection.html   # Lesson 1: Prompt injection boundary defense
│       ├── llm-api-key-security.html # Lesson 2: API key protection & Redis token budgets
│       ├── rag-tenant-isolation.html # Lesson 3: pgvector scoped multi-tenant retrieval
│       ├── agent-tool-sandboxing.html # Lesson 4: Policy gates & Human-in-the-loop tools
│       ├── pii-redaction.html      # Lesson 5: Reversible PII tokenization (Saudi PDPL)
│       └── model-output-validation.html # Lesson 6: Second-order injection & JSON Schema
├── assets/
│   ├── css/styles.css              # Compiled, minified Tailwind CSS output
│   ├── js/main.js                  # Vanilla JS for theme, copy buttons, checklists
│   └── img/                        # Social preview card (1200x630) & brand assets
├── src/
│   └── input.css                   # Tailwind source with reusable @apply component classes
├── tailwind.config.js              # Tailwind configuration & brand tokens
├── package.json                    # Build script ("build:css")
├── robots.txt                      # AI & search crawler directives
├── sitemap.xml                     # Search engine sitemap
├── llms.txt                        # AI search summary index
├── llms-full.txt                   # Complete lessons concatenated for AI ingestion
├── _headers                        # Cloudflare Pages security & cache headers
├── _redirects                      # Cloudflare Pages clean redirect rules
├── CNAME                           # Custom domain: techtalks.itsumarfarooq.com
└── README.md
```

---

## 3. Local Development & Building CSS

To compile the Tailwind stylesheet:

```bash
# Install dependencies
npm install

# Compile and minify CSS
npm run build:css

# Watch for changes during development
npx tailwindcss -i ./src/input.css -o ./assets/css/styles.css --watch
```

---

## 4. Hosting & Deployment Guide

### Recommended: Cloudflare Pages

1. Push this repository to GitHub (`techtalks-site`).
2. Go to **dash.cloudflare.com** &rarr; **Workers & Pages** &rarr; **Create application** &rarr; **Pages** &rarr; **Connect to Git**.
3. Build Configuration:
   - **Framework preset:** `None`
   - **Build command:** `npm run build:css` (or leave empty if committing compiled CSS)
   - **Build output directory:** `/` (root directory)
4. Go to **Custom domains** &rarr; **Set up a custom domain** &rarr; enter `techtalks.itsumarfarooq.com`.
5. Add the following single DNS record in Namecheap (Advanced DNS for `itsumarfarooq.com`):
   - **Type:** `CNAME`
   - **Host:** `techtalks`
   - **Value:** `techtalks-site.pages.dev` (the hostname Cloudflare provides)
   - **TTL:** `Automatic`

### Fallback: GitHub Pages

1. In repository **Settings** &rarr; **Pages** &rarr; Deploy from branch `main` / `root`.
2. The included `CNAME` file automatically binds `techtalks.itsumarfarooq.com`.
3. Add the CNAME record in Namecheap pointing `techtalks` to `umar-444.github.io`.
4. Tick **Enforce HTTPS** once the SSL certificate issues.

---

## 5. Editorial Standards & Honesty Rules

- **Entity Uniformity:** Umar Farooq is consistently presented as a Senior Full-Stack & Security Engineer with **5+ years** of production experience across all pages, bios, and structured schema markup.
- **Accurate Claims:** Zero fabricated metrics or vanity metrics. All code examples are verified against modern PHP 8.4 and Laravel 13 standards.
- **Independent Entity:** Clearly labeled: *"Not affiliated with Laravel or Taylor Otwell."*
