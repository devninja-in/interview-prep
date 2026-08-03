#!/usr/bin/env python3
"""Convert Interview Prep PDF into real HTML chapters (selectable text + code + diagrams)."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "assets" / "interview-prep.pdf"
OUT_CH = ROOT / "chapters"
OUT_DIAG = ROOT / "assets" / "diagrams"
BOOK_DATA = ROOT / "assets" / "book-data.json"

OUT_CH.mkdir(exist_ok=True)
OUT_DIAG.mkdir(parents=True, exist_ok=True)

doc = fitz.open(PDF)
data = json.loads(BOOK_DATA.read_text())
chapters = data["chapters"]
diagram_pages = {p["page"] for p in data["pages"] if p.get("is_diagram")}

CODE_LANGS = {"PYTHON", "JAVA", "SKILL.MD", "MCP SERVER"}
INDENT_UNIT = 24.6
CODE_BASE_X = 58.0


def spaced_caps(s: str) -> bool:
    return bool(re.fullmatch(r"(?:[A-Z0-9]\s+){2,}[A-Z0-9]", s.strip()))


def is_code_lang(s: str) -> bool:
    return s.strip() in CODE_LANGS


def looks_like_code(text: str, x0: float | None = None) -> bool:
    s = text.rstrip()
    if not s.strip():
        return True
    if x0 is not None and x0 >= CODE_BASE_X + INDENT_UNIT * 0.6:
        return True
    if re.match(
        r"^(def |class |import |from |return |if |for |while |else:|elif |try:|except|with |#|//|/\*|int |boolean |void |Map|Deque|List|public |private |static |new |@|function )",
        s,
    ):
        return True
    if any(tok in s for tok in ["{", "}", "();", "=>", ":=", "&&", "||", "[]{"]):
        return True
    if re.search(r"\w+\(.*\)", s) and (";" in s or s.endswith(":") or s.endswith("{") or s.endswith(")")):
        return True
    return False


def page_is_diagram(page_num: int, text: str, drawings: int) -> bool:
    if page_num in diagram_pages:
        return True
    body = re.sub(r"\s+", " ", text).strip()
    if drawings >= 40 and len(body) < 900:
        return True
    if drawings >= 28 and any(k in text for k in ("STEP BY STEP", "Clients", "Write path", "Producer")):
        return True
    return False


def render_diagram(page_num: int) -> str:
    page = doc[page_num - 1]
    pix = page.get_pixmap(matrix=fitz.Matrix(1.8, 1.8), alpha=False)
    fname = f"diagram-p{page_num:03d}.jpg"
    pix.save(str(OUT_DIAG / fname), jpg_quality=85)
    return f"assets/diagrams/{fname}"


def extract_lines(page_num: int) -> list[dict]:
    """Return reading-order lines with text + x0."""
    page = doc[page_num - 1]
    rows: list[dict] = []
    for block in page.get_text("dict")["blocks"]:
        if block.get("type") != 0:
            continue
        for line in block["lines"]:
            spans = line.get("spans") or []
            if not spans:
                continue
            text = "".join(s["text"] for s in spans)
            if not text.strip():
                # keep blank lines only if they have width (rare)
                continue
            rows.append(
                {
                    "text": text,
                    "x0": float(line["bbox"][0]),
                    "y0": float(line["bbox"][1]),
                    "size": float(spans[0].get("size") or 10),
                    "font": spans[0].get("font") or "",
                }
            )
    rows.sort(key=lambda r: (round(r["y0"], 1), r["x0"]))
    return rows


def indent_prefix(x0: float, base_x: float) -> str:
    steps = max(0, int(round((x0 - base_x) / INDENT_UNIT)))
    return "    " * steps


def convert_chapter(ch: dict) -> tuple[str, str]:
    title = ch["title"]
    num = ch.get("num")
    heading = f"{num} · {title}" if num else title

    parts: list[str] = [
        '<header class="chapter-hero">',
    ]
    if num:
        parts.append(f'<p class="chapter-num">Chapter {html.escape(str(num))}</p>')
    parts.append(f"<h1>{html.escape(title)}</h1>")
    parts.append("</header>")
    parts.append('<div class="chapter-body">')

    in_code = False
    code_lang = "text"
    code_buf: list[str] = []
    code_base = CODE_BASE_X
    para: list[str] = []

    def flush_code() -> None:
        nonlocal in_code, code_lang, code_buf, code_base
        if not in_code:
            return
        lang = code_lang.lower().replace(" ", "-")
        code = "\n".join(code_buf).rstrip() + "\n"
        parts.append(
            f'<div class="code-block"><div class="code-lang">{html.escape(code_lang)}</div>'
            f'<pre class="code"><code class="language-{html.escape(lang)}">{html.escape(code)}</code></pre></div>'
        )
        in_code = False
        code_lang = "text"
        code_buf = []
        code_base = CODE_BASE_X

    def flush_para() -> None:
        if not para:
            return
        text = re.sub(r"\s+", " ", " ".join(para)).strip()
        if text:
            parts.append(f"<p>{html.escape(text)}</p>")
        para.clear()

    for page_num in range(ch["start"], ch["end"] + 1):
        page = doc[page_num - 1]
        drawings = len(page.get_drawings())
        raw = page.get_text()
        lines = extract_lines(page_num)

        if page_is_diagram(page_num, raw, drawings):
            flush_code()
            flush_para()
            src = render_diagram(page_num)
            caption = title if page_num == ch["start"] else (lines[0]["text"].strip() if lines else f"Page {page_num}")
            if spaced_caps(caption):
                caption = re.sub(r"\s+", "", caption).title()
            parts.append(
                f'<figure class="diagram">'
                f'<img src="../{src}" alt="{html.escape(caption)}" loading="lazy" />'
                f"<figcaption>{html.escape(caption)}</figcaption>"
                f"</figure>"
            )
            # Skip dumping diagram chrome/labels; keep only longer prose lines if any
            prose_lines = [
                ln
                for ln in lines
                if len(ln["text"].strip()) > 55
                and not spaced_caps(ln["text"].strip())
                and ln["text"].strip().upper() not in {"PROS", "CONS", "GOING DEEPER", "STEP BY STEP"}
            ]
            for ln in prose_lines:
                para.append(ln["text"].strip())
            flush_para()
            continue

        for ln in lines:
            text = ln["text"]
            stripped = text.strip()
            x0 = ln["x0"]
            size = ln["size"]
            font = ln["font"]

            if is_code_lang(stripped):
                flush_para()
                flush_code()
                in_code = True
                code_lang = stripped
                code_buf = []
                code_base = CODE_BASE_X
                continue

            if in_code:
                if spaced_caps(stripped) or (
                    size >= 12 and "Spectral" in font
                ) or (
                    len(stripped) > 75 and not looks_like_code(stripped, x0) and x0 < CODE_BASE_X + 5
                ):
                    flush_code()
                    # fall through to re-handle as prose
                else:
                    if not code_buf:
                        code_base = min(x0, CODE_BASE_X + 1)
                    code_buf.append(indent_prefix(x0, code_base) + stripped)
                    continue

            # After possible code flush, handle as prose
            if spaced_caps(stripped) and len(re.sub(r"\s+", "", stripped)) >= 4:
                flush_para()
                parts.append(f'<h2 class="section-label">{html.escape(stripped)}</h2>')
                continue

            # Skip repeating chapter title on first page
            if page_num == ch["start"] and (
                stripped == title or (num and stripped.startswith(f"{num} "))
            ):
                continue
            if num and stripped == f"{num} {title}":
                continue

            # Large Spectral headings
            if "Spectral" in font and size >= 16:
                flush_para()
                parts.append(f"<h2>{html.escape(stripped)}</h2>")
                continue
            if "Spectral" in font and size >= 13:
                flush_para()
                parts.append(f"<h3>{html.escape(stripped)}</h3>")
                continue

            # ALL-CAPS short headings (non spaced)
            if stripped.isupper() and 3 <= len(stripped) <= 48 and " " in stripped and not spaced_caps(stripped):
                flush_para()
                parts.append(f"<h3>{html.escape(stripped.title())}</h3>")
                continue

            # Start a new paragraph on large y-gaps is hard here; break on sentence-ending previous
            if para and para[-1].endswith((".", "?", "!")) and stripped[:1].isupper():
                flush_para()

            para.append(stripped)

        flush_para()

    flush_code()
    flush_para()
    parts.append("</div>")
    return "\n".join(parts), heading


def main() -> None:
    nav_items = []
    part_label = {
        "front": "Front matter",
        "cp": "Competitive Programming",
        "sd": "System Design",
        "ai": "AI Engineering",
    }

    for ch in chapters:
        body, heading = convert_chapter(ch)
        slug = ch["id"]
        part = ch.get("part") or "front"
        num = ch.get("num")
        title = ch["title"]

        page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(heading)} — Interview Prep</title>
  <meta name="description" content="{html.escape(heading)} — Interview Prep book chapter" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=IBM+Plex+Mono:wght@400;500&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../css/styles.css" />
  <link rel="stylesheet" href="../css/chapter.css" />
</head>
<body class="chapter-page" data-chapter="{html.escape(slug)}" data-part="{html.escape(part)}">
  <a class="skip-link" href="#content">Skip to content</a>
  <div class="chapter-shell">
    <aside class="sidebar" id="sidebar" aria-label="Table of contents"></aside>
    <div class="sidebar-backdrop" id="sidebar-backdrop" hidden></div>
    <main class="chapter-main" id="content">
      <div class="chapter-toolbar">
        <button class="icon-btn menu-toggle" id="menu-toggle" type="button" aria-label="Open contents">☰</button>
        <a class="brand" href="../">Interview Prep <span>Book</span></a>
        <div class="toolbar-spacer"></div>
        <a class="btn btn-ghost btn-small" href="../">Home</a>
      </div>
      <article class="chapter-article">
        <p class="part-eyebrow">{html.escape(part_label.get(part, part))}</p>
        {body}
        <nav class="chapter-pager" id="chapter-pager" aria-label="Chapter pagination"></nav>
      </article>
    </main>
  </div>
  <script src="../js/nav.js"></script>
</body>
</html>
"""
        (OUT_CH / f"{slug}.html").write_text(page)
        nav_items.append(
            {
                "id": slug,
                "num": num,
                "title": title,
                "part": part,
                "href": f"chapters/{slug}.html",
            }
        )
        print(f"wrote {slug}.html")

    (ROOT / "assets" / "nav.json").write_text(json.dumps({"chapters": nav_items}, indent=2))
    print(f"done: {len(nav_items)} chapters, {len(list(OUT_DIAG.glob('*.jpg')))} diagrams")


if __name__ == "__main__":
    main()
