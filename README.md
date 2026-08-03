# Interview Prep

Coding, system design, and AI in one place — published as a static book.

**Live site:** [https://interview-prep.devninja.in/](https://interview-prep.devninja.in/)  
**GitHub Pages:** [https://devninja-in.github.io/interview-prep/](https://devninja-in.github.io/interview-prep/)

## What's inside

1. **Competitive Programming** — patterns from arrays and hashing through graphs, DP, and bit manipulation (Python & Java).
2. **System Design** — fundamentals, building blocks, and case studies (URL shortener, WhatsApp, Instagram, Amazon, S3, YouTube, Uber).
3. **AI Engineering** — LLMs, prompting, RAG, memory, agents, MCP, skills, and designing an AI assistant.

## Local preview

```bash
python3 -m http.server 8080
```

## Cloudflare Workers

Primary URL: [https://interview-prep.devninja.in/](https://interview-prep.devninja.in/)

Deployed as a **Worker + Static Assets** (`wrangler.jsonc`).

- `src/index.js` serves `env.ASSETS` (replaces the default Hello World Worker)
- `.assetsignore` excludes `.git` so deploys stay under the 25 MiB file limit
- Dashboard build command can stay empty; deploy command: `npx wrangler deploy`

## Files

| Path | Purpose |
|------|---------|
| `index.html` | Landing page & table of contents |
| `read.html` | Full-book reader (all 212 pages + diagrams) |
| `assets/pages/` | Rendered page images from the PDF |
| `assets/diagrams/` | Highlighted diagram pages |
| `assets/interview-prep.pdf` | Original PDF |
| `assets/book-data.json` | Chapter map for navigation |

## Keyboard (reader)

- `←` / `→` or `k` / `j` — previous / next page
- `Esc` — close mobile contents
