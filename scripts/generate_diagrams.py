#!/usr/bin/env python3
"""Generate native SVG topic diagrams (not PDF page screenshots)."""
from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "assets" / "diagrams"
OUT.mkdir(parents=True, exist_ok=True)

# Site palette
INK = "#0f1c24"
SOFT = "#3a4a54"
ACCENT = "#0d7a6f"
ACCENT_SOFT = "#d7ebe7"
SAND = "#f3e8d8"
ROSE = "#f7ddd4"
LINE = "#c5d5ce"
PAPER = "#f7faf8"
MONO = "IBM Plex Mono, ui-monospace, monospace"
SANS = "Manrope, Segoe UI, sans-serif"


def svg(w: int, h: int, body: str, title: str) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{title}">
  <defs>
    <marker id="arrowhead" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="{INK}"/>
    </marker>
  </defs>
  <rect width="{w}" height="{h}" fill="{PAPER}"/>
  <text x="24" y="36" font-family="{SANS}" font-size="18" font-weight="700" fill="{INK}">{title}</text>
  {body}
</svg>
'''


def box(x, y, w, h, fill, label, sub="", rx=10):
    lines = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{LINE}" stroke-width="1.2"/>',
        f'<text x="{x + w/2}" y="{y + h/2 - (6 if sub else 0)}" text-anchor="middle" font-family="{SANS}" font-size="13" font-weight="650" fill="{INK}">{label}</text>',
    ]
    if sub:
        lines.append(
            f'<text x="{x + w/2}" y="{y + h/2 + 14}" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{SOFT}">{sub}</text>'
        )
    return "\n".join(lines)


def caption(x, y, text):
    return f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="11" fill="{SOFT}">{text}</text>'


DIAGRAMS: dict[str, str] = {}

# --- Competitive programming ---
DIAGRAMS["hash-map"] = svg(
    720,
    280,
    f'''
  {box(40, 90, 90, 54, SAND, "key", '"apple"')}
  {box(40, 160, 90, 54, SAND, "key", '"mango"')}
  <text x="155" y="150" font-family="{MONO}" font-size="12" fill="{ACCENT}">hash()</text>
  <path d="M140 117 H210" stroke="{INK}" stroke-width="1.5" marker-end="url(#arrowhead)"/>
  <path d="M140 187 H210" stroke="{INK}" stroke-width="1.5" marker-end="url(#arrowhead)"/>
  {box(220, 80, 70, 44, ACCENT_SOFT, "[0]")}
  {box(220, 132, 70, 44, ACCENT_SOFT, "[1]", "apple")}
  {box(220, 184, 70, 44, ACCENT_SOFT, "[2]", "mango")}
  {box(320, 132, 140, 44, ROSE, "collision?", "chain / probe")}
  {caption(40, 260, "Hashing turns a key into a bucket index so lookup stays near O(1).")}
''',
    "Hash map lookup",
)

DIAGRAMS["two-pointers"] = svg(
    720,
    240,
    f'''
  {"".join(box(60 + i*70, 100, 58, 58, ACCENT_SOFT if i in (0,5) else "#fff", str(v)) for i,v in enumerate([1,2,3,4,6,8]))}
  <text x="89" y="90" font-family="{MONO}" font-size="11" fill="{ACCENT}">L</text>
  <text x="439" y="90" font-family="{MONO}" font-size="11" fill="{ACCENT}">R</text>
  <path d="M89 175 V195 H439 V175" fill="none" stroke="{ACCENT}" stroke-width="1.6"/>
  {caption(60, 220, "Move L/R based on the sum (or condition) until they meet.")}
''',
    "Two pointers",
)

DIAGRAMS["sliding-window"] = svg(
    720,
    240,
    f'''
  {"".join(box(50 + i*62, 100, 52, 52, ROSE if 2 <= i <= 4 else "#fff", c) for i,c in enumerate(list("ABCAC")))}
  <rect x="{50+2*62}" y="94" width="{52*3+20}" height="64" rx="8" fill="none" stroke="{ACCENT}" stroke-width="2.2"/>
  <text x="210" y="85" font-family="{MONO}" font-size="12" fill="{ACCENT}">window</text>
  {caption(50, 210, "Grow right, shrink left — keep only what the constraint allows.")}
''',
    "Sliding window",
)

DIAGRAMS["stack"] = svg(
    720,
    260,
    f'''
  {box(80, 180, 120, 40, ACCENT_SOFT, "A")}
  {box(80, 130, 120, 40, ACCENT_SOFT, "B")}
  {box(80, 80, 120, 40, ROSE, "C", "top")}
  <text x="260" y="120" font-family="{SANS}" font-size="14" fill="{INK}">push → add on top</text>
  <text x="260" y="150" font-family="{SANS}" font-size="14" fill="{INK}">pop → remove from top</text>
  {caption(80, 240, "Last in, first out — perfect for matching and next-greater problems.")}
''',
    "Stack",
)

DIAGRAMS["binary-search"] = svg(
    720,
    240,
    f'''
  {"".join(box(40 + i*70, 110, 58, 50, ROSE if i==3 else ACCENT_SOFT if i in (0,1,2) else "#fff", str(v)) for i,v in enumerate([2,4,6,8,10,12,14]))}
  <text x="60" y="95" font-family="{MONO}" font-size="11" fill="{ACCENT}">lo</text>
  <text x="270" y="95" font-family="{MONO}" font-size="11" fill="{ACCENT}">mid</text>
  <text x="480" y="95" font-family="{MONO}" font-size="11" fill="{SOFT}">hi</text>
  {caption(40, 210, "Compare mid, throw away half the search space each step.")}
