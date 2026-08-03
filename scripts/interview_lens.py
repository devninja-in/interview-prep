#!/usr/bin/env python3
"""Interview-perspective helpers: why asked, levels, mistakes, production examples."""
from __future__ import annotations

import html
from typing import Any

from interview_helpers import bullets, callout, esc


def level_table(rows: dict[str, str]) -> str:
    """rows keys: Junior, Mid, Senior, Staff, Principal (any subset)."""
    order = ["Junior", "Mid", "Senior", "Staff", "Principal"]
    body = []
    for level in order:
        if level not in rows:
            continue
        body.append(
            f"<tr><th scope=\"row\">{esc(level)}</th><td>{rows[level]}</td></tr>"
        )
    if not body:
        return ""
    return (
        '<div class="table-wrap level-table"><table>'
        "<caption>What interviewers expect by level</caption>"
        "<thead><tr><th>Level</th><th>Expectation</th></tr></thead>"
        f"<tbody>{''.join(body)}</tbody></table></div>"
    )


def interview_lens(
    *,
    why: str,
    evaluating: list[str],
    levels: dict[str, str] | None = None,
    expected: str | None = None,
    followups: list[str] | None = None,
    mistakes: list[str] | None = None,
    production: list[str] | None = None,
    next_topics: list[tuple[str, str]] | None = None,
    reading_mins: int | None = None,
) -> list[tuple[str, str]]:
    """Standard interview-perspective sections to prepend/append to a Q&A."""
    sections: list[tuple[str, str]] = []
    meta_bits = []
    if reading_mins:
        meta_bits.append(f"~{reading_mins} min to rehearse aloud")
    header = ""
    if meta_bits:
        header = f'<p class="qa-meta">{esc(" · ".join(meta_bits))}</p>'

    sections.append(
        (
            "Why interviewers ask this",
            header + f"<p>{why}</p>",
        )
    )
    sections.append(
        (
            "What they are evaluating",
            bullets(evaluating),
        )
    )
    if levels:
        sections.append(("Level expectations", level_table(levels)))
    if expected:
        sections.append(
            (
                "Expected answer shape",
                callout("Hit this arc", f"<p>{expected}</p>"),
            )
        )
    # Core solution sections are inserted by the caller between expected and followups
    return sections


def interview_closing(
    *,
    followups: list[str] | None = None,
    mistakes: list[str] | None = None,
    production: list[str] | None = None,
    next_topics: list[tuple[str, str]] | None = None,
) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    if followups:
        sections.append(("Follow-up questions", bullets(followups)))
    if mistakes:
        sections.append(
            (
                "Common mistakes",
                callout("Avoid these", bullets(mistakes)),
            )
        )
    if production:
        sections.append(
            (
                "Real-world production examples",
                bullets(production),
            )
        )
    if next_topics:
        links = "".join(
            f'<li><a href="{html.escape(href)}">{esc(label)}</a></li>'
            for label, href in next_topics
        )
        sections.append(("What to learn next", f"<ul class=\"next-topics\">{links}</ul>"))
    return sections


def page_meta_bar(
    *,
    difficulty: str,
    reading_mins: int,
    master_hours: str,
    level_focus: str,
) -> str:
    return f"""<div class="page-meta-bar" role="group" aria-label="Topic meta">
  <span><strong>Difficulty</strong> {esc(difficulty)}</span>
  <span><strong>Read</strong> ~{reading_mins} min</span>
  <span><strong>Master</strong> {esc(master_hours)}</span>
  <span><strong>Levels</strong> {esc(level_focus)}</span>
</div>"""


def prerequisites(items: list[str]) -> str:
    return (
        '<aside class="learn-box"><div class="qa-label">Prerequisites</div>'
        + bullets(items)
        + "</aside>"
    )


def what_next(items: list[tuple[str, str]]) -> str:
    links = "".join(
        f'<li><a href="{html.escape(href)}">{esc(label)}</a></li>' for label, href in items
    )
    return (
        '<aside class="learn-box learn-box-next"><div class="qa-label">What to learn next</div>'
        f"<ul>{links}</ul></aside>"
    )


def guide_shell(
    *,
    slug: str,
    part: str,
    eyebrow: str,
    title: str,
    subtitle: str,
    body: str,
    description: str | None = None,
) -> str:
    from interview_helpers import CHAPTER_SHELL, esc as e

    return CHAPTER_SHELL.format(
        heading=e(title),
        desc=e(description or f"{title} — Interview Prep"),
        slug=e(slug),
        part=e(part),
        eyebrow=e(eyebrow),
        num_html="",
        title=e(title),
        subtitle=e(subtitle),
        body=body.strip(),
    )
