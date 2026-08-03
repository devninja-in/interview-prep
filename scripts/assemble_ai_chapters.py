#!/usr/bin/env python3
"""Assemble deep AI chapter HTML from content/ai/*.html bodies."""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content" / "ai"
OUT = ROOT / "chapters"
NAV = {c["id"]: c for c in json.loads((ROOT / "assets" / "nav.json").read_text())["chapters"]}

META = {
    "part-ai": (None, "Part Three: AI Engineering"),
    "35-llms": ("35", "How LLMs work"),
    "36-prompting": ("36", "Prompting patterns"),
    "37-rag": ("37", "RAG"),
    "38-memory": ("38", "Memory"),
    "39-agents": ("39", "Agentic patterns"),
    "40-mcp": ("40", "MCP"),
    "41-skills": ("41", "Skills"),
    "42-ai-agent": ("42", "Design: an AI agent"),
}


def wrap(slug: str, num: str | None, title: str, body: str) -> str:
    heading = f"{num} · {title}" if num else title
    num_html = f'<p class="chapter-num">Chapter {html.escape(num)}</p>\n' if num else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(heading)} — Interview Prep</title>
  <meta name="description" content="{html.escape(heading)} — deep AI engineering guide for interviews" />
<link rel="stylesheet" href="../css/styles.css" />
  <link rel="stylesheet" href="../css/chapter.css" />
  <link rel="stylesheet" href="../css/interview.css" />
</head>
<body class="chapter-page" data-chapter="{html.escape(slug)}" data-part="ai">
  <a class="skip-link" href="#content">Skip to content</a>
  <div class="chapter-shell">
    <aside class="sidebar" id="sidebar" aria-label="Table of contents"></aside>
    <div class="sidebar-backdrop" id="sidebar-backdrop" hidden></div>
    <main class="chapter-main" id="content">
      <div class="chapter-toolbar">
        <button class="icon-btn menu-toggle" id="menu-toggle" type="button" aria-label="Open contents">☰</button>
        <a class="brand" href="../">Interview Prep <span>DevNinja</span></a>
        <div class="toolbar-spacer"></div>
        <a class="btn btn-ghost btn-small" href="../">Home</a>
      </div>
      <article class="chapter-article">
        <p class="part-eyebrow">AI Engineering</p>
        <header class="chapter-hero">
{num_html}<h1>{html.escape(title)}</h1>
</header>
<div class="chapter-body">
{body.strip()}
</div>
        <nav class="chapter-pager" id="chapter-pager" aria-label="Chapter pagination"></nav>
      </article>
    </main>
  </div>
  <script src="../js/nav.js"></script>
</body>
</html>
"""


def main() -> None:
    for slug, (num, title) in META.items():
        body_path = CONTENT / f"{slug}.html"
        body = body_path.read_text()
        (OUT / f"{slug}.html").write_text(wrap(slug, num, title, body))
        words = len(body.split())
        print(f"wrote {slug}.html ({words} words in body)")
    # Re-apply interview drills / CSS after regenerating AI shells.
    try:
        from assemble_interview import inject_all_drills, write_labs

        write_labs()
        inject_all_drills()
    except Exception as exc:  # pragma: no cover
        print(f"note: could not re-apply interview drills: {exc}")


if __name__ == "__main__":
    main()