''',
    "Binary search",
)

DIAGRAMS["linked-list"] = svg(
    720,
    240,
    f'''
  {box(50, 100, 70, 50, ACCENT_SOFT, "1")}
  {box(170, 100, 70, 50, ACCENT_SOFT, "2")}
  {box(290, 100, 70, 50, ACCENT_SOFT, "3")}
  <path d="M120 125 H165" stroke="{INK}" stroke-width="1.6"/>
  <path d="M240 125 H285" stroke="{INK}" stroke-width="1.6"/>
  <text x="400" y="110" font-family="{SANS}" font-size="13" fill="{INK}">reverse →</text>
  {box(500, 100, 70, 50, ROSE, "3")}
  {box(590, 100, 70, 50, ACCENT_SOFT, "2")}
  <path d="M570 125 H585" stroke="{INK}" stroke-width="1.6"/>
  {caption(50, 210, "Rewire next pointers carefully — null checks catch most bugs.")}
''',
    "Linked list reverse",
)

DIAGRAMS["tree-bst"] = svg(
    720,
    300,
    f'''
  {box(310, 70, 70, 40, ROSE, "8")}
  {box(180, 140, 70, 40, ACCENT_SOFT, "3")}
  {box(440, 140, 70, 40, ACCENT_SOFT, "10")}
  {box(120, 210, 70, 40, "#fff", "1")}
  {box(240, 210, 70, 40, "#fff", "6")}
  <path d="M330 110 L230 140" stroke="{INK}" stroke-width="1.4"/>
  <path d="M360 110 L460 140" stroke="{INK}" stroke-width="1.4"/>
  <path d="M200 180 L155 210" stroke="{INK}" stroke-width="1.4"/>
  <path d="M230 180 L270 210" stroke="{INK}" stroke-width="1.4"/>
  {caption(50, 280, "BST rule: left &lt; node &lt; right at every level.")}
''',
    "Binary search tree",
)

DIAGRAMS["heap"] = svg(
    720,
    280,
    f'''
  {box(310, 70, 70, 40, ROSE, "1", "min")}
  {box(200, 140, 70, 40, ACCENT_SOFT, "3")}
  {box(420, 140, 70, 40, ACCENT_SOFT, "2")}
  {box(140, 210, 70, 40, "#fff", "7")}
  {box(260, 210, 70, 40, "#fff", "5")}
  <path d="M330 110 L250 140" stroke="{INK}" stroke-width="1.4"/>
  <path d="M360 110 L440 140" stroke="{INK}" stroke-width="1.4"/>
  <path d="M220 180 L175 210" stroke="{INK}" stroke-width="1.4"/>
  <path d="M250 180 L290 210" stroke="{INK}" stroke-width="1.4"/>
  {caption(50, 260, "Parent is always smaller (min-heap) or larger (max-heap) than children.")}
''',
    "Heap / priority queue",
)

DIAGRAMS["backtracking"] = svg(
    720,
    260,
    f'''
  {box(40, 100, 140, 56, SAND, "1. Choose")}
  {box(240, 100, 140, 56, ACCENT_SOFT, "2. Explore")}
  {box(440, 100, 140, 56, ROSE, "3. Unchoose")}
  <path d="M185 128 H235" stroke="{INK}" stroke-width="1.6"/>
  <path d="M385 128 H435" stroke="{INK}" stroke-width="1.6"/>
  {caption(40, 210, "Build a candidate, recurse, then undo the choice and try the next.")}
''',
    "Backtracking loop",
)

DIAGRAMS["bfs-graph"] = svg(
    720,
    300,
    f'''
  {box(60, 130, 60, 40, ROSE, "A")}
  {box(200, 70, 60, 40, ACCENT_SOFT, "B")}
  {box(200, 190, 60, 40, ACCENT_SOFT, "C")}
  {box(340, 40, 60, 40, "#fff", "D")}
  {box(340, 120, 60, 40, "#fff", "E")}
  {box(340, 220, 60, 40, "#fff", "F")}
  <path d="M120 145 H195" stroke="{INK}" stroke-width="1.3"/>
  <path d="M120 155 H195 M200 165" stroke="{INK}" stroke-width="1.3"/>
  <path d="M120 150 Q160 200 200 205" fill="none" stroke="{INK}" stroke-width="1.3"/>
  <path d="M260 90 H335" stroke="{INK}" stroke-width="1.3"/>
  <path d="M260 100 H335 M340 135" stroke="{INK}" stroke-width="1.3"/>
  <path d="M260 210 H335" stroke="{INK}" stroke-width="1.3"/>
  {caption(40, 280, "BFS explores layer by layer using a queue — shortest path in unweighted graphs.")}
''',
    "Graph BFS layers",
)

DIAGRAMS["dp-table"] = svg(
    720,
    260,
    f'''
  {"".join(box(80 + i*70, 90, 60, 44, ACCENT_SOFT if i else ROSE, f"dp[{i}]", str(v)) for i,v in enumerate([0,1,1,2,3,5]))}
  <path d="M140 160 H470" stroke="{ACCENT}" stroke-width="1.5" stroke-dasharray="4 4"/>
  {caption(80, 210, "Each cell is built from earlier answers — get the recurrence and base cases right.")}
