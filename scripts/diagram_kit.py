#!/usr/bin/env python3
"""Professional SVG diagram kit for FAANG-style whiteboard figures."""
from __future__ import annotations

import html
import re
from dataclasses import dataclass

# Architecture palette — cool neutrals + one accent (not candy pastels)
INK = "#15202b"
MUTED = "#5b6b76"
LINE = "#9aabb5"
LINE_STRONG = "#2c3a45"
PAPER = "#fbfcfd"
TITLE_BG = "#15202b"
ZONE_CLIENT = "#eef2f5"
ZONE_EDGE = "#e8f1f8"
ZONE_APP = "#e9f4f1"
ZONE_DATA = "#f3f0ea"
ZONE_ASYNC = "#f7f0e6"
FILL_CLIENT = "#ffffff"
FILL_EDGE = "#d9e8f5"
FILL_APP = "#cfe8e2"
FILL_CACHE = "#dde9f7"
FILL_STORE = "#ffffff"
FILL_QUEUE = "#f3e2c7"
FILL_ALERT = "#f5d9d3"
FILL_HL = "#0d7a6f"
FILL_HL_SOFT = "#d5ebe7"
FILL_WARN = "#e8b86d"
SANS = "Manrope, 'Segoe UI', system-ui, sans-serif"
MONO = "'IBM Plex Mono', ui-monospace, monospace"


def _esc(s: str) -> str:
    return html.escape(s, quote=True)


def _fmt(v) -> str:
    if isinstance(v, (int, float)):
        if abs(v - round(v)) < 1e-9:
            return str(int(round(v)))
        return f"{v:.1f}".rstrip("0").rstrip(".")
    return str(v)


