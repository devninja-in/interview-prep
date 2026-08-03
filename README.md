# Interview Prep

Coding, system design, and AI in one place — published as a real HTML book.

**Live site:** [https://interview-prep.devninja.in/](https://interview-prep.devninja.in/)

## What's inside

1. **Competitive Programming** — patterns from arrays and hashing through graphs, DP, and bit manipulation (Python & Java).
2. **System Design** — fundamentals, building blocks, and case studies (URL shortener, WhatsApp, Instagram, Amazon, S3, YouTube, Uber).
3. **AI Engineering** — LLMs, prompting, RAG, memory, agents, MCP, skills, and designing an AI assistant.

Chapters are normal web pages (selectable text + code blocks). Diagrams are images only where the book used a figure — not full-page PDF screenshots.

## Local preview

```bash
python3 -m http.server 8080
```

Then open `http://localhost:8080` or any file under `chapters/`.

## Regenerate chapters from the PDF

```bash
pip install pymupdf
python3 scripts/build_chapters.py
```

## Cloudflare Workers

Primary URL: [https://interview-prep.devninja.in/](https://interview-prep.devninja.in/)

- `src/index.js` serves `env.ASSETS`
- `.assetsignore` excludes `.git`
- Deploy command: `npx wrangler deploy`

## Files

| Path | Purpose |
|------|---------|
| `index.html` | Landing page & table of contents |
| `chapters/` | HTML chapters (text, code, embedded diagrams) |
| `assets/diagrams/` | Diagram images only |
| `assets/interview-prep.pdf` | Original PDF |
| `assets/nav.json` | Chapter navigation |
| `read.html` | Redirects into the chapter reader |

## Keyboard (reader)

- `←` / `→` — previous / next chapter
- `Esc` — close mobile contents