''',
    "Dynamic programming table",
)

DIAGRAMS["intervals"] = svg(
    720,
    240,
    f'''
  <rect x="60" y="100" width="180" height="28" rx="6" fill="{ACCENT_SOFT}" stroke="{LINE}"/>
  <rect x="200" y="145" width="160" height="28" rx="6" fill="{ROSE}" stroke="{LINE}"/>
  <rect x="390" y="100" width="140" height="28" rx="6" fill="{SAND}" stroke="{LINE}"/>
  <line x1="50" y1="200" x2="560" y2="200" stroke="{INK}" stroke-width="1.2"/>
  {caption(60, 225, "Sort by start, then merge overlaps as you scan.")}
''',
    "Intervals",
)

DIAGRAMS["bits-xor"] = svg(
    720,
    240,
    f'''
  <text x="60" y="110" font-family="{MONO}" font-size="16" fill="{INK}">5 = 1 0 1</text>
  <text x="60" y="145" font-family="{MONO}" font-size="16" fill="{INK}">3 = 0 1 1</text>
  <line x1="60" y1="160" x2="200" y2="160" stroke="{LINE}"/>
  <text x="60" y="190" font-family="{MONO}" font-size="16" fill="{ACCENT}">XOR 1 1 0 = 6</text>
  {caption(280, 145, "XOR cancels pairs — lonely numbers fall out for free.")}
''',
    "Bit manipulation",
)

# --- System design ---
DIAGRAMS["load-balancer"] = svg(
    760,
    300,
    f'''
  {box(40, 130, 110, 50, SAND, "Clients")}
  {box(240, 130, 140, 50, ROSE, "Load Balancer", "health checks")}
  {box(500, 70, 120, 44, ACCENT_SOFT, "Server 1")}
  {box(500, 130, 120, 44, ACCENT_SOFT, "Server 2")}
  {box(500, 190, 120, 44, ACCENT_SOFT, "Server 3")}
  <path d="M155 155 H235" stroke="{INK}" stroke-width="1.6"/>
  <path d="M385 145 H495" stroke="{INK}" stroke-width="1.4"/>
  <path d="M385 155 H495" stroke="{INK}" stroke-width="1.4"/>
  <path d="M385 165 H495" stroke="{INK}" stroke-width="1.4"/>
  {caption(40, 270, "One entry point spreads traffic across identical, stateless servers.")}
''',
    "Load balancer",
)

DIAGRAMS["cache-cdn"] = svg(
    760,
    280,
    f'''
  {box(40, 120, 100, 48, SAND, "User")}
  {box(200, 120, 110, 48, ROSE, "CDN / edge")}
  {box(370, 120, 110, 48, ACCENT_SOFT, "App cache")}
  {box(540, 120, 120, 48, "#fff", "Database")}
  <path d="M145 144 H195" stroke="{INK}" stroke-width="1.5"/>
  <path d="M315 144 H365" stroke="{INK}" stroke-width="1.5"/>
  <path d="M485 144 H535" stroke="{INK}" stroke-width="1.5"/>
  {caption(40, 230, "Serve hot data from the closest fast layer; fall back on a miss.")}
''',
    "Caching & CDNs",
)

DIAGRAMS["sql-nosql"] = svg(
    760,
    280,
    f'''
  {box(60, 90, 260, 140, ACCENT_SOFT, "SQL", "fixed schema · joins · ACID")}
  {box(400, 90, 260, 140, ROSE, "NoSQL", "flexible · scale-out · simple access")}
  {caption(60, 260, "Pick for access patterns first — not fashion.")}
''',
    "SQL vs NoSQL",
)

DIAGRAMS["replication"] = svg(
    760,
    300,
    f'''
  {box(80, 80, 140, 50, ROSE, "Primary")}
  {box(80, 180, 140, 44, ACCENT_SOFT, "Replica A")}
  {box(280, 180, 140, 44, ACCENT_SOFT, "Replica B")}
  <path d="M150 135 V175" stroke="{INK}" stroke-width="1.4"/>
  <path d="M150 135 H350 V175" fill="none" stroke="{INK}" stroke-width="1.4"/>
  {box(500, 120, 160, 70, SAND, "Shard map", "user_id → shard")}
  {caption(80, 270, "Replication for reads/HA; sharding for capacity.")}
''',
    "Replication & sharding",
)

DIAGRAMS["cap"] = svg(
    720,
    300,
    f'''
  <polygon points="340,70 160,240 520,240" fill="{ACCENT_SOFT}" stroke="{LINE}" stroke-width="1.4"/>
  <text x="340" y="95" text-anchor="middle" font-family="{SANS}" font-size="14" font-weight="700" fill="{INK}">C</text>
  <text x="175" y="255" text-anchor="middle" font-family="{SANS}" font-size="14" font-weight="700" fill="{INK}">A</text>
  <text x="505" y="255" text-anchor="middle" font-family="{SANS}" font-size="14" font-weight="700" fill="{INK}">P</text>
  <text x="250" y="170" font-family="{MONO}" font-size="11" fill="{SOFT}">CP</text>
  <text x="400" y="170" font-family="{MONO}" font-size="11" fill="{SOFT}">AP</text>
  {caption(80, 285, "During a partition you choose consistency or availability.")}
