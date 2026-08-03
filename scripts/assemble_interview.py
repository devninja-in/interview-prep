#!/usr/bin/env python3
"""Assemble Interview Lab chapters and inject drills into topic chapters."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from interview_ai import ai_chapter_drills, ai_lab_body  # noqa: E402
from interview_cp import cp_chapter_drills, cp_lab_body  # noqa: E402
from interview_enrichment import get_enrichment  # noqa: E402
from interview_helpers import wrap_lab  # noqa: E402
from interview_lens import interview_closing, interview_lens  # noqa: E402
from interview_sd import sd_chapter_drills, sd_lab_body  # noqa: E402

CHAPTERS = ROOT / "chapters"
NAV_PATH = ROOT / "assets" / "nav.json"
CSS_LINK = '  <link rel="stylesheet" href="../css/interview.css" />\n'
MARKER_START = "<!-- INTERVIEW_DRILL_START -->"
MARKER_END = "<!-- INTERVIEW_DRILL_END -->"

LABS = [
    {
        "slug": "interview-cp",
        "part": "cp",
        "eyebrow": "Interview Lab · Competitive Programming",
        "title": "Coding interview questions",
        "subtitle": "Twenty FAANG-frequency problems with interviewer intent, level bars, solutions, follow-ups, mistakes, and production examples.",
        "body": cp_lab_body,
        "after": "18-study-plan",
        "nav_title": "Interview Lab: Coding",
        "enrich": "cp",
    },
    {
        "slug": "interview-sd",
        "part": "sd",
        "eyebrow": "Interview Lab · System Design",
        "title": "System design interview questions",
        "subtitle": "Eighteen L4–L6 prompts with why-asked, level expectations, whiteboard steps, and real company examples.",
        "body": sd_lab_body,
        "after": "34-uber",
        "nav_title": "Interview Lab: System Design",
        "enrich": "sd",
    },
    {
        "slug": "interview-ai",
        "part": "ai",
        "eyebrow": "Interview Lab · AI Engineering",
        "title": "AI interview questions",
        "subtitle": "Seventeen AI/ML prompts with interviewer scoring lenses, level bars, and production patterns.",
        "body": ai_lab_body,
        "after": "42-ai-agent",
        "nav_title": "Interview Lab: AI",
        "enrich": "ai",
    },
]


def ensure_interview_css(html: str) -> str:
    if "css/interview.css" in html:
        return html
    return html.replace(
        '  <link rel="stylesheet" href="../css/chapter.css" />\n',
        '  <link rel="stylesheet" href="../css/chapter.css" />\n' + CSS_LINK,
        1,
    )


def inject_drill(path: Path, drill_html: str) -> None:
    text = path.read_text()
    text = ensure_interview_css(text)
    block = f"{MARKER_START}\n{drill_html}\n{MARKER_END}"
    if MARKER_START in text:
        text = re.sub(
            re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
            block,
            text,
            count=1,
            flags=re.S,
        )
    else:
        needle = "</div>\n        <nav class=\"chapter-pager\""
        if needle not in text:
            # fallback: before chapter-pager nav
            text = text.replace(
                '<nav class="chapter-pager"',
                f"{block}\n<nav class=\"chapter-pager\"",
                1,
            )
        else:
            text = text.replace(needle, f"{block}\n</div>\n        <nav class=\"chapter-pager\"", 1)
    path.write_text(text)


def render_sections(sections: list[tuple[str, str]]) -> str:
    parts = []
    for label, content in sections:
        parts.append(f'<div class="qa-label">{label}</div>\n{content}')
    return "\n".join(parts)


def _find_qa_body_span(html: str, body_start: int) -> tuple[int, int] | None:
    """Return [content_start, content_end) for the qa-body that opens at body_start tag."""
    # body_start points at '<div class="qa-body">'
    open_tag_end = html.find(">", body_start) + 1
    depth = 1
    i = open_tag_end
    while i < len(html) and depth:
        next_open = html.find("<div", i)
        next_close = html.find("</div>", i)
        if next_close < 0:
            return None
        if next_open >= 0 and next_open < next_close:
            depth += 1
            i = next_open + 4
        else:
            depth -= 1
            if depth == 0:
                return open_tag_end, next_close
            i = next_close + 6
    return None


def enrich_lab_html(html: str, lab_key: str) -> str:
    """Inject interview-lens sections into each details#qN card."""
    for qnum in range(1, 40):
        data = get_enrichment(lab_key, qnum)
        if not data:
            continue
        marker = f'<details class="qa" id="q{qnum}">'
        dpos = html.find(marker)
        if dpos < 0:
            continue
        bpos = html.find('<div class="qa-body">', dpos)
        if bpos < 0:
            continue
        span = _find_qa_body_span(html, bpos)
        if not span:
            continue
        content_start, content_end = span
        body_inner = html[content_start:content_end]
        if "Why interviewers ask this" in body_inner:
            continue
        opening = render_sections(
            interview_lens(
                why=data["why"],
                evaluating=data["evaluating"],
                levels=data.get("levels"),
                expected=data.get("expected"),
                reading_mins=data.get("reading_mins"),
            )
        )
        closing = render_sections(
            interview_closing(
                followups=data.get("followups"),
                mistakes=data.get("mistakes"),
                production=data.get("production"),
            )
        )
        if '<p class="qa-meta">' in body_inner:
            body_inner = re.sub(
                r'(<p class="qa-meta">.*?</p>)',
                r"\1\n" + opening,
                body_inner,
                count=1,
                flags=re.S,
            )
        else:
            body_inner = opening + "\n" + body_inner
        body_inner = body_inner.rstrip() + "\n" + closing
        html = html[:content_start] + body_inner + html[content_end:]
    return html