def _sid(title: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return (s or "d")[:40]


@dataclass
class Canvas:
    w: int
    h: int
    title: str
    note: str = ""
    parts: list[str] | None = None

    def __post_init__(self):
        if self.parts is None:
            self.parts = []

    def add(self, *chunks: str) -> "Canvas":
        self.parts.extend(chunks)
        return self

    def render(self) -> str:
        mid = _sid(self.title)
        note_html = ""
        if self.note:
            note_html = (
                f'<rect x="0" y="{self.h - 36}" width="{self.w}" height="36" fill="#f0f3f5"/>'
                f'<text x="28" y="{self.h - 14}" font-family="{MONO}" font-size="11" fill="{MUTED}">'
                f"{_esc(self.note)}</text>"
            )
        body = "\n".join(self.parts)
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{_esc(self.title)}">
  <defs>
    <marker id="arr-{mid}" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">
      <path d="M0,0 L10,4 L0,8 Z" fill="{LINE_STRONG}"/>
    </marker>
    <marker id="arr-acc-{mid}" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">
      <path d="M0,0 L10,4 L0,8 Z" fill="{FILL_HL}"/>
    </marker>
    <filter id="sh-{mid}" x="-8%" y="-8%" width="116%" height="124%">
      <feDropShadow dx="0" dy="1" stdDeviation="1.2" flood-color="#15202b" flood-opacity="0.10"/>
    </filter>
  </defs>
  <rect width="{self.w}" height="{self.h}" fill="{PAPER}"/>
  <rect x="0" y="0" width="{self.w}" height="44" fill="{TITLE_BG}"/>
  <text x="28" y="28" font-family="{SANS}" font-size="16" font-weight="700" fill="#ffffff">{_esc(self.title)}</text>
  {body}
  {note_html}
</svg>
'''


def zone(x, y, w, h, label: str, fill: str) -> str:
    x, y, w, h = map(_fmt, (x, y, w, h))
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{LINE}" stroke-width="1"/>'
        f'<text x="{_fmt(float(x) + 12)}" y="{_fmt(float(y) + 18)}" font-family="{MONO}" font-size="10" font-weight="600" '
        f'letter-spacing="0.08em" fill="{MUTED}">{_esc(label.upper())}</text>'
    )


def node(
    x,
    y,
    w,
    h,
    label: str,
    *,
    sub: str = "",
    kind: str = "app",
    mid: str = "d",
    rx: int = 6,
) -> str:
    fills = {
        "client": FILL_CLIENT,
        "edge": FILL_EDGE,
        "app": FILL_APP,
        "cache": FILL_CACHE,
        "store": FILL_STORE,
        "queue": FILL_QUEUE,
        "alert": FILL_ALERT,
        "hl": FILL_HL_SOFT,
        "warn": "#f7e7c8",
        "white": "#ffffff",
    }
    fill = fills.get(kind, FILL_APP)
    stroke = FILL_HL if kind == "hl" else (LINE_STRONG if kind in ("store", "queue") else LINE)
    sw = 1.6 if kind in ("store", "queue", "hl") else 1.2
    # cylinder hint for stores
    extra = ""
    if kind == "store":
        extra = (
            f'<path d="M{_fmt(x)},{_fmt(y + 8)} Q{_fmt(x + w/2)},{_fmt(y - 2)} {_fmt(x + w)},{_fmt(y + 8)}" fill="none" stroke="{stroke}" stroke-width="1"/>'
        )
    ly = y + h / 2 - (7 if sub else 0)
    lines = [
        f'<rect x="{_fmt(x)}" y="{_fmt(y)}" width="{_fmt(w)}" height="{_fmt(h)}" rx="{_fmt(rx)}" fill="{fill}" stroke="{stroke}" '
        f'stroke-width="{sw}" filter="url(#sh-{mid})"/>',
        extra,
        f'<text x="{_fmt(x + w/2)}" y="{_fmt(ly)}" text-anchor="middle" font-family="{SANS}" font-size="12.5" '
        f'font-weight="650" fill="{INK}">{_esc(label)}</text>',
    ]
    if sub:
        lines.append(
            f'<text x="{_fmt(x + w/2)}" y="{_fmt(ly + 15)}" text-anchor="middle" font-family="{MONO}" font-size="10" '
            f'fill="{MUTED}">{_esc(sub)}</text>'
        )
    return "\n".join(lines)


def cell(x, y, w, h, label: str, *, active: bool = False, soft: bool = False, mid: str = "d") -> str:
    if active:
        fill, stroke, sw = FILL_HL, FILL_HL, 1.8
        tc = "#ffffff"
    elif soft:
        fill, stroke, sw, tc = FILL_HL_SOFT, LINE, 1.2, INK
    else:
        fill, stroke, sw, tc = "#ffffff", LINE, 1.2, INK
    return (
        f'<rect x="{_fmt(x)}" y="{_fmt(y)}" width="{_fmt(w)}" height="{_fmt(h)}" rx="4" fill="{fill}" stroke="{stroke}" '
        f'stroke-width="{sw}" filter="url(#sh-{mid})"/>'
        f'<text x="{_fmt(x + w/2)}" y="{_fmt(y + h/2 + 4)}" text-anchor="middle" font-family="{MONO}" '
        f'font-size="12" font-weight="600" fill="{tc}">{_esc(str(label))}</text>'
    )


def arrow(x1, y1, x2, y2, *, mid: str = "d", accent: bool = False, dashed: bool = False) -> str:
    mk = f"arr-acc-{mid}" if accent else f"arr-{mid}"
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    color = FILL_HL if accent else LINE_STRONG
    return (
        f'<path d="M{_fmt(x1)} {_fmt(y1)} L{_fmt(x2)} {_fmt(y2)}" fill="none" stroke="{color}" stroke-width="1.6"'
        f'{dash} marker-end="url(#{mk})"/>'
    )


def elbow(x1, y1, x2, y2, *, mid: str = "d", via: str = "hv", accent: bool = False, dashed: bool = False) -> str:
    """Orthogonal connector: hv = horizontal then vertical; vh = vertical then horizontal."""
    mk = f"arr-acc-{mid}" if accent else f"arr-{mid}"
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    color = FILL_HL if accent else LINE_STRONG
    if via == "hv":
        d = f"M{_fmt(x1)} {_fmt(y1)} H{_fmt(x2)} V{_fmt(y2)}"
    else:
        d = f"M{_fmt(x1)} {_fmt(y1)} V{_fmt(y2)} H{_fmt(x2)}"
    return (
        f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.5"{dash} marker-end="url(#{mk})"/>'
    )


def label(x, y, text: str, *, mono: bool = True, accent: bool = False, anchor: str = "start") -> str:
    fam = MONO if mono else SANS
    color = FILL_HL if accent else MUTED
    return (
        f'<text x="{_fmt(x)}" y="{_fmt(y)}" text-anchor="{anchor}" font-family="{fam}" font-size="11" '
        f'fill="{color}">{_esc(text)}</text>'
    )


def badge(x, y, n: int | str, *, mid: str = "d") -> str:
    return (
        f'<circle cx="{_fmt(x)}" cy="{_fmt(y)}" r="10" fill="{TITLE_BG}"/>'
        f'<text x="{_fmt(x)}" y="{_fmt(y + 4)}" text-anchor="middle" font-family="{MONO}" font-size="11" '
        f'font-weight="700" fill="#fff">{n}</text>'
    )


def legend(x, y, items: list[tuple[str, str]], *, mid: str = "d") -> str:
    """items: (kind, label)"""
    parts = [label(x, y, "LEGEND", mono=True)]
    for i, (kind, text) in enumerate(items):
        yy = y + 14 + i * 18
        parts.append(node(x, yy - 10, 18, 14, "", kind=kind, mid=mid, rx=3))
        parts.append(label(x + 26, yy + 2, text, mono=False))
    return "\n".join(parts)


def callout(x, y, w, h, title: str, body: str, *, mid: str = "d") -> str:
    return (
        f'<rect x="{_fmt(x)}" y="{_fmt(y)}" width="{_fmt(w)}" height="{_fmt(h)}" rx="6" fill="#ffffff" stroke="{LINE}" stroke-width="1.2"/>'
        f'<text x="{_fmt(x + 12)}" y="{_fmt(y + 18)}" font-family="{MONO}" font-size="10" font-weight="700" fill="{FILL_HL}">'
        f"{_esc(title.upper())}</text>"
        f'<text x="{_fmt(x + 12)}" y="{_fmt(y + 38)}" font-family="{SANS}" font-size="12" fill="{INK}">{_esc(body)}</text>'
    )


def path_line(d: str, *, mid: str = "d", accent: bool = False, dashed: bool = False, arrow: bool = True) -> str:
    mk = f' marker-end="url(#arr-acc-{mid})"' if accent and arrow else (
        f' marker-end="url(#arr-{mid})"' if arrow else ""
    )
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    color = FILL_HL if accent else LINE_STRONG
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.55"{dash}{mk}/>'


def mid_of(title: str) -> str:
    return _sid(title)