''',
    "CAP trade-offs",
)

DIAGRAMS["queue"] = svg(
    760,
    260,
    f'''
  {box(40, 110, 120, 50, SAND, "Producer")}
  {box(240, 100, 200, 70, ROSE, "Queue / topic", "async buffer")}
  {box(520, 90, 120, 44, ACCENT_SOFT, "Worker A")}
  {box(520, 150, 120, 44, ACCENT_SOFT, "Worker B")}
  <path d="M165 135 H235" stroke="{INK}" stroke-width="1.5"/>
  <path d="M445 125 H515" stroke="{INK}" stroke-width="1.4"/>
  <path d="M445 145 H515" stroke="{INK}" stroke-width="1.4"/>
  {caption(40, 230, "Decouple producers from consumers and smooth traffic spikes.")}
''',
    "Message queues",
)

DIAGRAMS["url-shortener"] = svg(
    760,
    280,
    f'''
  {box(40, 110, 90, 48, SAND, "Client")}
  {box(180, 110, 90, 48, ROSE, "API")}
  {box(320, 110, 120, 48, ACCENT_SOFT, "ID service")}
  {box(490, 70, 140, 40, "#fff", "KV / DB")}
  {box(490, 150, 140, 40, "#fff", "Cache")}
  <path d="M135 134 H175" stroke="{INK}" stroke-width="1.4"/>
  <path d="M275 134 H315" stroke="{INK}" stroke-width="1.4"/>
  <path d="M445 125 H485" stroke="{INK}" stroke-width="1.3"/>
  <path d="M445 145 H485" stroke="{INK}" stroke-width="1.3"/>
  {caption(40, 240, "Write path: create code, store mapping, cache hot redirects.")}
''',
    "URL shortener write path",
)

DIAGRAMS["chat-flow"] = svg(
    760,
    280,
    f'''
  {box(40, 110, 100, 48, SAND, "Client A")}
  {box(190, 110, 120, 48, ROSE, "Gateway")}
  {box(360, 110, 130, 48, ACCENT_SOFT, "Chat service")}
  {box(540, 70, 130, 40, "#fff", "Store")}
  {box(540, 160, 130, 40, "#fff", "Client B")}
  <path d="M145 134 H185" stroke="{INK}" stroke-width="1.4"/>
  <path d="M315 134 H355" stroke="{INK}" stroke-width="1.4"/>
  <path d="M495 125 H535" stroke="{INK}" stroke-width="1.3"/>
  <path d="M495 145 H535" stroke="{INK}" stroke-width="1.3"/>
  {caption(40, 240, "Persist first, then fan out to connected recipients.")}
''',
    "Chat message flow",
)

DIAGRAMS["feed-fanout"] = svg(
    760,
    280,
    f'''
  {box(40, 110, 110, 48, SAND, "New post")}
  {box(210, 110, 130, 48, ROSE, "Fanout worker")}
  {box(410, 60, 140, 40, ACCENT_SOFT, "Follower feed 1")}
  {box(410, 120, 140, 40, ACCENT_SOFT, "Follower feed 2")}
  {box(410, 180, 140, 40, ACCENT_SOFT, "Follower feed N")}
  <path d="M155 134 H205" stroke="{INK}" stroke-width="1.4"/>
  <path d="M345 120 H405" stroke="{INK}" stroke-width="1.3"/>
  <path d="M345 134 H405" stroke="{INK}" stroke-width="1.3"/>
  <path d="M345 148 H405" stroke="{INK}" stroke-width="1.3"/>
  {caption(40, 250, "Push fanout writes the post id into follower inboxes ahead of time.")}
''',
    "Feed fanout",
)

DIAGRAMS["object-storage"] = svg(
    760,
    280,
    f'''
  {box(40, 120, 100, 48, SAND, "Object")}
  {box(200, 90, 100, 40, ROSE, "chunk 1")}
  {box(200, 145, 100, 40, ROSE, "chunk 2")}
  {box(200, 200, 100, 40, ROSE, "chunk 3")}
  {box(380, 90, 120, 40, ACCENT_SOFT, "disk / rack A")}
  {box(380, 145, 120, 40, ACCENT_SOFT, "disk / rack B")}
  {box(380, 200, 120, 40, ACCENT_SOFT, "disk / rack C")}
  <path d="M145 140 H195" stroke="{INK}" stroke-width="1.3"/>
  <path d="M145 145 H195" stroke="{INK}" stroke-width="1.3"/>
  <path d="M145 155 H195" stroke="{INK}" stroke-width="1.3"/>
  {caption(40, 260, "Split, replicate across failure domains, reassemble on read.")}
''',
    "Object storage",
)

DIAGRAMS["video-pipeline"] = svg(
    760,
    260,
    f'''
  {box(40, 110, 110, 48, SAND, "Upload")}
  {box(200, 110, 130, 48, ROSE, "Transcode")}
  {box(380, 80, 100, 40, ACCENT_SOFT, "1080p")}
  {box(380, 140, 100, 40, ACCENT_SOFT, "720p")}
  {box(540, 110, 120, 48, "#fff", "CDN")}
  <path d="M155 134 H195" stroke="{INK}" stroke-width="1.4"/>
  <path d="M335 125 H375" stroke="{INK}" stroke-width="1.3"/>
  <path d="M335 145 H375" stroke="{INK}" stroke-width="1.3"/>
  <path d="M485 134 H535" stroke="{INK}" stroke-width="1.4"/>
  {caption(40, 230, "Transcode once, then serve the right rendition from the edge.")}
