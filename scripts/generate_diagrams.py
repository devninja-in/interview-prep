#!/usr/bin/env python3
"""Generate professional SVG diagrams for interview prep chapters.

The diagrams intentionally share a restrained visual language:
dark title bar, paper background, role-colored components, orthogonal
connectors, and terse interview-takeaway footers.
"""
from __future__ import annotations

import html
import json
from pathlib import Path

from diagram_kit import (
    FILL_APP,
    FILL_CACHE,
    FILL_HL,
    FILL_HL_SOFT,
    FILL_QUEUE,
    FILL_WARN,
    INK,
    LINE,
    LINE_STRONG,
    MONO,
    MUTED,
    SANS,
    ZONE_APP,
    ZONE_ASYNC,
    ZONE_CLIENT,
    ZONE_DATA,
    ZONE_EDGE,
    Canvas,
    arrow,
    badge,
    callout,
    cell,
    elbow,
    label,
    mid_of,
    node,
    path_line,
    zone,
)

OUT = Path(__file__).resolve().parents[1] / "assets" / "diagrams"
OUT.mkdir(parents=True, exist_ok=True)

# Keep diagram code compact while still calling the kit node primitive.
kit_node = node


def node(
    x,
    y,
    w,
    h,
    label_text: str,
    sub: str = "",
    *,
    kind: str = "app",
    mid: str = "d",
    rx: int = 6,
) -> str:
    return kit_node(x, y, w, h, label_text, sub=sub, kind=kind, mid=mid, rx=rx)


REQUIRED_KEYS = [
    "agent-loop",
    "agent-tools",
    "agentic-rag",
    "ai-assistant",
    "autocomplete-trie",
    "backtracking",
    "bfs-graph",
    "binary-search",
    "bits-xor",
    "cache-cdn",
    "cap",
    "chat-flow",
    "chat-message-path",
    "code-copilot",
    "coin-change-dp",
    "consistent-hash-cache",
    "dp-table",
    "dropbox-sync",
    "eval-pipeline",
    "feature-store",
    "feed-fanout",
    "feed-hybrid-fanout",
    "geo-matching",
    "grounded-support",
    "hash-map",
    "heap",
    "hybrid-search",
    "intervals",
    "islands-dfs",
    "kadane",
    "kafka-partitions",
    "leaderboard",
    "linked-list",
    "llm-flow",
    "llm-serving",
    "load-balancer",
    "longest-substr-window",
    "lru-cache",
    "mcp",
    "meeting-rooms",
    "memory",
    "memory-tiers",
    "merge-intervals-walk",
    "min-window",
    "moderation-cascade",
    "multi-tenant-ai",
    "notification-pipeline",
    "object-storage",
    "payment-saga",
    "prefix-sums",
    "queue",
    "rag",
    "rag-detailed",
    "rate-limiter-token",
    "recsys-towers",
    "replication",
    "rotated-search",
    "rotting-oranges",
    "semantic-cache",
    "serialize-tree",
    "skills",
    "sliding-window",
    "sql-nosql",
    "stack",
    "stock-profit",
    "ticket-hold-checkout",
    "top-k-buckets",
    "topo-kahn",
    "transcription-ai",
    "trap-water",
    "tree-bst",
    "two-pointers",
    "two-sum-walk",
    "uber-matching",
    "url-shortener",
    "url-shortener-detailed",
    "video-pipeline",
    "web-crawler",
    "word-ladder-bfs",
    "youtube-cdn-pipeline",
]

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
    "interview-cp": [
        "two-sum-walk",
        "longest-substr-window",
        "merge-intervals-walk",
        "lru-cache",
        "islands-dfs",
        "topo-kahn",
        "coin-change-dp",
        "word-ladder-bfs",
        "serialize-tree",
        "trap-water",
        "stock-profit",
        "min-window",
        "kadane",
        "rotated-search",
        "top-k-buckets",
        "meeting-rooms",
        "rotting-oranges",
    ],
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
        "llm-serving",
        "agentic-rag",
        "semantic-cache",
        "code-copilot",
        "feature-store",
    ],
    "interview-sd": [
        "url-shortener-detailed",
        "feed-hybrid-fanout",
        "chat-message-path",
        "rate-limiter-token",
        "uber-matching",
        "youtube-cdn-pipeline",
        "notification-pipeline",
        "autocomplete-trie",
        "consistent-hash-cache",
        "ticket-hold-checkout",
        "dropbox-sync",
        "web-crawler",
        "payment-saga",
        "leaderboard",
        "kafka-partitions",
    ],
}


def esc(text: object) -> str:
    return html.escape(str(text), quote=True)


def fmt(v: object) -> str:
    if isinstance(v, (int, float)):
        if abs(v - round(v)) < 1e-9:
            return str(int(round(v)))
        return f"{v:.1f}".rstrip("0").rstrip(".")
    return str(v)


def text(
    x: float,
    y: float,
    body: str,
    *,
    size: int = 12,
    weight: str = "500",
    fill: str = INK,
    mono: bool = False,
    anchor: str = "start",
) -> str:
    fam = MONO if mono else SANS
    return (
        f'<text x="{fmt(x)}" y="{fmt(y)}" text-anchor="{anchor}" font-family="{fam}" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}">{esc(body)}</text>'
    )


def text_lines(
    x: float,
    y: float,
    lines: list[str],
    *,
    size: int = 12,
    gap: int = 15,
    fill: str = MUTED,
    mono: bool = False,
) -> str:
    return "\n".join(text(x, y + i * gap, line, size=size, fill=fill, mono=mono) for i, line in enumerate(lines))


def edge_label(x: float, y: float, body: str, *, accent: bool = False) -> str:
    if not body:
        return ""
    w = max(36, len(body) * 6.2 + 14)
    fill = "#ffffff"
    stroke = FILL_HL if accent else LINE
    return (
        f'<rect x="{fmt(x - w / 2)}" y="{fmt(y - 14)}" width="{fmt(w)}" height="20" rx="10" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
        + text(x, y, body, size=10, fill=FILL_HL if accent else MUTED, mono=True, anchor="middle")
    )


LANES = {
    "CLIENT": (28, 64, 140, 410, ZONE_CLIENT),
    "EDGE": (182, 64, 150, 410, ZONE_EDGE),
    "SERVICE": (346, 64, 198, 410, ZONE_APP),
    "ASYNC": (558, 64, 164, 410, ZONE_ASYNC),
    "DATA": (736, 64, 236, 410, ZONE_DATA),
}

NODE_W = {"CLIENT": 108, "EDGE": 118, "SERVICE": 152, "ASYNC": 124, "DATA": 142}


def n(
    ident: str,
    lane: str,
    row: float,
    title: str,
    sub: str = "",
    kind: str = "app",
    *,
    dx: float = 0,
    w: int | None = None,
    h: int = 56,
) -> dict[str, object]:
    return {
        "id": ident,
        "lane": lane,
        "row": row,
        "title": title,
        "sub": sub,
        "kind": kind,
        "dx": dx,
        "w": w,
        "h": h,
    }


def f(
    src: str,
    dst: str,
    label_text: str = "",
    step: int | str | None = None,
    *,
    accent: bool = False,
    dashed: bool = False,
    via: str = "hv",
) -> dict[str, object]:
    return {
        "src": src,
        "dst": dst,
        "label": label_text,
        "step": step,
        "accent": accent,
        "dashed": dashed,
        "via": via,
    }


def _node_box(spec: dict[str, object]) -> tuple[float, float, float, float]:
    lane = str(spec["lane"])
    zx, zy, zw, _zh, _fill = LANES[lane]
    w = float(spec["w"] or NODE_W[lane])
    h = float(spec["h"])
    x = zx + (zw - w) / 2 + float(spec["dx"])
    y = zy + 42 + float(spec["row"]) * 78
    return x, y, w, h


