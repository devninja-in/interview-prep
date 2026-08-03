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
CODE_LANGS = {"PYTHON", "JAVA", "SKILL.MD", "MCP SERVER"}
INDENT_UNIT = 24.6
CODE_BASE_X = 58.0

DIAGRAM_MANIFEST = json.loads((OUT_DIAG / "manifest.json").read_text()) if (OUT_DIAG / "manifest.json").exists() else {"chapters": {}}
CHAPTER_DIAGRAMS = DIAGRAM_MANIFEST.get("chapters", {})


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


def page_is_visual_only(page_num: int, text: str, drawings: int, table_count: int = 0) -> bool:
    """PDF pages that are mostly figures — keep prose/tables only, never screenshot them."""
    # Prefer structured extraction when tables exist (e.g. STEP BY STEP walkthroughs)
    if table_count > 0:
        return False
    body = re.sub(r"\s+", " ", text).strip()
    if drawings >= 40 and len(body) < 900:
        return True
    if drawings >= 28 and any(k in text for k in ("Clients", "Write path", "Producer", "Load Balancer")):
        return True
    if any(p.get("page") == page_num and p.get("is_diagram") for p in data.get("pages", [])):
        # Still skip pure diagram screenshots, but not if content is mostly table/text
        if "STEP BY STEP" in text or "Problem type" in text:
            return False
        return True
    return False


def clean_cell(val) -> str:
    if val is None:
        return ""
    return re.sub(r"\s+", " ", str(val)).strip()


def extract_page_tables(page) -> list[dict]:
    """Return usable tables with a tight bbox + normalized rows."""
    out = []
    try:
        finder = page.find_tables()
        tables = finder.tables if finder else []
    except Exception:
        return out

    for t in tables:
        raw = t.extract() or []
        rows = [[clean_cell(c) for c in row] for row in raw]
        rows = [r for r in rows if any(c for c in r)]
        if len(rows) < 2:
            continue

        cols = max((len(r) for r in rows), default=0)
        keep_cols = [ci for ci in range(cols) if any((r[ci] if ci < len(r) else "") for r in rows)]
        if len(keep_cols) < 2:
            continue
        norm = [[(r[ci] if ci < len(r) else "") for ci in keep_cols] for r in rows]

        # Find the real header row: short cells, not a prose paragraph
        header_idx = None
        for i, r in enumerate(norm):
            lengths = [len(c) for c in r]
            if max(lengths, default=0) <= 42 and sum(1 for c in r if c) >= 2:
                # Prefer rows that look like labels (contain short words / symbols)
                header_idx = i
                break
        if header_idx is None:
            continue

        header = norm[header_idx]
        body = []
        for r in norm[header_idx + 1 :]:
            if max((len(c) for c in r), default=0) >= 160:
                continue
            if not any(c for c in r):
                continue
            # skip repeated header-like rows
            if [c.lower() for c in r] == [c.lower() for c in header]:
                continue
            body.append(r)
        if not body:
            continue

        # Tight bbox from only kept rows so prose below is not swallowed
        y_vals = []
        try:
            # include header_idx and following kept body rows
            # Table.rows aligns with extract() rows
            for offset, _ in enumerate([header] + body):
                ri = header_idx + offset
                if ri < len(t.rows):
                    rb = t.rows[ri].bbox
                    y_vals.extend([rb[1], rb[3]])
        except Exception:
            y_vals = [t.bbox[1], t.bbox[3]]
        if not y_vals:
            y_vals = [t.bbox[1], t.bbox[3]]
        bbox = fitz.Rect(t.bbox[0], min(y_vals) - 2, t.bbox[2], max(y_vals) + 2)
        out.append({"bbox": bbox, "header": header, "body": body})
    return out