''',
    "Video pipeline",
)

DIAGRAMS["geo-matching"] = svg(
    760,
    300,
    f'''
  <rect x="80" y="70" width="280" height="180" fill="#fff" stroke="{LINE}"/>
  <path d="M150 70 V250 M220 70 V250 M290 70 V250 M80 130 H360 M80 190 H360" stroke="{LINE}"/>
  <circle cx="200" cy="160" r="10" fill="{ROSE}" stroke="{INK}"/>
  <text x="214" y="164" font-family="{MONO}" font-size="12" fill="{INK}">R</text>
  <circle cx="175" cy="145" r="5" fill="{ACCENT}"/>
  <circle cx="230" cy="175" r="5" fill="{ACCENT}"/>
  <circle cx="250" cy="140" r="5" fill="{ACCENT}"/>
  {caption(400, 140, "Rider R")}
  {caption(400, 165, "Drivers in nearby cells")}
  {caption(80, 280, "Search the rider cell and neighbors — not the whole map.")}
''',
    "Geo matching",
)

# --- AI ---
DIAGRAMS["llm-flow"] = svg(
    760,
    260,
    f'''
  {box(40, 110, 120, 50, SAND, "Tokens in")}
  {box(220, 110, 160, 50, ROSE, "Model", "next-token probs")}
  {box(440, 110, 140, 50, ACCENT_SOFT, "Sample", "temperature")}
  <path d="M165 135 H215" stroke="{INK}" stroke-width="1.5"/>
  <path d="M385 135 H435" stroke="{INK}" stroke-width="1.5"/>
  {caption(40, 220, "A model predicts the next token from context — repeatedly.")}
''',
    "How an LLM answers",
)

DIAGRAMS["rag"] = svg(
    760,
    300,
    f'''
  {box(40, 70, 140, 44, SAND, "Documents")}
  {box(40, 150, 140, 44, ROSE, " Embeddings")}
  {box(40, 220, 140, 44, ACCENT_SOFT, "Vector index")}
  {box(280, 150, 140, 50, SAND, "Question")}
  {box(480, 90, 160, 50, ROSE, "Retrieve top-k")}
  {box(480, 180, 160, 50, ACCENT_SOFT, "LLM + context")}
  <path d="M110 118 V145" stroke="{INK}" stroke-width="1.3"/>
  <path d="M110 198 V215" stroke="{INK}" stroke-width="1.3"/>
  <path d="M185 240 H470" stroke="{INK}" stroke-width="1.2"/>
  <path d="M425 175 H475" stroke="{INK}" stroke-width="1.3"/>
  <path d="M560 145 V175" stroke="{INK}" stroke-width="1.3"/>
  {caption(280, 280, "Index once; on each question retrieve, then generate.")}
''',
    "RAG pipeline",
)

DIAGRAMS["memory"] = svg(
    760,
    280,
    f'''
  {box(60, 80, 520, 50, ROSE, "Context window", "system · history · tools · user")}
  {box(60, 170, 200, 50, ACCENT_SOFT, "Short-term", "recent turns")}
  {box(320, 170, 260, 50, SAND, "Long-term retrieval", "search past notes")}
  {caption(60, 250, "Everything competing for one fixed window — budget it carefully.")}
''',
    "Memory layers",
)

DIAGRAMS["agent-loop"] = svg(
    760,
    260,
    f'''
  {box(60, 110, 120, 50, SAND, "Think")}
  {box(240, 110, 120, 50, ROSE, "Act / tool")}
  {box(420, 110, 120, 50, ACCENT_SOFT, "Observe")}
  <path d="M185 135 H235" stroke="{INK}" stroke-width="1.5"/>
  <path d="M365 135 H415" stroke="{INK}" stroke-width="1.5"/>
  <path d="M540 135 H580 Q610 135 610 180 H120 Q90 180 90 145" fill="none" stroke="{ACCENT}" stroke-width="1.5" stroke-dasharray="5 4"/>
  {caption(60, 220, "ReAct-style loop: reason, call a tool, read the result, repeat.")}
''',
    "Agent loop",
)

DIAGRAMS["mcp"] = svg(
    760,
    280,
    f'''
  {box(60, 110, 120, 50, SAND, "App A")}
  {box(60, 180, 120, 50, SAND, "App B")}
  {box(280, 130, 150, 60, ROSE, "MCP", "one protocol")}
  {box(520, 90, 130, 44, ACCENT_SOFT, "Tools")}
  {box(520, 150, 130, 44, ACCENT_SOFT, "Data")}
  {box(520, 210, 130, 44, ACCENT_SOFT, "Prompts")}
  <path d="M185 135 H275" stroke="{INK}" stroke-width="1.3"/>
  <path d="M185 200 H275" stroke="{INK}" stroke-width="1.3"/>
  <path d="M435 150 H515" stroke="{INK}" stroke-width="1.3"/>
  {caption(60, 265, "Standardize tool access instead of N×M custom integrations.")}
''',
    "MCP",
)

DIAGRAMS["skills"] = svg(
    760,
    260,
    f'''
  {box(60, 100, 180, 70, SAND, "Name + description", "always loaded")}
  {box(300, 100, 200, 70, ROSE, "Full SKILL.md", "loaded when needed")}
  {box(560, 100, 120, 70, ACCENT_SOFT, "Agent")}
  <path d="M245 135 H295" stroke="{INK}" stroke-width="1.4"/>
  <path d="M505 135 H555" stroke="{INK}" stroke-width="1.4"/>
  {caption(60, 220, "Keep catalogs cheap; pull full instructions only for the active skill.")}