def write_labs() -> None:
    for lab in LABS:
        body = enrich_lab_html(lab["body"](), lab["enrich"])
        html = wrap_lab(
            slug=lab["slug"],
            part=lab["part"],
            eyebrow=lab["eyebrow"],
            title=lab["title"],
            subtitle=lab["subtitle"],
            body=body,
        )
        out = CHAPTERS / f"{lab['slug']}.html"
        out.write_text(html)
        words = len(re.sub(r"<[^>]+>", " ", html).split())
        print(f"wrote {out.name} (~{words} words)")


def inject_all_drills() -> None:
    mapping: dict[str, str] = {}
    mapping.update(cp_chapter_drills())
    mapping.update(sd_chapter_drills())
    mapping.update(ai_chapter_drills())
    for slug, drill in mapping.items():
        path = CHAPTERS / f"{slug}.html"
        if not path.exists():
            print(f"skip missing chapter {slug}")
            continue
        inject_drill(path, drill)
        print(f"injected drill into {slug}")


def update_nav() -> None:
    data = json.loads(NAV_PATH.read_text())
    chapters = data["chapters"]
    # Remove prior lab entries if re-running
    chapters = [c for c in chapters if not str(c["id"]).startswith("interview-")]
    by_id = {c["id"]: i for i, c in enumerate(chapters)}
    for lab in LABS:
        entry = {
            "id": lab["slug"],
            "num": None,
            "title": lab["nav_title"],
            "part": lab["part"],
            "href": f"chapters/{lab['slug']}.html",
            "lab": True,
        }
        after = lab["after"]
        if after in by_id:
            insert_at = by_id[after] + 1
        else:
            insert_at = len(chapters)
        chapters.insert(insert_at, entry)
        # refresh indices
        by_id = {c["id"]: i for i, c in enumerate(chapters)}
    data["chapters"] = chapters
    NAV_PATH.write_text(json.dumps(data, indent=2) + "\n")
    print(f"updated nav.json ({len(chapters)} entries)")


def patch_builders_for_css() -> None:
    """Ensure rebuild scripts keep linking interview.css when present."""
    ai = ROOT / "scripts" / "assemble_ai_chapters.py"
    text = ai.read_text()
    if "interview.css" not in text:
        text = text.replace(
            '  <link rel="stylesheet" href="../css/chapter.css" />\n</head>',
            '  <link rel="stylesheet" href="../css/chapter.css" />\n'
            '  <link rel="stylesheet" href="../css/interview.css" />\n</head>',
        )
        ai.write_text(text)
        print("patched assemble_ai_chapters.py for interview.css")

    build = ROOT / "scripts" / "build_chapters.py"
    btext = build.read_text()
    if "interview.css" not in btext:
        btext = btext.replace(
            '  <link rel="stylesheet" href="../css/chapter.css" />\n',
            '  <link rel="stylesheet" href="../css/chapter.css" />\n'
            '  <link rel="stylesheet" href="../css/interview.css" />\n',
            1,
        )
        build.write_text(btext)
        print("patched build_chapters.py for interview.css")


def main() -> None:
    write_labs()
    inject_all_drills()
    update_nav()
    patch_builders_for_css()


if __name__ == "__main__":
    main()
