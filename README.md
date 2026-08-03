# Interview Prep

Coding, system design, and AI in one place — published as a real HTML book.

**Live site:** [https://interview-prep.devninja.in/](https://interview-prep.devninja.in/)

## What's inside

1. **Competitive Programming** — patterns from arrays and hashing through graphs, DP, and bit manipulation (Python & Java).
2. **System Design** — fundamentals, building blocks, and case studies (URL shortener, WhatsApp, Instagram, Amazon, S3, YouTube, Uber).
3. **AI Engineering** — a deep story-driven path: LLMs, prompting, RAG, memory, agents, MCP, skills, and designing a full assistant (`content/ai/`).

Chapters are normal web pages (selectable text + code blocks). Topic diagrams are freshly drawn SVGs — not PDF page screenshots.

## Local preview

```bash
python3 -m http.server 8080
```

Then open `http://localhost:8080` or any file under `chapters/`.

## Regenerate from the PDF / diagrams

```bash
pip install pymupdf
python3 scripts/generate_diagrams.py   # native SVG topic diagrams
python3 scripts/build_chapters.py      # HTML chapters from PDF (skips hand-authored AI)
python3 scripts/assemble_ai_chapters.py  # deep AI section from content/ai/
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