''',
    "Skills loading",
)

DIAGRAMS["ai-assistant"] = svg(
    760,
    300,
    f'''
  {box(40, 120, 100, 48, SAND, "User")}
  {box(190, 110, 140, 68, ROSE, "Orchestrator", "agent loop")}
  {box(390, 60, 130, 44, ACCENT_SOFT, "Memory")}
  {box(390, 120, 130, 44, ACCENT_SOFT, "RAG")}
  {box(390, 180, 130, 44, ACCENT_SOFT, "MCP tools")}
  {box(580, 120, 120, 48, "#fff", "Model")}
  <path d="M145 144 H185" stroke="{INK}" stroke-width="1.4"/>
  <path d="M335 130 H385" stroke="{INK}" stroke-width="1.3"/>
  <path d="M335 144 H385" stroke="{INK}" stroke-width="1.3"/>
  <path d="M335 158 H385" stroke="{INK}" stroke-width="1.3"/>
  <path d="M525 144 H575" stroke="{INK}" stroke-width="1.4"/>
  {caption(40, 270, "One orchestrator owns context and routes memory, retrieval, and tools.")}
''',
    "AI assistant design",
)

# --- AI interview deep-dive diagrams ---
DIAGRAMS["rag-detailed"] = svg(
    820,
    360,
    f'''
  <text x="40" y="68" font-family="{MONO}" font-size="12" fill="{ACCENT}">INGEST (offline / nearline)</text>
  {box(40, 80, 100, 44, SAND, "Connectors")}
  {box(160, 80, 90, 44, "#fff", "Clean")}
  {box(270, 80, 90, 44, ROSE, "Chunk")}
  {box(380, 80, 90, 44, ACCENT_SOFT, "Embed")}
  {box(490, 80, 120, 44, SAND, "Vector + meta")}
  <path d="M140 102 H155" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  <path d="M250 102 H265" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  <path d="M360 102 H375" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  <path d="M470 102 H485" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  <text x="40" y="175" font-family="{MONO}" font-size="12" fill="{ACCENT}">QUERY (online, &lt;2–3s)</text>
  {box(40, 190, 100, 44, SAND, "Question")}
  {box(160, 190, 100, 44, ROSE, "Rewrite")}
  {box(280, 190, 110, 44, ACCENT_SOFT, "Hybrid retrieve")}
  {box(410, 190, 90, 44, "#fff", "Rerank")}
  {box(520, 190, 110, 44, SAND, "Ground LLM")}
  {box(650, 190, 110, 44, ROSE, "Cite + stream")}
  <path d="M140 212 H155" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  <path d="M260 212 H275" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  <path d="M390 212 H405" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  <path d="M500 212 H515" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  <path d="M630 212 H645" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  {box(280, 260, 110, 40, ROSE, "ACL filter", "at retrieve")}
  {box(410, 260, 90, 40, ACCENT_SOFT, "Abstain", "low conf.")}
  <path d="M335 234 V255" stroke="{INK}" stroke-width="1.2"/>
  <path d="M455 234 V255" stroke="{INK}" stroke-width="1.2"/>
  {caption(40, 335, "Separate ingest from query. Filter permissions in retrieval — never only in the prompt.")}
''',
    "RAG interview whiteboard",
)

DIAGRAMS["hybrid-search"] = svg(
    820,
    300,
    f'''
  {box(40, 120, 120, 50, SAND, "Query")}
  {box(220, 70, 140, 48, ACCENT_SOFT, "BM25 / lexical")}
  {box(220, 160, 140, 48, ROSE, "Dense / ANN")}
  {box(420, 115, 140, 50, "#fff", "Fuse (RRF)")}
  {box(620, 115, 140, 50, SAND, "Rerank top-n")}
  <path d="M165 145 H215" stroke="{INK}" stroke-width="1.4"/>
  <path d="M200 145 V94 H215" fill="none" stroke="{INK}" stroke-width="1.3"/>
  <path d="M200 145 V184 H215" fill="none" stroke="{INK}" stroke-width="1.3"/>
  <path d="M365 94 H390 V140 H415" fill="none" stroke="{INK}" stroke-width="1.3"/>
  <path d="M365 184 H390 V140" fill="none" stroke="{INK}" stroke-width="1.3"/>
  <path d="M565 140 H615" stroke="{INK}" stroke-width="1.4" marker-end="url(#arrowhead)"/>
  {caption(40, 260, "Lexical catches IDs & rare tokens; dense catches paraphrases; fuse then rerank.")}
''',
    "Hybrid retrieval",
)

DIAGRAMS["eval-pipeline"] = svg(
    820,
    320,
    f'''
  {box(40, 90, 130, 50, SAND, "Gold sets")}
  {box(200, 90, 140, 50, ROSE, "Candidate run")}
  {box(370, 70, 150, 44, ACCENT_SOFT, "Auto metrics")}
  {box(370, 130, 150, 44, "#fff", "LLM judge")}
  {box(560, 90, 140, 50, SAND, "Gate vs baseline")}
  {box(720, 90, 60, 50, ROSE, "Ship?")}
  <path d="M175 115 H195" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  <path d="M345 115 H365" stroke="{INK}" stroke-width="1.3"/>
  <path d="M525 115 H555" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  <path d="M705 115 H715" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  {box(40, 210, 160, 48, ACCENT_SOFT, "Online: A/B")}
  {box(230, 210, 160, 48, "#fff", "Traces + feedback")}
  {box(420, 210, 180, 48, ROSE, "Human spot-check")}
  <path d="M630 140 V180 H120 V205" fill="none" stroke="{ACCENT}" stroke-width="1.3" stroke-dasharray="4 3"/>
  {caption(40, 295, "Offline gates block bad deploys; online + humans catch what metrics miss.")}
