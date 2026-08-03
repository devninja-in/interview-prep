# Interview Prep

FAANG-style interview preparation for coding, system design, and AI — a DevNinja product site.

**Live site:** [https://interview-prep.devninja.in/](https://interview-prep.devninja.in/)

## What's inside

1. **Competitive Programming** — patterns from arrays and hashing through graphs, DP, and bit manipulation (Python & Java).
2. **System Design** — fundamentals, building blocks, and case studies (URL shortener, WhatsApp, Instagram, Amazon, S3, YouTube, Uber).
3. **AI Engineering** — LLMs, prompting, RAG, memory, agents, MCP, skills, and designing a full assistant (`content/ai/`).
4. **Interview Labs** — 55 FAANG-frequency questions with why-asked, level expectations, expected arcs, follow-ups, mistakes, and production examples.
5. **Guides** — interview playbook, role learning paths, comparisons, company guides, behavioral/HR, and cheat sheets.

The site uses the **DevNinja** visual system (sky primary, zinc neutrals, system typography) shared with [devninja.in](https://devninja.in/).

## Local preview

```bash
python3 -m http.server 8080
```

Then open `http://localhost:8080` or any file under `chapters/`.

## Regenerate

```bash
pip install pymupdf
python3 scripts/generate_diagrams.py
python3 scripts/build_chapters.py
python3 scripts/assemble_ai_chapters.py
python3 scripts/assemble_interview.py
python3 scripts/assemble_guides.py
```

## Cloudflare Workers

Primary URL: [https://interview-prep.devninja.in/](https://interview-prep.devninja.in/)

- `src/index.js` serves `env.ASSETS`
- Deploy: `npx wrangler deploy`
