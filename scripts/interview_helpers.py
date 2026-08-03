#!/usr/bin/env python3
"""Shared HTML helpers for interview Q&A rendering."""
from __future__ import annotations

import html


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def code_block(lang: str, code: str) -> str:
    lang_u = lang.upper()
    safe = html.escape(code.rstrip() + "\n")
    return (
        f'<div class="code-block"><div class="code-lang">{lang_u}</div>'
        f'<pre class="code"><code class="language-{lang.lower()}">{safe}</code></pre></div>'
    )


def figure_diagram(name: str, alt: str) -> str:
    return (
        f'<figure class="diagram native qa-diagram">'
        f'<img src="../assets/diagrams/{html.escape(name)}.svg" alt="{esc(alt)}" loading="lazy" />'
        f"</figure>"
    )


def steps(items: list[str]) -> str:
    """Numbered whiteboard steps; items may include safe HTML."""
    return '<ol class="qa-steps">' + "".join(f"<li>{item}</li>" for item in items) + "</ol>"


def bullets(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"


def callout(title: str, body: str) -> str:
    return (
        f'<aside class="qa-callout"><div class="qa-label">{esc(title)}</div>'
        f"{body}</aside>"
    )


def qa_block(
    *,
    qnum: int,
    title: str,
    asked: str,
    difficulty: str,
    pattern: str,
    prompt: str,
    sections: list[tuple[str, str]],
) -> str:
    """sections: list of (label, html_body)."""
    meta = (
        f'<p class="qa-meta"><strong>Asked at:</strong> {esc(asked)} · '
        f'<strong>Difficulty:</strong> {esc(difficulty)} · '
        f'<strong>Pattern:</strong> {esc(pattern)}</p>'
    )
    body_parts = [f"<p>{esc(prompt)}</p>", meta]
    for label, content in sections:
        body_parts.append(f'<div class="qa-label">{esc(label)}</div>')
        body_parts.append(content)
    inner = "\n".join(body_parts)
    return f"""<details class="qa">
<summary><span>Q{qnum}. {esc(title)}</span></summary>
<div class="qa-body">
{inner}
</div>
</details>"""


def drill_section(title: str, intro: str, items: list[str], lab_href: str | None = None) -> str:
    lab = (
        f'<p class="drill-intro">More drills in the <a href="{lab_href}">Interview Lab</a>.</p>'
        if lab_href
        else ""
    )
    return f"""<section class="interview-drill" id="interview-drill">
<h2>{esc(title)}</h2>
<p class="drill-intro">{intro}</p>
{lab}
{"".join(items)}
</section>"""


CHAPTER_SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{heading} — Interview Prep</title>
  <meta name="description" content="{desc}" />
  <link rel="stylesheet" href="../css/styles.css" />
  <link rel="stylesheet" href="../css/chapter.css" />
  <link rel="stylesheet" href="../css/interview.css" />
</head>
<body class="chapter-page" data-chapter="{slug}" data-part="{part}">
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
        <p class="part-eyebrow">{eyebrow}</p>
        <header class="chapter-hero">
{num_html}<h1>{title}</h1>
<p class="lab-hero-note">{subtitle}</p>
</header>
<div class="chapter-body">
{body}
</div>
        <nav class="chapter-pager" id="chapter-pager" aria-label="Chapter pagination"></nav>
      </article>
    </main>
  </div>
  <script src="../js/nav.js"></script>
  <script src="../js/progress.js"></script>
</body>
</html>
"""


def wrap_lab(
    *,
    slug: str,
    part: str,
    eyebrow: str,
    title: str,
    subtitle: str,
    body: str,
    num: str | None = None,
) -> str:
    heading = f"{num} · {title}" if num else title
    num_html = f'<p class="chapter-num">Chapter {esc(num)}</p>\n' if num else ""
    return CHAPTER_SHELL.format(
        heading=esc(heading),
        desc=esc(f"{heading} — interview questions and deep solutions"),
        slug=esc(slug),
        part=esc(part),
        eyebrow=esc(eyebrow),
        num_html=num_html,
        title=esc(title),
        subtitle=esc(subtitle),
        body=body.strip(),
    )