''',
    "LLM evaluation pipeline",
)

DIAGRAMS["agent-tools"] = svg(
    820,
    340,
    f'''
  {box(40, 100, 110, 48, SAND, "User goal")}
  {box(180, 100, 130, 48, ROSE, "Planner LLM")}
  {box(350, 60, 130, 40, ACCENT_SOFT, "search_*")}
  {box(350, 115, 130, 40, ACCENT_SOFT, "hold / book")}
  {box(350, 170, 130, 40, "#fff", "pay (gated)")}
  {box(530, 100, 130, 48, SAND, "Tool runtime")}
  {box(690, 100, 100, 48, ROSE, "APIs")}
  <path d="M155 124 H175" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  <path d="M315 124 H345" stroke="{INK}" stroke-width="1.3"/>
  <path d="M485 80 H510 V124 H525" fill="none" stroke="{INK}" stroke-width="1.2"/>
  <path d="M485 135 H525" stroke="{INK}" stroke-width="1.2"/>
  <path d="M485 190 H510 V124" fill="none" stroke="{INK}" stroke-width="1.2"/>
  <path d="M665 124 H685" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  {box(180, 240, 160, 44, ROSE, "Confirm UI", "before pay/book")}
  {box(370, 240, 160, 44, ACCENT_SOFT, "Budgets", "steps / $ / tokens")}
  {box(560, 240, 160, 44, "#fff", "Audit log")}
  {caption(40, 315, "Tools are the product. Schema-validate args; gate irreversible actions; cap loops.")}
''',
    "Tool-using agent",
)

DIAGRAMS["memory-tiers"] = svg(
    820,
    300,
    f'''
  {box(40, 110, 160, 70, SAND, "Short-term", "thread window")}
  {box(240, 110, 160, 70, ROSE, "Working state", "slots / summary")}
  {box(440, 110, 160, 70, ACCENT_SOFT, "Long-term facts", "editable store")}
  {box(640, 110, 140, 70, "#fff", "Semantic recall", "embeddings")}
  <path d="M205 145 H235" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  <path d="M405 145 H435" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  <path d="M605 145 H635" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  {caption(40, 230, "Do not dump months of chat into the prompt — retrieve the right memories each turn.")}
  {caption(40, 255, "User must be able to see, edit, and delete long-term memory.")}
''',
    "Assistant memory tiers",
)

DIAGRAMS["moderation-cascade"] = svg(
    820,
    280,
    f'''
  {box(40, 110, 100, 50, SAND, "Content")}
  {box(170, 110, 120, 50, ROSE, "Hash / rules")}
  {box(320, 110, 130, 50, ACCENT_SOFT, "Classifiers")}
  {box(480, 110, 130, 50, "#fff", "LLM (gray)")}
  {box(640, 70, 130, 40, ROSE, "Auto action")}
  {box(640, 130, 130, 40, SAND, "Human queue")}
  {box(640, 190, 130, 40, ACCENT_SOFT, "Allow")}
  <path d="M145 135 H165" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  <path d="M295 135 H315" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  <path d="M455 135 H475" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  <path d="M615 135 H635" stroke="{INK}" stroke-width="1.2"/>
  {caption(40, 255, "Cheap filters first; LLM only on uncertain band; humans for high-severity appeals.")}
''',
    "Moderation cascade",
)

DIAGRAMS["recsys-towers"] = svg(
    820,
    300,
    f'''
  {box(40, 80, 140, 48, SAND, "User features")}
  {box(40, 180, 140, 48, SAND, "Item features")}
  {box(230, 80, 140, 48, ROSE, "User tower")}
  {box(230, 180, 140, 48, ROSE, "Item tower")}
  {box(420, 130, 140, 48, ACCENT_SOFT, "ANN retrieve")}
  {box(610, 130, 150, 48, "#fff", "Ranker → top N")}
  <path d="M185 104 H225" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  <path d="M185 204 H225" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  <path d="M375 104 H395 V154 H415" fill="none" stroke="{INK}" stroke-width="1.2"/>
  <path d="M375 204 H395 V154" fill="none" stroke="{INK}" stroke-width="1.2"/>
  <path d="M565 154 H605" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  {caption(40, 270, "Retrieve thousands cheaply with towers; spend compute only on ranking candidates.")}
''',
    "Two-tower recommendations",
)

DIAGRAMS["multi-tenant-ai"] = svg(
    820,
    300,
    f'''
  {box(40, 120, 110, 50, SAND, "Tenant A")}
  {box(40, 190, 110, 50, SAND, "Tenant B")}
  {box(200, 145, 140, 50, ROSE, "API gateway", "auth + quota")}
  {box(390, 100, 140, 44, ACCENT_SOFT, "Model router")}
  {box(390, 160, 140, 44, "#fff", "Meter / bill")}
  {box(390, 220, 140, 44, SAND, "Trace store")}
  {box(580, 145, 180, 50, ROSE, "Providers / models")}
  <path d="M155 145 H195" stroke="{INK}" stroke-width="1.2"/>
  <path d="M155 215 H175 V170 H195" fill="none" stroke="{INK}" stroke-width="1.2"/>
  <path d="M345 170 H385" stroke="{INK}" stroke-width="1.2"/>
  <path d="M535 170 H575" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  {caption(40, 280, "Quotas and tenancy are product features — not afterthoughts on the LLM call.")}
