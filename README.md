# Interview Prep

Coding, system design, and AI in one place — published as a static book.

**Cloudflare Worker:** [https://interview-prep.devninja.workers.dev/](https://interview-prep.devninja.workers.dev/)  
**GitHub Pages:** [https://devninja-in.github.io/interview-prep/](https://devninja-in.github.io/interview-prep/)

## What's inside

1. **Competitive Programming** — patterns from arrays and hashing through graphs, DP, and bit manipulation (Python & Java).
2. **System Design** — fundamentals, building blocks, and case studies (URL shortener, WhatsApp, Instagram, Amazon, S3, YouTube, Uber).
3. **AI Engineering** — LLMs, prompting, RAG, memory, agents, MCP, skills, and designing an AI assistant.

## Local preview

```bash
python3 -m http.server 8080
# or
npm run build && npx wrangler dev
```

## Cloudflare Workers deploy

This project deploys as a **Worker with Static Assets** (not classic Pages).

### Required build settings (Workers → Settings → Builds)

| Setting | Value |
|---------|--------|
| Git branch | `main` |
| Build command | `npm run build` (or leave empty) |
| Deploy command | `npm run deploy` |
| Root directory | `/` |

`npm run deploy` runs `npm run build && wrangler deploy`, so `dist/` is always fresh and `.git` is never uploaded.
### What the build does

1. `npm run build` copies the site into `dist/` (no `.git`)
2. `wrangler deploy` publishes `src/index.js` + `dist/` assets
3. The Worker serves assets via `env.ASSETS.fetch()` (replaces any Hello World stub)

Files: `wrangler.jsonc`, `src/index.js`, `scripts/build.mjs`, `.assetsignore`

**Deploy trigger:** 2026-08-03 Cloudflare dist fix

## Files

| Path | Purpose |
|------|---------|
| `index.html` | Landing page & table of contents |
| `read.html` | Full-book reader (all 212 pages + diagrams) |
| `assets/pages/` | Rendered page images from the PDF |
| `assets/diagrams/` | Highlighted diagram pages |
| `assets/interview-prep.pdf` | Original PDF |
| `assets/book-data.json` | Chapter map for navigation |
| `dist/` | Build output for Cloudflare (generated) |

## Keyboard (reader)

- `←` / `→` or `k` / `j` — previous / next page
- `Esc` — close mobile contents