def _anchors(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    acx, acy = ax + aw / 2, ay + ah / 2
    bcx, bcy = bx + bw / 2, by + bh / 2
    if abs(bcx - acx) >= abs(bcy - acy):
        if bcx >= acx:
            return ax + aw, acy, bx, bcy
        return ax, acy, bx + bw, bcy
    if bcy >= acy:
        return acx, ay + ah, bcx, by
    return acx, ay, bcx, by + bh


def system_diagram(
    title: str,
    note: str,
    nodes: list[dict[str, object]],
    flows: list[dict[str, object]],
    *,
    callouts: list[tuple[int, int, int, int, str, str]] | None = None,
) -> str:
    mid = mid_of(title)
    boxes: dict[str, tuple[float, float, float, float]] = {}
    parts: list[str] = [
        zone(x, y, w, h, lane, fill) for lane, (x, y, w, h, fill) in LANES.items()
    ]
    for spec in nodes:
        x, y, w, h = _node_box(spec)
        boxes[str(spec["id"])] = (x, y, w, h)
        parts.append(
            node(
                x,
                y,
                w,
                h,
                str(spec["title"]),
                sub=str(spec["sub"]),
                kind=str(spec["kind"]),
                mid=mid,
            )
        )
    badge_counts: dict[str, int] = {}
    for flow in flows:
        x1, y1, x2, y2 = _anchors(boxes[str(flow["src"])], boxes[str(flow["dst"])])
        parts.append(
            elbow(
                x1,
                y1,
                x2,
                y2,
                mid=mid,
                via=str(flow["via"]),
                accent=bool(flow["accent"]),
                dashed=bool(flow["dashed"]),
            )
        )
        lx, ly = (x1 + x2) / 2, (y1 + y2) / 2 - 4
        parts.append(edge_label(lx, ly, str(flow["label"]), accent=bool(flow["accent"])))
        if flow["step"] is not None:
            src = str(flow["src"])
            fanout = badge_counts.get(src, 0)
            badge_counts[src] = fanout + 1
            bx = x1 + (x2 - x1) * 0.14 + (12 if x2 >= x1 else -12)
            by = y1 + (y2 - y1) * 0.14 - 14 + fanout * 17
            parts.append(badge(bx, by, flow["step"], mid=mid))
    for co in callouts or []:
        parts.append(callout(*co, mid=mid))
    return Canvas(1000, 530, title, note=note).add(*parts).render()


def simple_system(
    title: str,
    note: str,
    *,
    client: tuple[str, str] = ("Client", "mobile / web"),
    edge: tuple[str, str] = ("Gateway", "auth + routing"),
    service: tuple[str, str] = ("Service", "business logic"),
    async_node: tuple[str, str] = ("Event bus", "decouple writes"),
    data: tuple[str, str] = ("Store", "durable state"),
    extra_data: tuple[str, str] | None = None,
    labels: tuple[str, str, str, str] = ("request", "route", "publish", "persist"),
) -> str:
    nodes = [
        n("client", "CLIENT", 1, client[0], client[1], "client"),
        n("edge", "EDGE", 1, edge[0], edge[1], "edge"),
        n("service", "SERVICE", 1, service[0], service[1], "app"),
        n("async", "ASYNC", 1, async_node[0], async_node[1], "queue"),
        n("data", "DATA", 0.45 if extra_data else 1, data[0], data[1], "store", dx=-38 if extra_data else 0),
    ]
    if extra_data:
        nodes.append(n("data2", "DATA", 1.75, extra_data[0], extra_data[1], "cache", dx=38))
    flows = [
        f("client", "edge", labels[0], 1),
        f("edge", "service", labels[1], 2),
        f("service", "async", labels[2], 3, accent=True),
        f("async", "data", labels[3], 4),
    ]
    if extra_data:
        flows.append(f("service", "data2", "read-through", "R", dashed=True))
    return system_diagram(title, note, nodes, flows)


def array_row(
    values: list[object],
    *,
    x: int,
    y: int,
    w: int = 50,
    h: int = 44,
    active: set[int] | list[int] | range = (),
    soft: set[int] | list[int] | range = (),
    pointers: dict[int, str] | None = None,
    indexes: bool = True,
    mid: str,
) -> str:
    active_set, soft_set = set(active), set(soft)
    pointers = pointers or {}
    parts: list[str] = []
    for i, value in enumerate(values):
        cx = x + i * (w + 8)
        parts.append(cell(cx, y, w, h, value, active=i in active_set, soft=i in soft_set, mid=mid))
        if indexes:
            parts.append(text(cx + w / 2, y + h + 17, str(i), size=10, fill=MUTED, mono=True, anchor="middle"))
        if i in pointers:
            parts.append(text(cx + w / 2, y - 18, pointers[i], size=11, fill=FILL_HL, mono=True, anchor="middle"))
            parts.append(path_line(f"M{cx + w / 2} {y - 13} V{y - 2}", mid=mid, accent=True))
    return "\n".join(parts)


def mini_node(x: int, y: int, name: str, *, active: bool = False, soft: bool = False, mid: str) -> str:
    fill = FILL_HL if active else (FILL_HL_SOFT if soft else "#ffffff")
    stroke = FILL_HL if active else LINE_STRONG
    tc = "#ffffff" if active else INK
    return (
        f'<circle cx="{x}" cy="{y}" r="24" fill="{fill}" stroke="{stroke}" stroke-width="1.5" filter="url(#sh-{mid})"/>'
        + text(x, y + 5, name, size=12, weight="700", fill=tc, mono=True, anchor="middle")
    )


def matrix_grid(
    values: list[list[object]],
    *,
    x: int,
    y: int,
    active: set[tuple[int, int]] = frozenset(),
    soft: set[tuple[int, int]] = frozenset(),
    mid: str,
    size: int = 42,
) -> str:
    parts: list[str] = []
    for r, row in enumerate(values):
        for c, value in enumerate(row):
            parts.append(cell(x + c * (size + 6), y + r * (size + 6), size, size, value, active=(r, c) in active, soft=(r, c) in soft, mid=mid))
    return "\n".join(parts)


def bars(values: list[int], *, x: int, baseline: int, scale: int, active: set[int], soft: set[int], mid: str) -> str:
    parts: list[str] = []
    for i, value in enumerate(values):
        h = value * scale
        bx = x + i * 42
        fill = FILL_HL if i in active else (FILL_HL_SOFT if i in soft else "#ffffff")
        parts.append(
            f'<rect x="{bx}" y="{baseline - h}" width="30" height="{h}" rx="3" fill="{fill}" '
            f'stroke="{LINE_STRONG}" stroke-width="1.2" filter="url(#sh-{mid})"/>'
        )
        parts.append(text(bx + 15, baseline + 16, str(value), size=10, fill=MUTED, mono=True, anchor="middle"))
    return "\n".join(parts)


def interval_bar(x: int, y: int, start: int, end: int, label_text: str, *, active: bool, mid: str) -> str:
    sx, ex = x + start * 48, x + end * 48
    fill = FILL_HL_SOFT if active else "#ffffff"
    stroke = FILL_HL if active else LINE_STRONG
    return (
        f'<line x1="{x}" y1="{y + 26}" x2="{x + 360}" y2="{y + 26}" stroke="{LINE}" stroke-width="1"/>'
        f'<rect x="{sx}" y="{y}" width="{ex - sx}" height="34" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.4" filter="url(#sh-{mid})"/>'
        + text((sx + ex) / 2, y + 22, label_text, size=11, weight="650", fill=INK, anchor="middle")
    )


ALGO_META: dict[str, tuple[str, str, str]] = {
    "Hash map lookup": ("bucket = hash(key) % m", "load factor stays bounded", "avg O(1), resize O(n)"),
    "Two pointers": ("L=0, R=n-1, target=9", "pointers only move inward", "O(n) time, O(1) space"),
    "Sliding window": ("freq map + L/R bounds", "window always valid after shrink", "O(n), each index moves once"),
    "Stack": ("top pointer on C", "only top is mutable", "push/pop O(1)"),
    "Binary search": ("lo=0, hi=6, mid=3", "answer remains inside range", "O(log n), O(1)"),
    "Linked list reverse": ("prev, cur, next", "reversed prefix points back", "O(n) time, O(1) space"),
    "Binary search tree": ("node=8, bounds=(-inf,inf)", "left < node < right recursively", "O(h), worst O(n)"),
    "Heap / priority queue": ("array-backed complete tree", "parent priority <= children", "push/pop O(log n)"),
    "Backtracking loop": ("path + remaining choices", "undo every mutation", "exponential; prune early"),
    "Graph BFS layers": ("queue + visited set", "first visit is shortest depth", "O(V+E)"),
    "Dynamic programming table": ("dp[i] stores solved prefix", "compute dependencies first", "states x transitions"),
    "Intervals": ("sorted by start", "current interval is merged prefix", "O(n log n) sort"),
    "Bits and XOR": ("bit columns for a and b", "same bits cancel under XOR", "O(bits), O(1)"),
    "Prefix sums": ("prefix[i] sum before i", "prefix is cumulative", "build O(n), query O(1)"),
    "Two sum walk": ("seen map: value -> index", "complement checked before insert", "O(n) time, O(n) space"),
    "Longest substring window": ("last_seen + L/R", "no duplicate inside window", "O(n), alphabet map"),
    "Merge intervals walk": ("current=[1,4], next=[3,6]", "merged output never overlaps", "O(n log n)"),
    "LRU cache": ("map + doubly linked list", "MRU left, LRU right", "get/put O(1)"),
    "Number of islands DFS": ("grid cell + visited", "DFS consumes one island", "O(R*C)"),
    "Topological sort - Kahn": ("indegree map + zero queue", "output has no unmet prereqs", "O(V+E)"),
    "Coin change DP": ("dp[amount] min coins", "relax from smaller amounts", "O(amount * coins)"),
    "Word ladder BFS": ("frontier by word distance", "first target hit is shortest", "O(N * word_len^2)"),
    "Serialize binary tree": ("preorder token cursor", "# marks null children", "O(n) encode/decode"),
    "Trapping rain water": ("leftMax/rightMax", "smaller wall bounds water", "O(n) time, O(1) space"),
    "Best time to buy/sell stock": ("min_price so far", "sell after buy only", "O(n), one pass"),
    "Minimum window substring": ("need/have counts + L/R", "valid iff formed == required", "O(|s|+|t|)"),
    "Kadane maximum subarray": ("current sum, best sum", "negative prefix is discarded", "O(n), O(1)"),
    "Search rotated sorted array": ("lo/mid/hi + target", "one half is always sorted", "O(log n)"),
    "Top K frequent buckets": ("count map + buckets", "bucket i holds freq i", "O(n) time"),
    "Meeting rooms sweep": ("min-heap of end times", "heap holds active meetings", "O(n log n)"),
    "Rotting oranges BFS": ("multi-source queue", "minute = BFS layer", "O(R*C)"),
    "Autocomplete trie": ("prefix cursor at node", "path spells prefix", "O(prefix + k)"),
}


def state_panel(x: int, y: int, w: int, items: tuple[str, str, str], *, mid: str) -> str:
    headings = ("STATE", "INVARIANT", "COMPLEXITY")
    col = w / 3
    parts = [
        f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="82" rx="8" fill="#ffffff" stroke="{LINE}" stroke-width="1.2" filter="url(#sh-{mid})"/>'
    ]
    for i, (heading, body) in enumerate(zip(headings, items)):
        cx = x + i * col
        if i:
            parts.append(f'<line x1="{fmt(cx)}" y1="{fmt(y + 12)}" x2="{fmt(cx)}" y2="{fmt(y + 70)}" stroke="{LINE}" stroke-width="1"/>')
        parts.append(text(cx + 14, y + 25, heading, size=10, weight="700", fill=FILL_HL, mono=True))
        parts.append(text(cx + 14, y + 49, body, size=11, weight="550", fill=INK, mono=False))
    return "\n".join(parts)


def algorithm_canvas(title: str, note: str, *parts: str, w: int = 900, h: int = 360) -> str:
    chunks = list(parts)
    meta = ALGO_META.get(title)
    if meta:
        h = max(h, 450)
        chunks.append(state_panel(48, h - 132, w - 96, meta, mid=mid_of(title)))
    return Canvas(w, h, title, note=note).add(*chunks).render()


def hash_map() -> str:
    title = "Hash map lookup"
    mid = mid_of(title)
    parts = [
        node(48, 110, 110, 54, 'key="apple"', "stable hash", kind="client", mid=mid),
        node(220, 110, 120, 54, "hash(key)", "mod buckets", kind="app", mid=mid),
        arrow(162, 137, 215, 137, mid=mid, accent=True),
        array_row(["0", "1", "2", "3"], x=400, y=84, w=58, h=44, active={1}, soft={2}, pointers={}, mid=mid),
        node(646, 92, 132, 44, "value", "profile row", kind="store", mid=mid),
        node(646, 160, 132, 44, "collision", "chain/probe", kind="warn", mid=mid),
        elbow(636, 106, 545, 106, mid=mid, via="vh", accent=True),
        edge_label(592, 100, "bucket[1]", accent=True),
        callout(48, 230, 355, 64, "invariant", "Average O(1) depends on low load factor and good hashing.", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: state the hash, collision strategy, and resize threshold.", *parts)


def two_pointers() -> str:
    title = "Two pointers"
    mid = mid_of(title)
    parts = [
        array_row([1, 2, 3, 4, 6, 8], x=90, y=132, active={0, 5}, soft={1, 2, 3, 4}, pointers={0: "L", 5: "R"}, mid=mid),
        path_line("M115 212 H405", mid=mid, accent=True, arrow=False),
        text(260, 240, "sum = 1 + 8; move L right if too small, R left if too large", size=12, fill=MUTED, mono=True, anchor="middle"),
        callout(560, 116, 260, 80, "whiteboard note", "Sorted input lets each pointer move once: O(n).", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: monotonic movement is the proof that this stays linear.", *parts)


def sliding_window() -> str:
    title = "Sliding window"
    mid = mid_of(title)
    parts = [
        array_row(list("A B C A C B".split()), x=86, y=128, active={2, 3, 4}, soft={1, 5}, pointers={2: "L", 4: "R"}, mid=mid),
        f'<rect x="198" y="118" width="166" height="64" rx="8" fill="none" stroke="{FILL_HL}" stroke-width="2"/>',
        callout(520, 108, 270, 96, "loop shape", "Expand R to include a candidate; shrink L until the constraint is valid.", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: maintain the answer incrementally instead of rescanning the window.", *parts)


def stack() -> str:
    title = "Stack"
    mid = mid_of(title)
    parts = [
        cell(120, 204, 130, 42, "A", soft=True, mid=mid),
        cell(120, 156, 130, 42, "B", soft=True, mid=mid),
        cell(120, 108, 130, 42, "C", active=True, mid=mid),
        text(270, 132, "top", size=12, fill=FILL_HL, mono=True),
        arrow(260, 128, 250, 128, mid=mid, accent=True),
        node(455, 96, 160, 52, "push(x)", "add above top", kind="app", mid=mid),
        node(455, 176, 160, 52, "pop()", "remove top", kind="app", mid=mid),
        callout(76, 274, 430, 48, "pattern", "Use stacks for matching, rollback, monotonic next-greater scans.", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: LIFO gives O(1) local state for nested or monotonic problems.", *parts)


def binary_search() -> str:
    title = "Binary search"
    mid = mid_of(title)
    parts = [
        array_row([2, 4, 6, 8, 10, 12, 14], x=72, y=132, active={3}, soft={0, 1, 2}, pointers={0: "lo", 3: "mid", 6: "hi"}, mid=mid),
        edge_label(180, 114, "discard left half?"),
        callout(560, 108, 270, 96, "decision", "Compare target with mid, then keep the sorted half that can contain it.", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: define inclusive/exclusive bounds before writing the loop.", *parts)


def linked_list() -> str:
    title = "Linked list reverse"
    mid = mid_of(title)
    parts = [
        node(70, 126, 72, 48, "1", "prev", kind="hl", mid=mid),
        node(190, 126, 72, 48, "2", "cur", kind="app", mid=mid),
        node(310, 126, 72, 48, "3", "next", kind="app", mid=mid),
        arrow(142, 150, 185, 150, mid=mid),
        arrow(262, 150, 305, 150, mid=mid),
        node(540, 126, 120, 48, "reverse", "cur.next = prev", kind="warn", mid=mid),
        elbow(540, 150, 382, 150, mid=mid, via="hv", accent=True),
        callout(72, 246, 470, 52, "safe order", "Save next before rewiring; then advance prev and cur.", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: pointer problems are mostly about update order.", *parts)


def tree_bst() -> str:
    title = "Binary search tree"
    mid = mid_of(title)
    parts = [
        mini_node(430, 98, "8", active=True, mid=mid),
        mini_node(300, 178, "3", soft=True, mid=mid),
        mini_node(560, 178, "10", soft=True, mid=mid),
        mini_node(230, 260, "1", mid=mid),
        mini_node(370, 260, "6", mid=mid),
        path_line("M414 116 L318 160", mid=mid, arrow=False),
        path_line("M446 116 L542 160", mid=mid, arrow=False),
        path_line("M286 196 L244 242", mid=mid, arrow=False),
        path_line("M314 196 L356 242", mid=mid, arrow=False),
        callout(60, 102, 220, 84, "invariant", "Every subtree obeys left < node < right.", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: carry min/max bounds; local comparisons alone miss invalid descendants.", *parts, h=390)


def heap() -> str:
    title = "Heap / priority queue"
    mid = mid_of(title)
    parts = [
        mini_node(284, 92, "1", active=True, mid=mid),
        mini_node(204, 164, "3", soft=True, mid=mid),
        mini_node(364, 164, "2", soft=True, mid=mid),
        mini_node(154, 236, "7", mid=mid),
        mini_node(254, 236, "5", mid=mid),
        path_line("M270 112 L218 146 M298 112 L350 146 M192 184 L166 218 M216 184 L242 218", mid=mid, arrow=False),
        array_row([1, 3, 2, 7, 5], x=500, y=146, active={0}, soft={1, 2}, pointers={0: "min"}, mid=mid),
        callout(500, 230, 270, 52, "operations", "push/pop restore the heap by bubbling along one path.", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: heap shape is complete; priority comes from parent-child order.", *parts, h=380)


def backtracking() -> str:
    title = "Backtracking loop"
    mid = mid_of(title)
    parts = [
        mini_node(120, 112, "start", active=True, mid=mid),
        mini_node(260, 188, "A", soft=True, mid=mid),
        mini_node(120, 188, "B", soft=True, mid=mid),
        mini_node(400, 188, "C", soft=True, mid=mid),
        path_line("M140 126 L240 174 M120 136 V164 M140 126 L380 174", mid=mid, arrow=False),
        node(560, 94, 170, 50, "choose", "append candidate", kind="app", mid=mid),
        node(560, 164, 170, 50, "explore", "recursive call", kind="hl", mid=mid),
        node(560, 234, 170, 50, "unchoose", "pop candidate", kind="warn", mid=mid),
        arrow(645, 144, 645, 160, mid=mid, accent=True),
        arrow(645, 214, 645, 230, mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: mutate state in a disciplined choose/explore/unchoose cycle.", *parts, h=380)


def bfs_graph() -> str:
    title = "Graph BFS layers"
    mid = mid_of(title)
    parts = [
        mini_node(90, 172, "A", active=True, mid=mid),
        mini_node(240, 112, "B", soft=True, mid=mid),
        mini_node(240, 232, "C", soft=True, mid=mid),
        mini_node(390, 90, "D", mid=mid),
        mini_node(390, 172, "E", mid=mid),
        mini_node(390, 254, "F", mid=mid),
        path_line("M114 162 L216 122 M114 182 L216 222 M264 112 L366 90 M264 232 L366 254 M264 122 L366 164", mid=mid, arrow=False),
        node(560, 96, 210, 52, "queue", "A | B C | D E F", kind="queue", mid=mid),
        callout(560, 178, 250, 70, "shortest path", "First visit to a node is the minimum edge count in an unweighted graph.", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: BFS is level-order traversal with a visited set.", *parts, h=380)


def dp_table() -> str:
    title = "Dynamic programming table"
    mid = mid_of(title)
    parts = [
        text(76, 104, "state", size=12, fill=MUTED, mono=True),
        array_row(["dp[0]", "dp[1]", "dp[2]", "dp[3]", "dp[4]", "dp[5]"], x=76, y=124, w=74, active={5}, soft={3, 4}, pointers={5: "answer"}, indexes=False, mid=mid),
        text(76, 212, "value", size=12, fill=MUTED, mono=True),
        array_row([0, 1, 1, 2, 3, 5], x=76, y=228, w=74, active={5}, soft={3, 4}, indexes=False, mid=mid),
        callout(630, 132, 210, 92, "transition", "dp[i] = combine(previous states); compute in dependency order.", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: name the state, base case, transition, and iteration order.", *parts, h=390)


def intervals() -> str:
    title = "Intervals"
    mid = mid_of(title)
    parts = [
        interval_bar(90, 100, 0, 3, "[1,4]", active=True, mid=mid),
        interval_bar(90, 154, 2, 5, "[3,6]", active=True, mid=mid),
        interval_bar(90, 208, 6, 7, "[7,8]", active=False, mid=mid),
        node(560, 120, 180, 56, "sort by start", "then sweep", kind="app", mid=mid),
        node(560, 210, 180, 56, "merge if", "next.start <= end", kind="hl", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: sorting turns pairwise overlap into a linear sweep.", *parts, h=370)


def bits_xor() -> str:
    title = "Bits and XOR"
    mid = mid_of(title)
    parts = [
        text(92, 106, "a", mono=True, fill=MUTED),
        array_row([1, 0, 1, 1, 0], x=130, y=86, active={0, 2, 3}, indexes=False, mid=mid),
        text(92, 170, "b", mono=True, fill=MUTED),
        array_row([0, 0, 1, 0, 1], x=130, y=150, active={2, 4}, indexes=False, mid=mid),
        text(92, 240, "a^b", mono=True, fill=FILL_HL),
        array_row([1, 0, 0, 1, 1], x=130, y=220, active={0, 3, 4}, soft={1, 2}, indexes=False, mid=mid),
        callout(560, 130, 230, 70, "property", "x ^ x = 0 and x ^ 0 = x; order does not matter.", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: XOR cancels duplicates and encodes parity.", *parts, h=360)


def prefix_sums() -> str:
    title = "Prefix sums"
    mid = mid_of(title)
    parts = [
        text(70, 114, "array", mono=True, fill=MUTED),
        array_row([3, 1, 4, 1, 5], x=150, y=92, active={1, 2, 3}, mid=mid),
        text(70, 214, "prefix", mono=True, fill=MUTED),
        array_row([0, 3, 4, 8, 9, 14], x=150, y=192, w=46, active={1, 4}, soft={2, 3}, mid=mid),
        callout(560, 140, 230, 74, "range sum", "sum[l..r] = prefix[r+1] - prefix[l]", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: precompute cumulative state to answer ranges in O(1).", *parts, h=360)


def two_sum_walk() -> str:
    title = "Two sum walk"
    mid = mid_of(title)
    parts = [
        array_row([2, 7, 11, 15], x=86, y=128, active={0, 1}, pointers={0: "i", 1: "j"}, mid=mid),
        node(420, 104, 170, 56, "target = 9", "2 + 7", kind="hl", mid=mid),
        arrow(332, 150, 415, 132, mid=mid, accent=True),
        callout(620, 104, 230, 86, "hash map pass", "Before inserting nums[i], ask whether target - nums[i] was seen.", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: one pass works because the complement is the only needed history.", *parts, h=340)


def longest_substr_window() -> str:
    title = "Longest substring window"
    mid = mid_of(title)
    chars = list("P W W K E W".split())
    parts = [
        array_row(chars, x=72, y=132, active={2, 3, 4}, soft={5}, pointers={2: "L", 4: "R"}, mid=mid),
        node(540, 105, 210, 56, "last_seen", "W -> 2, K -> 3", kind="cache", mid=mid),
        callout(540, 188, 252, 74, "on duplicate", "Move L to max(L, last_seen[c] + 1). Never move L backwards.", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: indexes in the map let the left edge jump over duplicates.", *parts)


def merge_intervals_walk() -> str:
    title = "Merge intervals walk"
    mid = mid_of(title)
    parts = [
        interval_bar(80, 90, 0, 3, "[1,4]", active=True, mid=mid),
        interval_bar(80, 142, 2, 5, "[3,6]", active=True, mid=mid),
        interval_bar(80, 226, 0, 5, "[1,6]", active=True, mid=mid),
        node(560, 116, 190, 56, "overlap", "3 <= current.end", kind="hl", mid=mid),
        arrow(260, 196, 260, 220, mid=mid, accent=True),
    ]
    return algorithm_canvas(title, "Interview takeaway: keep one current interval and extend its end greedily.", *parts, h=360)


def lru_cache() -> str:
    title = "LRU cache"
    mid = mid_of(title)
    parts = [
        node(70, 120, 140, 54, "hash map", "key -> list node", kind="cache", mid=mid),
        node(330, 90, 90, 44, "MRU", "C", kind="hl", mid=mid),
        node(460, 90, 90, 44, "B", "", kind="app", mid=mid),
        node(590, 90, 90, 44, "LRU", "A", kind="warn", mid=mid),
        arrow(420, 112, 455, 112, mid=mid),
        arrow(550, 112, 585, 112, mid=mid),
        elbow(210, 147, 330, 112, mid=mid, via="hv", accent=True),
        callout(330, 186, 300, 74, "invariant", "Reads and writes move a node to MRU; capacity eviction pops LRU.", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: hash map + doubly linked list gives O(1) get/put.", *parts)


def islands_dfs() -> str:
    title = "Number of islands DFS"
    mid = mid_of(title)
    grid = [["1", "1", "0", "0"], ["1", "0", "0", "1"], ["0", "0", "1", "1"], ["1", "0", "0", "0"]]
    parts = [
        matrix_grid(grid, x=90, y=90, active={(0, 0), (0, 1), (1, 0)}, soft={(1, 3), (2, 2), (2, 3)}, mid=mid),
        node(420, 114, 190, 56, "DFS flood fill", "mark visited water", kind="hl", mid=mid),
        callout(420, 196, 280, 70, "count rule", "Increment when you see unvisited land; DFS consumes the whole component.", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: components in grids are graph traversals with boundary checks.", *parts)


def topo_kahn() -> str:
    title = "Topological sort - Kahn"
    mid = mid_of(title)
    parts = [
        mini_node(110, 168, "A", active=True, mid=mid),
        mini_node(250, 112, "B", soft=True, mid=mid),
        mini_node(250, 224, "C", soft=True, mid=mid),
        mini_node(410, 168, "D", mid=mid),
        path_line("M134 160 L226 122 M134 176 L226 214 M274 122 L388 160 M274 214 L388 176", mid=mid, accent=True),
        node(560, 104, 210, 54, "zero indegree queue", "A, then B/C", kind="queue", mid=mid),
        node(560, 190, 210, 54, "emit order", "A B C D", kind="store", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: removing zero-indegree nodes exposes the next valid choices.", *parts)


def coin_change_dp() -> str:
    title = "Coin change DP"
    mid = mid_of(title)
    parts = [
        text(88, 96, "amount", mono=True, fill=MUTED),
        array_row(list(range(0, 8)), x=90, y=112, w=42, indexes=False, soft={0}, active={6}, mid=mid),
        text(88, 190, "min coins", mono=True, fill=MUTED),
        array_row([0, 1, 1, 2, 2, 1, 2, 2], x=90, y=206, w=42, indexes=False, soft={1, 3, 5}, active={6}, mid=mid),
        callout(560, 130, 260, 86, "transition", "dp[a] = 1 + min(dp[a-c]) for each coin c <= a.", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: initialize impossible states and relax with each allowed coin.", *parts, h=360)


def word_ladder_bfs() -> str:
    title = "Word ladder BFS"
    mid = mid_of(title)
    parts = [
        node(70, 128, 92, 42, "hit", "", kind="hl", mid=mid),
        node(222, 92, 92, 42, "hot", "", kind="app", mid=mid),
        node(374, 72, 92, 42, "dot", "", kind="app", mid=mid),
        node(374, 154, 92, 42, "lot", "", kind="app", mid=mid),
        node(526, 92, 92, 42, "dog", "", kind="app", mid=mid),
        node(678, 92, 92, 42, "cog", "", kind="store", mid=mid),
        elbow(162, 149, 222, 113, mid=mid, accent=True),
        elbow(314, 113, 374, 93, mid=mid, accent=True),
        elbow(466, 93, 526, 113, mid=mid, accent=True),
        elbow(618, 113, 678, 113, mid=mid, accent=True),
        callout(210, 236, 360, 58, "neighbor generation", "Wildcard buckets like h*t avoid comparing every word pair.", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: BFS gives shortest transformations; preprocessing makes neighbors cheap.", *parts)


def serialize_tree() -> str:
    title = "Serialize binary tree"
    mid = mid_of(title)
    parts = [
        mini_node(210, 90, "1", active=True, mid=mid),
        mini_node(130, 170, "2", soft=True, mid=mid),
        mini_node(290, 170, "3", soft=True, mid=mid),
        mini_node(250, 250, "4", mid=mid),
        mini_node(330, 250, "5", mid=mid),
        path_line("M196 110 L144 152 M224 110 L276 152 M282 192 L258 232 M298 192 L322 232", mid=mid, arrow=False),
        array_row(["1", "2", "#", "#", "3", "4", "#", "#", "5"], x=460, y=146, w=42, active={0, 4}, soft={2, 3, 6, 7}, indexes=False, mid=mid),
        callout(458, 230, 300, 52, "decoder", "Read preorder tokens recursively; # consumes a null child.", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: include null markers or structure is ambiguous.", *parts, h=380)


def trap_water() -> str:
    title = "Trapping rain water"
    mid = mid_of(title)
    parts = [
        bars([0, 3, 0, 2, 0, 4], x=110, baseline=250, scale=38, active={1, 5}, soft={2, 3, 4}, mid=mid),
        f'<rect x="194" y="136" width="182" height="114" fill="{FILL_HL_SOFT}" opacity="0.55" stroke="none"/>',
        text(286, 128, "water = min(leftMax,rightMax)-height[i]", size=12, fill=FILL_HL, mono=True, anchor="middle"),
        callout(540, 132, 250, 82, "two pointer rule", "Advance the side with smaller max; the opposite side already bounds it.", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: reason from the limiting wall, not from each bar independently.", *parts)


def stock_profit() -> str:
    title = "Best time to buy/sell stock"
    mid = mid_of(title)
    pts = [(96, 230), (176, 150), (256, 210), (336, 110), (416, 170), (496, 90)]
    path = "M" + " L".join(f"{x} {y}" for x, y in pts)
    parts = [
        path_line(path, mid=mid, accent=True, arrow=False),
        mini_node(176, 150, "buy", soft=True, mid=mid),
        mini_node(496, 90, "sell", active=True, mid=mid),
        path_line("M176 150 H496", mid=mid, accent=True),
        edge_label(336, 140, "max profit"),
        callout(580, 118, 230, 82, "scan state", "Track min price so far; profit today = price - min.", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: greedily remember the best prior buy, then evaluate each sell.", *parts)


def min_window() -> str:
    title = "Minimum window substring"
    mid = mid_of(title)
    parts = [
        array_row(list("A D O B E C O D E B A N C".split()), x=44, y=136, w=36, active=set(range(8, 13)), soft=set(range(3, 8)), pointers={8: "L", 12: "R"}, mid=mid),
        node(570, 108, 210, 56, "need counts", "A:1 B:1 C:1", kind="cache", mid=mid),
        callout(570, 190, 260, 72, "valid window", "When formed == required, shrink L and record the smallest span.", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: count satisfied characters, not just window length.", *parts)


def kadane() -> str:
    title = "Kadane maximum subarray"
    mid = mid_of(title)
    parts = [
        array_row([-2, 1, -3, 4, -1, 2, 1, -5, 4], x=72, y=128, w=46, active={3, 4, 5, 6}, soft={1, 2}, pointers={3: "start", 6: "best"}, mid=mid),
        node(620, 92, 190, 54, "current = max(x, current+x)", "", kind="app", mid=mid),
        node(620, 172, 190, 54, "best = max(best,current)", "", kind="hl", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: drop any prefix whose running sum becomes negative.", *parts)


def rotated_search() -> str:
    title = "Search rotated sorted array"
    mid = mid_of(title)
    parts = [
        array_row([4, 5, 6, 7, 0, 1, 2], x=80, y=132, active={3}, soft={0, 1, 2}, pointers={0: "lo", 3: "mid", 6: "hi"}, mid=mid),
        edge_label(205, 114, "left half sorted", accent=True),
        node(590, 104, 210, 70, "branch", "If target fits sorted half, keep it; else search other half.", kind="app", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: one side of mid is always sorted; use it to discard half.", *parts)


def top_k_buckets() -> str:
    title = "Top K frequent buckets"
    mid = mid_of(title)
    parts = [
        node(60, 116, 150, 54, "frequency map", "item -> count", kind="cache", mid=mid),
        array_row(["0", "1", "2", "3", "4"], x=280, y=104, w=48, active={3}, soft={1, 2}, pointers={3: "bucket count"}, indexes=False, mid=mid),
        node(598, 92, 150, 48, "scan high -> low", "emit until k", kind="hl", mid=mid),
        node(598, 172, 150, 48, "answer", "top K", kind="store", mid=mid),
        arrow(210, 143, 275, 126, mid=mid, accent=True),
        arrow(536, 126, 592, 116, mid=mid, accent=True),
    ]
    return algorithm_canvas(title, "Interview takeaway: counts are bounded by n, so buckets avoid O(n log n) sorting.", *parts)


def meeting_rooms() -> str:
    title = "Meeting rooms sweep"
    mid = mid_of(title)
    parts = [
        interval_bar(90, 88, 0, 3, "A", active=True, mid=mid),
        interval_bar(90, 142, 1, 5, "B", active=True, mid=mid),
        interval_bar(90, 196, 4, 6, "C", active=False, mid=mid),
        node(560, 96, 170, 54, "min-heap", "earliest end", kind="queue", mid=mid),
        node(560, 176, 170, 54, "rooms = heap size", "peak overlap", kind="hl", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: reuse a room when the earliest ending meeting has finished.", *parts, h=350)


def rotting_oranges() -> str:
    title = "Rotting oranges BFS"
    mid = mid_of(title)
    grid = [[2, 1, 1, 0], [1, 1, 0, 1], [0, 1, 1, 1]]
    parts = [
        matrix_grid(grid, x=100, y=92, active={(0, 0)}, soft={(0, 1), (1, 0)}, mid=mid, size=46),
        node(430, 96, 190, 54, "multi-source queue", "all rotten at t=0", kind="queue", mid=mid),
        node(430, 176, 190, 54, "minute layers", "infect neighbors", kind="hl", mid=mid),
        callout(430, 258, 270, 48, "finish", "If fresh remain after BFS, return -1.", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: time in grids is often BFS layer count.", *parts, h=370)


def autocomplete_trie() -> str:
    title = "Autocomplete trie"
    mid = mid_of(title)
    parts = [
        mini_node(180, 90, "root", active=True, mid=mid),
        mini_node(100, 170, "c", soft=True, mid=mid),
        mini_node(260, 170, "d", mid=mid),
        mini_node(70, 250, "a", soft=True, mid=mid),
        mini_node(150, 250, "o", soft=True, mid=mid),
        path_line("M164 108 L116 152 M196 108 L244 152 M94 188 L76 232 M106 188 L140 232", mid=mid, arrow=False),
        node(470, 102, 200, 54, "prefix walk", "O(len(prefix))", kind="app", mid=mid),
        node(470, 188, 200, 54, "top suggestions", "cached by node", kind="cache", mid=mid),
    ]
    return algorithm_canvas(title, "Interview takeaway: trie nodes trade memory for prefix lookup speed.", *parts, h=370)


def simple_arch_diagrams() -> dict[str, str]:
    return {
        "cache-cdn": simple_system(
            "CDN cache path",
            "Interview takeaway: separate edge hits from origin misses and invalidate with versioned assets.",
            client=("Browser", "GET asset"),
            edge=("CDN POP", "cache key"),
            service=("Origin app", "auth / render"),
            async_node=("Purge bus", "ban / version"),
            data=("Object store", "immutable blobs"),
            extra_data=("Redis", "hot HTML"),
            labels=("GET", "miss", "purge", "fetch"),
        ),
        "cap": simple_system(
            "CAP trade-off",
            "Interview takeaway: under partition you choose availability or consistency per operation.",
            client=("Client", "read/write"),
            edge=("Router", "region aware"),
            service=("Replica A", "leader?"),
            async_node=("Partition", "delayed link"),
            data=("Replica B", "possibly stale"),
            labels=("write", "route", "replicate", "converge"),
        ),
        "chat-flow": simple_system(
            "Chat send flow",
            "Interview takeaway: persist before fanout; delivery receipts are separate from message writes.",
            client=("Sender", "mobile"),
            edge=("WebSocket GW", "sticky session"),
            service=("Message svc", "validate + store"),
            async_node=("Fanout topic", "per conversation"),
            data=("Message DB", "append only"),
            extra_data=("Presence cache", "online users"),
            labels=("send", "auth", "produce", "append"),
        ),
        "feed-fanout": simple_system(
            "Feed fanout on write",
            "Interview takeaway: precompute follower inboxes for fast reads, but protect celebrity writes.",
            client=("Creator", "post"),
            edge=("API edge", "rate limits"),
            service=("Post svc", "fanout plan"),
            async_node=("Fanout workers", "followers"),
            data=("Inbox store", "per user feed"),
            extra_data=("Post store", "source of truth"),
            labels=("post", "write", "enqueue", "append"),
        ),
        "object-storage": simple_system(
            "Object storage upload",
            "Interview takeaway: split metadata from immutable chunks and verify checksums at boundaries.",
            client=("Client", "multipart upload"),
            edge=("Upload edge", "signed URL"),
            service=("Metadata svc", "object manifest"),
            async_node=("Compaction queue", "erasure coding"),
            data=("Blob store", "chunks"),
            extra_data=("Metadata DB", "namespace"),
            labels=("PUT part", "authorize", "complete", "write"),
        ),
        "video-pipeline": simple_system(
            "Video processing pipeline",
            "Interview takeaway: uploads return quickly; transcoding and thumbnails happen asynchronously.",
            client=("Uploader", "raw video"),
            edge=("Upload edge", "resumable"),
            service=("Asset svc", "metadata"),
            async_node=("Transcode jobs", "renditions"),
            data=("Media store", "HLS/DASH"),
            extra_data=("Catalog DB", "status"),
            labels=("upload", "register", "job", "write"),
        ),
        "geo-matching": simple_system(
            "Geo proximity matching",
            "Interview takeaway: index moving entities by geohash/S2 cells and widen search gradually.",
            client=("Rider app", "pickup"),
            edge=("Location edge", "coarse cell"),
            service=("Matcher", "candidate rank"),
            async_node=("Dispatch events", "offer / accept"),
            data=("Geo index", "drivers by cell"),
            extra_data=("Trip DB", "state machine"),
            labels=("request", "nearby", "offer", "update"),
        ),
        "llm-flow": simple_system(
            "LLM request flow",
            "Interview takeaway: keep prompt assembly, model inference, and safety boundaries explicit.",
            client=("User", "prompt"),
            edge=("AI gateway", "auth + quota"),
            service=("Prompt builder", "context + policy"),
            async_node=("Model runtime", "stream tokens"),
            data=("Prompt logs", "audit / eval"),
            extra_data=("Context cache", "short-lived"),
            labels=("ask", "gate", "infer", "log"),
        ),
        "rag": simple_system(
            "Retrieval augmented generation",
            "Interview takeaway: retrieval is a grounding step, not a guarantee; cite and evaluate sources.",
            client=("User", "question"),
            edge=("API", "tenant policy"),
            service=("Retriever", "embed + search"),
            async_node=("LLM", "grounded answer"),
            data=("Vector index", "chunks"),
            extra_data=("Doc store", "source text"),
            labels=("ask", "rewrite", "top-k", "fetch"),
        ),
        "memory": simple_system(
            "Agent memory",
            "Interview takeaway: separate ephemeral context from durable user facts with consent and decay.",
            client=("User", "conversation"),
            edge=("Assistant", "session"),
            service=("Memory writer", "extract facts"),
            async_node=("Review queue", "privacy filters"),
            data=("Long-term store", "facts"),
            extra_data=("Short context", "tokens"),
            labels=("turn", "summarize", "review", "upsert"),
        ),
        "agent-loop": simple_system(
            "Agent loop",
            "Interview takeaway: plan-act-observe loops need budgets, tool allowlists, and stop conditions.",
            client=("User goal", "task"),
            edge=("Planner", "decompose"),
            service=("Executor", "tool call"),
            async_node=("Observation", "result"),
            data=("Scratchpad", "state"),
            extra_data=("Policy", "limits"),
            labels=("goal", "plan", "act", "record"),
        ),
        "mcp": simple_system(
            "MCP tool boundary",
            "Interview takeaway: MCP standardizes tool schemas while preserving least-privilege server boundaries.",
            client=("LLM host", "client"),
            edge=("MCP client", "schema cache"),
            service=("MCP server", "tool router"),
            async_node=("Tool call", "side effect"),
            data=("External API", "resource"),
            labels=("intent", "JSON-RPC", "invoke", "read/write"),
        ),
        "skills": simple_system(
            "Skills packaging",
            "Interview takeaway: skills make repeatable procedures discoverable without retraining the model.",
            client=("User", "request"),
            edge=("Skill router", "metadata match"),
            service=("Skill runtime", "instructions"),
            async_node=("Artifacts", "files / commands"),
            data=("Skill registry", "versioned"),
            labels=("ask", "select", "execute", "publish"),
        ),
        "ai-assistant": simple_system(
            "AI assistant architecture",
            "Interview takeaway: assistants are product systems: identity, memory, tools, safety, and eval loops.",
            client=("User", "chat UI"),
            edge=("Assistant API", "auth + quota"),
            service=("Orchestrator", "model + tools"),
            async_node=("Eval stream", "quality signals"),
            data=("Memory + logs", "tenant scoped"),
            extra_data=("Tool registry", "allowlist"),
            labels=("message", "route", "trace", "store"),
        ),
        "hybrid-search": simple_system(
            "Hybrid search",
            "Interview takeaway: combine lexical precision with vector recall, then rerank the merged candidates.",
            client=("Query", "keywords + intent"),
            edge=("Search API", "filters"),
            service=("Merger/Reranker", "BM25 + ANN"),
            async_node=("Index updates", "freshness"),
            data=("Vector index", "semantic"),
            extra_data=("Inverted index", "lexical"),
            labels=("search", "parse", "rank", "refresh"),
        ),
        "eval-pipeline": simple_system(
            "AI evaluation pipeline",
            "Interview takeaway: ship model changes behind eval gates with offline, online, and human signals.",
            client=("Traffic sample", "prompts"),
            edge=("Trace collector", "redaction"),
            service=("Eval runner", "judges + metrics"),
            async_node=("Review queue", "human labels"),
            data=("Metrics store", "slices"),
            extra_data=("Golden set", "regression"),
            labels=("sample", "sanitize", "score", "write"),
        ),
        "agent-tools": simple_system(
            "Agent tool use",
            "Interview takeaway: tools extend capability but require schemas, retries, and permission checks.",
            client=("User task", "goal"),
            edge=("Policy gate", "allowed tools"),
            service=("Tool planner", "arguments"),
            async_node=("Tool executor", "idempotent call"),
            data=("Tool result", "observation"),
            labels=("intent", "authorize", "call", "return"),
        ),
        "memory-tiers": simple_system(
            "AI memory tiers",
            "Interview takeaway: choose TTL and retrieval policy per memory tier to avoid stale personalization.",
            client=("Conversation", "turns"),
            edge=("Context window", "working set"),
            service=("Summarizer", "episodic"),
            async_node=("Consolidator", "decay + merge"),
            data=("Profile store", "semantic facts"),
            extra_data=("Vector memory", "episodes"),
            labels=("recent", "compress", "promote", "upsert"),
        ),
        "moderation-cascade": simple_system(
            "Moderation cascade",
            "Interview takeaway: fast rules catch obvious cases; expensive classifiers handle ambiguous content.",
            client=("Input", "text/image"),
            edge=("Rules", "blocklists"),
            service=("Classifier", "risk score"),
            async_node=("Human review", "appeals"),
            data=("Policy log", "audit"),
            labels=("submit", "screen", "escalate", "record"),
        ),
        "recsys-towers": simple_system(
            "Recommendation two-tower retrieval",
            "Interview takeaway: retrieve cheaply with embeddings, then rank deeply on a smaller candidate set.",
            client=("User", "session"),
            edge=("Feature fetch", "fresh context"),
            service=("User tower", "embedding"),
            async_node=("Candidate gen", "ANN top-k"),
            data=("Item tower index", "item vectors"),
            extra_data=("Feature store", "features"),
            labels=("request", "hydrate", "query", "retrieve"),
        ),
        "multi-tenant-ai": simple_system(
            "Multi-tenant AI platform",
            "Interview takeaway: tenant isolation spans prompts, tools, data, quotas, and observability.",
            client=("Tenant app", "API key"),
            edge=("Gateway", "quota + auth"),
            service=("Orchestrator", "tenant policy"),
            async_node=("Trace bus", "billing/eval"),
            data=("Tenant data", "isolated"),
            extra_data=("Config store", "models/tools"),
            labels=("call", "identify", "trace", "access"),
        ),
        "transcription-ai": simple_system(
            "AI transcription pipeline",
            "Interview takeaway: streaming UX and batch accuracy often use different model paths.",
            client=("Audio stream", "chunks"),
            edge=("Media gateway", "VAD"),
            service=("ASR service", "partial text"),
            async_node=("Diarization job", "speakers"),
            data=("Transcript store", "segments"),
            extra_data=("Object store", "audio"),
            labels=("stream", "decode", "enrich", "save"),
        ),
        "grounded-support": simple_system(
            "Grounded support assistant",
            "Interview takeaway: cite retrieved sources and hand off when confidence or policy requires it.",
            client=("Customer", "question"),
            edge=("Support API", "account auth"),
            service=("RAG agent", "retrieve + answer"),
            async_node=("Ticket queue", "handoff"),
            data=("Knowledge base", "articles"),
            extra_data=("CRM", "customer facts"),
            labels=("ask", "authorize", "escalate", "lookup"),
        ),
        "llm-serving": simple_system(
            "LLM inference serving",
            "Interview takeaway: throughput comes from batching and KV cache management; latency needs admission control.",
            client=("Clients", "streaming"),
            edge=("Model gateway", "rate + auth"),
            service=("Batcher", "continuous batch"),
            async_node=("GPU workers", "decode loop"),
            data=("KV cache", "paged blocks"),
            extra_data=("Model weights", "replicas"),
            labels=("prompt", "admit", "schedule", "read"),
        ),
        "agentic-rag": simple_system(
            "Agentic RAG routing",
            "Interview takeaway: default to simple RAG; add agent loops only for measurable multi-hop needs.",
            client=("Question", "user"),
            edge=("Router", "complexity score"),
            service=("RAG planner", "sub-questions"),
            async_node=("Tool loop", "retrieve/verify"),
            data=("Knowledge graph", "entities"),
            extra_data=("Vector index", "chunks"),
            labels=("ask", "classify", "iterate", "lookup"),
        ),
        "semantic-cache": simple_system(
            "Semantic cache",
            "Interview takeaway: cache keys include tenant, model, policy, and similarity threshold.",
            client=("Prompt", "request"),
            edge=("Embedding gate", "tenant/model"),
            service=("ANN lookup", "similarity"),
            async_node=("LLM fallback", "miss path"),
            data=("Response cache", "embedding+answer"),
            labels=("embed", "search", "miss", "fill"),
        ),
        "code-copilot": simple_system(
            "Coding copilot",
            "Interview takeaway: inline completion optimizes latency; repo Q&A optimizes context quality.",
            client=("IDE", "cursor + file"),
            edge=("Context packer", "budget"),
            service=("Retriever", "repo symbols"),
            async_node=("Model call", "FIM/chat"),
            data=("Repo index", "embeddings"),
            extra_data=("Telemetry", "acceptance"),
            labels=("request", "pack", "infer", "search"),
        ),
        "feature-store": simple_system(
            "Feature store",
            "Interview takeaway: train/serve parity depends on shared definitions and point-in-time correctness.",
            client=("Pipelines", "events"),
            edge=("Registry", "feature defs"),
            service=("Transform jobs", "offline/online"),
            async_node=("Materializer", "freshness"),
            data=("Online KV", "serving"),
            extra_data=("Offline tables", "training"),
            labels=("define", "compute", "publish", "serve"),
        ),
        "chat-message-path": simple_system(
            "Chat message path",
            "Interview takeaway: message IDs, ordering, and ack semantics matter more than socket mechanics.",
            client=("Sender", "mobile"),
            edge=("WS gateway", "connection id"),
            service=("Message API", "idempotency key"),
            async_node=("Delivery fanout", "recipients"),
            data=("Message log", "ordered append"),
            extra_data=("Inbox cache", "unread"),
            labels=("send", "validate", "produce", "append"),
        ),
        "rate-limiter-token": simple_system(
            "Token bucket rate limiter",
            "Interview takeaway: token bucket permits bursts while enforcing average rate over time.",
            client=("Client", "request"),
            edge=("Edge proxy", "identity key"),
            service=("Limiter", "consume token"),
            async_node=("Refill clock", "tokens/sec"),
            data=("Counter store", "atomic TTL"),
            labels=("call", "check", "refill", "write"),
        ),
        "youtube-cdn-pipeline": simple_system(
            "YouTube CDN pipeline",
            "Interview takeaway: upload, transcode, package, and edge distribution are separate scaling problems.",
            client=("Viewer", "playback"),
            edge=("CDN edge", "segment cache"),
            service=("Playback API", "manifest"),
            async_node=("Packager", "HLS/DASH"),
            data=("Origin media", "renditions"),
            extra_data=("Metadata DB", "catalog"),
            labels=("GET", "manifest", "prefetch", "segments"),
        ),
        "notification-pipeline": simple_system(
            "Notification pipeline",
            "Interview takeaway: preferences, dedupe, and provider retries belong before fanout leaves your system.",
            client=("Producer", "event"),
            edge=("Ingress", "schema"),
            service=("Preference svc", "dedupe + quiet hours"),
            async_node=("Channel queues", "email/push/SMS"),
            data=("Delivery log", "status"),
            extra_data=("User prefs", "opt-in"),
            labels=("event", "filter", "enqueue", "record"),
        ),
        "consistent-hash-cache": simple_system(
            "Consistent hash cache",
            "Interview takeaway: virtual nodes smooth distribution and minimize key movement on membership changes.",
            client=("Client", "key"),
            edge=("Hash ring", "virtual nodes"),
            service=("Cache router", "owner lookup"),
            async_node=("Rebalance", "node changes"),
            data=("Cache nodes", "sharded"),
            labels=("get", "hash", "move keys", "route"),
        ),
        "ticket-hold-checkout": simple_system(
            "Ticket hold checkout",
            "Interview takeaway: holds are leases; payment success must atomically confirm before expiry.",
            client=("Buyer", "seat select"),
            edge=("Checkout API", "idempotency"),
            service=("Inventory svc", "hold lease"),
            async_node=("Payment saga", "authorize/capture"),
            data=("Seat ledger", "holds + sales"),
            extra_data=("Timer wheel", "expiry"),
            labels=("hold", "validate", "authorize", "commit"),
        ),
        "dropbox-sync": simple_system(
            "Dropbox file sync",
            "Interview takeaway: sync protocols exchange metadata first, then transfer content-addressed blocks.",
            client=("Device", "local changes"),
            edge=("Sync edge", "delta cursor"),
            service=("Metadata svc", "version vector"),
            async_node=("Block upload", "dedupe chunks"),
            data=("Block store", "content hash"),
            extra_data=("Metadata DB", "folders"),
            labels=("delta", "compare", "upload", "store"),
        ),
        "web-crawler": simple_system(
            "Web crawler",
            "Interview takeaway: politeness and frontier scheduling are first-class design constraints.",
            client=("Seeds", "URLs"),
            edge=("Frontier", "priority + host"),
            service=("Fetcher", "robots + crawl"),
            async_node=("Parser queue", "links/content"),
            data=("Index store", "documents"),
            extra_data=("Seen set", "dedupe"),
            labels=("seed", "schedule", "parse", "index"),
        ),
        "payment-saga": simple_system(
            "Payment saga",
            "Interview takeaway: distributed checkout uses compensating actions, not cross-service transactions.",
            client=("Buyer", "checkout"),
            edge=("Order API", "idempotency"),
            service=("Saga orchestrator", "state machine"),
            async_node=("Events", "reserve/pay/ship"),
            data=("Order ledger", "append state"),
            extra_data=("Outbox", "exactly-once-ish"),
            labels=("submit", "start", "emit", "record"),
        ),
        "leaderboard": simple_system(
            "Leaderboard",
            "Interview takeaway: hot ranked reads need sorted structures plus async aggregation for write spikes.",
            client=("Player", "score"),
            edge=("Game API", "auth"),
            service=("Score svc", "validate"),
            async_node=("Aggregator", "season/window"),
            data=("Sorted set", "rank by score"),
            extra_data=("Event log", "audit"),
            labels=("score", "check", "aggregate", "zadd"),
        ),
    }


def load_balancer() -> str:
    return system_diagram(
        "Load balancer",
        "Interview takeaway: balancing policy, health checks, and connection draining are the core trade-offs.",
        [
            n("user", "CLIENT", 1, "Clients", "web / mobile", "client"),
            n("dns", "EDGE", 0.25, "DNS / Anycast", "nearest POP", "edge"),
            n("lb", "EDGE", 1.4, "L7 load balancer", "TLS + routing", "edge"),
            n("api1", "SERVICE", 0.15, "API replica A", "healthy", "app", dx=-18),
            n("api2", "SERVICE", 1.15, "API replica B", "draining", "warn", dx=18),
            n("api3", "SERVICE", 2.15, "API replica C", "healthy", "app", dx=-18),
            n("jobs", "ASYNC", 1.15, "Work queue", "slow tasks", "queue"),
            n("cache", "DATA", 0.45, "Redis cache", "hot reads", "cache", dx=-42),
            n("db", "DATA", 1.85, "Primary DB", "durable writes", "store", dx=42),
        ],
        [
            f("user", "dns", "lookup", 1),
            f("dns", "lb", "connect", 2),
            f("lb", "api1", "least-conn", 3, accent=True),
            f("lb", "api2", "drain", "D", dashed=True),
            f("api1", "cache", "hit", 4, accent=True),
            f("api1", "db", "miss/read", 5),
            f("api1", "jobs", "enqueue", 6),
        ],
        callouts=[(732, 388, 218, 54, "slo guardrail", "Health checks remove bad hosts before users see errors.")],
    )


def url_shortener() -> str:
    return simple_system(
        "URL shortener",
        "Interview takeaway: short code generation, redirect latency, and abuse controls define the design.",
        client=("Browser", "short URL"),
        edge=("Redirect edge", "domain + TLS"),
        service=("URL service", "lookup code"),
        async_node=("Analytics bus", "click events"),
        data=("URL mapping DB", "code -> long URL"),
        extra_data=("Hot cache", "code -> URL"),
        labels=("GET /abc", "route", "emit", "lookup"),
    )


def url_shortener_detailed() -> str:
    return system_diagram(
        "URL shortener detailed",
        "Interview takeaway: create path optimizes uniqueness; redirect path optimizes cache hit latency.",
        [
            n("creator", "CLIENT", 0.35, "Creator", "POST long URL", "client"),
            n("clicker", "CLIENT", 2.05, "Clicker", "GET /xYz", "client"),
            n("edge", "EDGE", 1.15, "API / Redirect edge", "auth + abuse", "edge"),
            n("api", "SERVICE", 0.35, "Create API", "validate URL", "app", dx=-20),
            n("redir", "SERVICE", 2.05, "Redirect API", "302 response", "hl", dx=20),
            n("id", "ASYNC", 0.35, "ID allocator", "base62 / Snowflake", "queue"),
            n("events", "ASYNC", 2.05, "Click stream", "analytics", "queue"),
            n("map", "DATA", 0.55, "Mapping DB", "code -> long", "store", dx=-44),
            n("cache", "DATA", 1.85, "Redis cache", "hot codes", "cache", dx=44),
        ],
        [
            f("creator", "edge", "create", 1),
            f("edge", "api", "POST", 2),
            f("api", "id", "reserve", 3, accent=True),
            f("api", "map", "insert", 4),
            f("clicker", "edge", "GET", 5),
            f("edge", "redir", "route", 6),
            f("redir", "cache", "hit/miss", 7, accent=True),
            f("redir", "map", "fallback", 8),
            f("redir", "events", "produce", 9),
        ],
        callouts=[(738, 388, 218, 54, "redirect path", "Cache and return 302 before analytics finishes.")],
    )


def rag_detailed() -> str:
    return system_diagram(
        "RAG detailed",
        "Interview takeaway: retrieval quality, reranking, and citation grounding are more important than model size.",
        [
            n("user", "CLIENT", 1.2, "User", "question", "client"),
            n("api", "EDGE", 1.2, "RAG API", "tenant + policy", "edge"),
            n("rewrite", "SERVICE", 0.2, "Query rewrite", "intent + filters", "app", dx=-22),
            n("rerank", "SERVICE", 1.45, "Reranker", "cross encoder", "hl", dx=22),
            n("llm", "ASYNC", 1.1, "LLM", "grounded answer", "queue"),
            n("vec", "DATA", 0.15, "Vector index", "ANN top-k", "store", dx=-44),
            n("lex", "DATA", 1.15, "BM25 index", "exact terms", "cache", dx=44),
            n("docs", "DATA", 2.2, "Doc store", "source chunks", "store", dx=0),
        ],
        [
            f("user", "api", "ask", 1),
            f("api", "rewrite", "rewrite", 2),
            f("rewrite", "vec", "semantic", 3, accent=True),
            f("rewrite", "lex", "lexical", 4),
            f("vec", "rerank", "top-k", 5, via="vh"),
            f("lex", "rerank", "merge", 6, via="vh"),
            f("rerank", "docs", "fetch text", 7),
            f("rerank", "llm", "context", 8, accent=True),
            f("llm", "api", "answer+cites", 9, via="vh"),
        ],
        callouts=[(44, 390, 280, 52, "failure mode", "Good RAG cites sources and says when retrieval is weak.")],
    )


def feed_hybrid_fanout() -> str:
    return system_diagram(
        "Hybrid feed fanout",
        "Interview takeaway: use push for normal accounts and pull/rank celebrity content at read time.",
        [
            n("creator", "CLIENT", 0.35, "Publisher", "new post", "client"),
            n("reader", "CLIENT", 2.1, "Reader", "open feed", "client"),
            n("edge", "EDGE", 1.2, "Feed API", "auth + cursor", "edge"),
            n("write", "SERVICE", 0.35, "Write path", "post metadata", "app", dx=-20),
            n("read", "SERVICE", 2.1, "Read path", "merge + rank", "hl", dx=20),
            n("fanout", "ASYNC", 0.45, "Fanout workers", "followers inbox", "queue"),
            n("pull", "ASYNC", 2.0, "Celebrity pull", "defer heavy fanout", "queue"),
            n("post", "DATA", 0.35, "Post store", "source of truth", "store", dx=-54),
            n("inbox", "DATA", 1.35, "Inbox store", "precomputed", "cache", dx=44),
            n("graph", "DATA", 2.35, "Graph store", "follow edges", "store", dx=-10),
        ],
        [
            f("creator", "edge", "post", 1),
            f("edge", "write", "write", 2),
            f("write", "post", "append", 3),
            f("write", "fanout", "produce", 4, accent=True),
            f("fanout", "inbox", "push", 5),
            f("reader", "edge", "read", 6),
            f("edge", "read", "cursor", 7),
            f("read", "inbox", "pull inbox", 8),
            f("read", "pull", "celebrity ids", 9, dashed=True),
            f("pull", "post", "fetch latest", 10),
            f("read", "graph", "filters", 11),
        ],
        callouts=[(744, 388, 210, 54, "ranker input", "Merge inbox, pull candidates, ads, and freshness features.")],
    )


def uber_matching() -> str:
    return system_diagram(
        "Uber matching",
        "Interview takeaway: matching is a low-latency geo search plus a stateful dispatch protocol.",
        [
            n("rider", "CLIENT", 0.6, "Rider app", "pickup/dropoff", "client"),
            n("driver", "CLIENT", 2.0, "Driver app", "location pings", "client"),
            n("edge", "EDGE", 1.3, "Mobile edge", "region routing", "edge"),
            n("loc", "SERVICE", 0.35, "Location svc", "S2/geohash", "app", dx=-22),
            n("match", "SERVICE", 1.55, "Matcher", "ETA + constraints", "hl", dx=22),
            n("dispatch", "ASYNC", 1.35, "Dispatch queue", "offer timeout", "queue"),
            n("geo", "DATA", 0.35, "Geo index", "drivers by cell", "cache", dx=-50),
            n("trip", "DATA", 1.55, "Trip store", "state machine", "store", dx=40),
            n("pricing", "DATA", 2.55, "Pricing cache", "surge/ETA", "cache", dx=-20),
        ],
        [
            f("driver", "edge", "ping", 1),
            f("edge", "loc", "update", 2),
            f("loc", "geo", "upsert cell", 3, accent=True),
            f("rider", "edge", "request", 4),
            f("edge", "match", "route", 5),
            f("match", "geo", "nearby", 6, accent=True),
            f("match", "pricing", "ETA/fare", 7),
            f("match", "dispatch", "offer", 8),
            f("dispatch", "trip", "accept/timeout", 9),
        ],
        callouts=[(738, 388, 218, 54, "search widening", "Start in pickup cell, expand rings until enough drivers qualify.")],
    )


def kafka_partitions() -> str:
    return system_diagram(
        "Kafka partitions",
        "Interview takeaway: ordering is per partition; consumer-group parallelism is bounded by partition count.",
        [
            n("prod", "CLIENT", 1.1, "Producers", "keyed events", "client"),
            n("broker", "EDGE", 1.1, "Broker leader", "topic metadata", "edge"),
            n("p0", "ASYNC", 0.2, "Partition 0", "append log", "queue"),
            n("p1", "ASYNC", 1.15, "Partition 1", "append log", "queue"),
            n("p2", "ASYNC", 2.1, "Partition 2", "append log", "queue"),
            n("cg", "SERVICE", 1.1, "Consumer group", "rebalance", "app"),
            n("offsets", "DATA", 0.75, "Offsets", "committed", "store", dx=-40),
            n("sink", "DATA", 2.0, "Sink DB", "materialized", "store", dx=40),
        ],
        [
            f("prod", "broker", "produce", 1),
            f("broker", "p1", "hash(key)", 2, accent=True),
            f("p1", "cg", "poll", 3, via="vh"),
            f("cg", "offsets", "commit", 4),
            f("cg", "sink", "process", 5),
            f("p0", "cg", "parallel", "A", dashed=True, via="vh"),
            f("p2", "cg", "parallel", "B", dashed=True, via="vh"),
        ],
        callouts=[(42, 388, 286, 54, "replay", "Offsets are consumer state; logs can be replayed if retention keeps data.")],
    )


def replication() -> str:
    return system_diagram(
        "Database replication",
        "Interview takeaway: replicas improve read scale and availability but introduce lag and failover complexity.",
        [
            n("client", "CLIENT", 1, "Client", "read/write", "client"),
            n("proxy", "EDGE", 1, "DB proxy", "route reads", "edge"),
            n("primary", "SERVICE", 1, "Primary", "writes", "hl"),
            n("wal", "ASYNC", 1, "WAL stream", "ordered log", "queue"),
            n("r1", "DATA", 0.45, "Replica A", "read", "store", dx=-42),
            n("r2", "DATA", 1.75, "Replica B", "lagging", "store", dx=42),
        ],
        [
            f("client", "proxy", "SQL", 1),
            f("proxy", "primary", "writes", 2, accent=True),
            f("primary", "wal", "replicate", 3),
            f("wal", "r1", "apply", 4),
            f("wal", "r2", "apply lag", 5, dashed=True),
        ],
    )


def sql_nosql() -> str:
    return system_diagram(
        "SQL vs NoSQL",
        "Interview takeaway: pick data models from access patterns, consistency needs, and query flexibility.",
        [
            n("app", "CLIENT", 1, "Application", "access patterns", "client"),
            n("dao", "EDGE", 1, "Data API", "contract", "edge"),
            n("tx", "SERVICE", 0.45, "SQL path", "joins + ACID", "app", dx=-20),
            n("kv", "SERVICE", 1.75, "NoSQL path", "scale + shape", "app", dx=20),
            n("events", "ASYNC", 1, "CDC / stream", "sync views", "queue"),
            n("sql", "DATA", 0.45, "Relational DB", "normalized", "store", dx=-45),
            n("nosql", "DATA", 1.75, "Document/KV", "denormalized", "store", dx=45),
        ],
        [
            f("app", "dao", "query", 1),
            f("dao", "tx", "transactions", 2),
            f("dao", "kv", "key access", 3),
            f("tx", "sql", "SQL", 4),
            f("kv", "nosql", "get/put", 5),
            f("tx", "events", "changes", 6, dashed=True),
            f("events", "nosql", "project", 7, dashed=True),
        ],
    )


def queue_diagram() -> str:
    return system_diagram(
        "Queue based workflow",
        "Interview takeaway: queues absorb spikes, retry transient failure, and need dead-letter handling.",
        [
            n("prod", "CLIENT", 1, "Producer", "request accepted", "client"),
            n("api", "EDGE", 1, "Ingress API", "idempotency", "edge"),
            n("svc", "SERVICE", 1, "Job service", "validate", "app"),
            n("q", "ASYNC", 0.6, "Main queue", "visibility timeout", "queue"),
            n("dlq", "ASYNC", 2.1, "DLQ", "poison messages", "alert"),
            n("worker", "DATA", 0.6, "Workers", "side effects", "app", dx=-42),
            n("state", "DATA", 2.0, "Job state DB", "status", "store", dx=42),
        ],
        [
            f("prod", "api", "submit", 1),
            f("api", "svc", "202", 2),
            f("svc", "q", "enqueue", 3, accent=True),
            f("q", "worker", "lease", 4),
            f("worker", "state", "complete", 5),
            f("worker", "dlq", "fail xN", 6, dashed=True),
        ],
    )


def build_diagrams() -> dict[str, str]:
    diagrams: dict[str, str] = {
        "hash-map": hash_map(),
        "two-pointers": two_pointers(),
        "sliding-window": sliding_window(),
        "stack": stack(),
        "binary-search": binary_search(),
        "linked-list": linked_list(),
        "tree-bst": tree_bst(),
        "heap": heap(),
        "backtracking": backtracking(),
        "bfs-graph": bfs_graph(),
        "dp-table": dp_table(),
        "intervals": intervals(),
        "bits-xor": bits_xor(),
        "prefix-sums": prefix_sums(),
        "two-sum-walk": two_sum_walk(),
        "longest-substr-window": longest_substr_window(),
        "merge-intervals-walk": merge_intervals_walk(),
        "lru-cache": lru_cache(),
        "islands-dfs": islands_dfs(),
        "topo-kahn": topo_kahn(),
        "coin-change-dp": coin_change_dp(),
        "word-ladder-bfs": word_ladder_bfs(),
        "serialize-tree": serialize_tree(),
        "trap-water": trap_water(),
        "stock-profit": stock_profit(),
        "min-window": min_window(),
        "kadane": kadane(),
        "rotated-search": rotated_search(),
        "top-k-buckets": top_k_buckets(),
        "meeting-rooms": meeting_rooms(),
        "rotting-oranges": rotting_oranges(),
        "autocomplete-trie": autocomplete_trie(),
        "load-balancer": load_balancer(),
        "url-shortener": url_shortener(),
        "url-shortener-detailed": url_shortener_detailed(),
        "rag-detailed": rag_detailed(),
        "feed-hybrid-fanout": feed_hybrid_fanout(),
        "uber-matching": uber_matching(),
        "kafka-partitions": kafka_partitions(),
        "replication": replication(),
        "sql-nosql": sql_nosql(),
        "queue": queue_diagram(),
    }
    diagrams.update(simple_arch_diagrams())
    missing = [key for key in REQUIRED_KEYS if key not in diagrams]
    extra = [key for key in diagrams if key not in REQUIRED_KEYS]
    if missing or extra:
        raise RuntimeError(f"diagram key mismatch; missing={missing}, extra={extra}")
    return {key: diagrams[key] for key in REQUIRED_KEYS}


DIAGRAMS = build_diagrams()


def main() -> None:
    for p in OUT.glob("diagram-p*.jpg"):
        p.unlink()
    for p in OUT.glob("*.svg"):
        p.unlink()

    for key, content in DIAGRAMS.items():
        path = OUT / f"{key}.svg"
        path.write_text(content, encoding="utf-8")
        print("wrote", path.name)

    (OUT / "manifest.json").write_text(
        json.dumps({"diagrams": list(DIAGRAMS.keys()), "chapters": CHAPTER_DIAGRAMS}, indent=2),
        encoding="utf-8",
    )
    print("manifest diagrams:", len(DIAGRAMS))


if __name__ == "__main__":
    main()