''',
    "Multi-tenant AI platform",
)

DIAGRAMS["transcription-ai"] = svg(
    820,
    280,
    f'''
  {box(40, 110, 100, 50, SAND, "Audio")}
  {box(170, 110, 120, 50, ROSE, "Streaming ASR")}
  {box(320, 110, 120, 50, ACCENT_SOFT, "Diarize")}
  {box(470, 70, 140, 44, "#fff", "Live captions")}
  {box(470, 140, 140, 44, SAND, "LLM summary")}
  {box(640, 110, 130, 50, ROSE, "Search index")}
  <path d="M145 135 H165" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  <path d="M295 135 H315" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  <path d="M445 135 H465" stroke="{INK}" stroke-width="1.2"/>
  <path d="M615 135 H635" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  {caption(40, 240, "Stream partials for UX; batch structured notes; index for later search.")}
''',
    "Realtime transcription + summary",
)

DIAGRAMS["grounded-support"] = svg(
    820,
    300,
    f'''
  {box(40, 130, 110, 48, SAND, "Ticket")}
  {box(180, 130, 130, 48, ROSE, "Intent route")}
  {box(350, 70, 150, 48, ACCENT_SOFT, "RAG policies")}
  {box(350, 160, 150, 48, "#fff", "Action tools")}
  {box(540, 70, 140, 48, SAND, "Cited answer")}
  {box(540, 160, 140, 48, ROSE, "Authz + caps")}
  {box(720, 115, 70, 48, ACCENT_SOFT, "Human")}
  <path d="M155 154 H175" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  <path d="M315 154 H330 V94 H345" fill="none" stroke="{INK}" stroke-width="1.2"/>
  <path d="M315 154 H330 V184 H345" fill="none" stroke="{INK}" stroke-width="1.2"/>
  <path d="M505 94 H535" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  <path d="M505 184 H535" stroke="{INK}" stroke-width="1.3" marker-end="url(#arrowhead)"/>
  <path d="M685 154 H715" stroke="{INK}" stroke-width="1.2" marker-end="url(#arrowhead)"/>
  {caption(40, 260, "Knowledge path cites policy; action path is deterministic server auth — not LLM vibes.")}
''',
    "Grounded support bot",
)

DIAGRAMS["prefix-sums"] = svg(
    720,
    260,
    f'''
  <text x="60" y="90" font-family="{SANS}" font-size="13" fill="{SOFT}">array</text>
  {"".join(box(60 + i*70, 100, 58, 44, "#fff", str(v)) for i,v in enumerate([3,1,4,1,5]))}
  <text x="60" y="175" font-family="{SANS}" font-size="13" fill="{SOFT}">prefix</text>
  {"".join(box(60 + i*58, 185, 50, 40, ACCENT_SOFT if i else ROSE, str(v)) for i,v in enumerate([0,3,4,8,9,14]))}
  {caption(60, 245, "sum(1..3) = prefix[4] - prefix[1] = 9 - 3 = 6")}
''',
    "Prefix sums",
)

# Map chapter id -> diagram keys (ordered)
CHAPTER_DIAGRAMS = {
    "03-arrays": ["hash-map", "prefix-sums"],
    "04-two-pointers": ["two-pointers"],
    "05-sliding-window": ["sliding-window"],
    "06-stack": ["stack"],
    "07-binary-search": ["binary-search"],
    "08-linked-lists": ["linked-list"],
    "09-trees": ["tree-bst"],
    "10-heaps": ["heap"],
    "11-backtracking": ["backtracking"],
    "12-graphs": ["bfs-graph"],
    "13-dp": ["dp-table"],
    "15-intervals": ["intervals"],
    "16-bits": ["bits-xor"],
    "21-scaling": ["load-balancer"],
    "22-caching": ["cache-cdn"],
    "23-databases": ["sql-nosql"],
    "24-replication": ["replication"],
    "25-cap": ["cap"],
    "26-queues": ["queue"],
    "28-url-shortener": ["url-shortener"],
    "29-whatsapp": ["chat-flow"],
    "30-instagram": ["feed-fanout"],
    "32-s3": ["object-storage"],
    "33-youtube": ["video-pipeline"],
    "34-uber": ["geo-matching"],
    "35-llms": ["llm-flow"],
    "37-rag": ["rag"],
    "38-memory": ["memory"],
    "39-agents": ["agent-loop"],
    "40-mcp": ["mcp"],
    "41-skills": ["skills"],
    "42-ai-agent": ["ai-assistant"],
    "interview-ai": [
        "rag-detailed",
        "hybrid-search",
        "eval-pipeline",
        "agent-tools",
        "memory-tiers",
        "moderation-cascade",
        "recsys-towers",
        "multi-tenant-ai",
        "transcription-ai",
        "grounded-support",
    ],
}


def main() -> None:
    for p in OUT.glob("diagram-p*.jpg"):
        p.unlink()
    for p in OUT.glob("*.svg"):
        p.unlink()

    for key, content in DIAGRAMS.items():
        path = OUT / f"{key}.svg"
        path.write_text(content)
        print("wrote", path.name)

    import json

    (OUT / "manifest.json").write_text(
        json.dumps({"diagrams": list(DIAGRAMS.keys()), "chapters": CHAPTER_DIAGRAMS}, indent=2)
    )
    print("manifest diagrams:", len(DIAGRAMS))


if __name__ == "__main__":
    main()
