# Interview Prep

Coding, system design, and AI in one place — published as a static book for GitHub Pages.

**Live site:** [https://devninja-in.github.io/interview-prep/](https://devninja-in.github.io/interview-prep/)

## What's inside

1. **Competitive Programming** — patterns from arrays and hashing through graphs, DP, and bit manipulation (Python & Java).
2. **System Design** — fundamentals, building blocks, and case studies (URL shortener, WhatsApp, Instagram, Amazon, S3, YouTube, Uber).
3. **AI Engineering** — LLMs, prompting, RAG, memory, agents, MCP, skills, and designing an AI assistant.

## Local preview

Open `index.html` in a browser, or serve the repo root:

```bash
python3 -m http.server 8080
```

Then visit `http://localhost:8080`.

## Cloudflare deploy

This repo includes `wrangler.jsonc` and `.assetsignore` so Workers Static Assets do **not** upload `.git` (which exceeds the 25 MiB file limit).

In Cloudflare, use:
- **Framework preset:** None / Static
- **Build command:** leave empty (or `echo "static site"`)
- **Deploy / output directory:** `.` (repo root)
- Ensure the committed `wrangler.jsonc` is used (do not let setup recreate assets as the full git checkout without `.assetsignore`)

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