def table_html(header: list[str], body: list[list[str]], caption: str | None = None) -> str:
    thead = "".join(f"<th>{html.escape(c)}</th>" for c in header)
    rows = []
    for r in body:
        rows.append("<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in r) + "</tr>")
    cap = f"<caption>{html.escape(caption)}</caption>" if caption else ""
    return (
        f'<div class="table-wrap"><table>{cap}<thead><tr>{thead}</tr></thead>'
        f"<tbody>{''.join(rows)}</tbody></table></div>"
    )


def line_in_tables(y0: float, tables: list[dict], pad: float = 4.0) -> bool:
    for t in tables:
        y1, y2 = t["bbox"].y0 - pad, t["bbox"].y1 + pad
        if y1 <= y0 <= y2:
            return True
    return False


def native_diagram_html(chapter_id: str) -> str:
    keys = CHAPTER_DIAGRAMS.get(chapter_id) or []
    chunks = []
    for key in keys:
        src = OUT_DIAG / f"{key}.svg"
        if not src.exists():
            continue
        title = key.replace("-", " ")
        chunks.append(
            f'<figure class="diagram native">'
            f'<img src="../assets/diagrams/{key}.svg" alt="{html.escape(title)}" loading="lazy" />'
            f"</figure>"
        )
    return "\n".join(chunks)


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
    native = native_diagram_html(ch["id"])
    if native:
        parts.append(native)

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
        tables = extract_page_tables(page)

        if page_is_visual_only(page_num, raw, drawings, table_count=len(tables)):
            flush_code()
            flush_para()
            # Keep explanatory prose from architecture pages; never embed PDF screenshots.
            prose_lines = [
                ln
                for ln in lines
                if len(ln["text"].strip()) > 70
                and not spaced_caps(ln["text"].strip())
                and ln["text"].strip().upper() not in {"PROS", "CONS", "GOING DEEPER", "STEP BY STEP"}
            ]
            for ln in prose_lines:
                para.append(ln["text"].strip())
            flush_para()
            continue

        # Tables / prose are interleaved by y-position below.
        emitted_table_ids: set[int] = set()

        def maybe_emit_tables(before_y: float | None) -> None:
            for idx, t in enumerate(tables):
                if idx in emitted_table_ids:
                    continue
                # emit when we have passed the table's top (or at end)
                if before_y is None or t["bbox"].y0 <= before_y + 2:
                    flush_para()
                    flush_code()
                    caption = None
                    if t["header"] and t["header"][0].lower().startswith("problem"):
                        caption = "Pattern → example problems"
                    elif any("nums[i]" in h or h == "i" for h in t["header"]):
                        caption = "Worked walkthrough"
                    parts.append(table_html(t["header"], t["body"], caption))
                    emitted_table_ids.add(idx)

        for ln in lines:
            text = ln["text"]
            stripped = text.strip()
            x0 = ln["x0"]
            size = ln["size"]
            font = ln["font"]
            y0 = ln["y0"]

            # Skip text that belongs to an extracted table
            if line_in_tables(y0, tables):
                maybe_emit_tables(y0)
                continue

            maybe_emit_tables(y0)

            if stripped.upper() == "STEP BY STEP":
                flush_para()
                flush_code()
                parts.append('<h2 class="section-label">S T E P &nbsp; B Y &nbsp; S T E P</h2>')
                continue

            if is_code_lang(stripped):
                flush_para()
                flush_code()
                in_code = True
                code_lang = stripped
                code_buf = []
                code_base = CODE_BASE_X
                continue

            if in_code:
                if (
                    stripped in {"GOING DEEPER", "DEEPER INTUITION"}
                    or spaced_caps(stripped)
                    or (size >= 12 and "Spectral" in font)
                    or (
                        len(stripped) > 75
                        and not looks_like_code(stripped, x0)
                        and x0 < CODE_BASE_X + 5
                    )
                ):
                    flush_code()
                    if stripped in {"GOING DEEPER", "DEEPER INTUITION"}:
                        parts.append(f"<h3>{html.escape(stripped.title())}</h3>")
                        continue
                    # else fall through to re-handle as prose
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

            # Start a new paragraph on sentence boundary
            if para and para[-1].endswith((".", "?", "!")) and stripped[:1].isupper():
                flush_para()

            para.append(stripped)

        maybe_emit_tables(None)
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
        slug = ch["id"]
        # Hand-authored deep AI chapters live under content/ai/ — do not clobber.
        if (ROOT / "content" / "ai" / f"{slug}.html").exists():
            print(f"skip {slug}.html (hand-authored AI content)")
            nav_items.append(
                {
                    "id": slug,
                    "num": ch.get("num"),
                    "title": ch["title"],
                    "part": ch.get("part") or "front",
                    "href": f"chapters/{slug}.html",
                }
            )
            continue
        body, heading = convert_chapter(ch)
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
<link rel="stylesheet" href="../css/styles.css" />
  <link rel="stylesheet" href="../css/chapter.css" />
  <link rel="stylesheet" href="../css/interview.css" />
</head>
<body class="chapter-page" data-chapter="{html.escape(slug)}" data-part="{html.escape(part)}">
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

    # Re-apply Interview Labs + per-chapter drills (also restores lab entries in nav.json).
    try:
        import sys

        sys.path.insert(0, str(ROOT / "scripts"))
        from assemble_interview import main as assemble_interview_main

        assemble_interview_main()
    except Exception as exc:  # pragma: no cover
        print(f"note: could not assemble interview labs: {exc}")


if __name__ == "__main__":
    main()
