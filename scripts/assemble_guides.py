#!/usr/bin/env python3
"""Build interview-focus guide pages: paths, comparisons, companies, behavioral."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from interview_helpers import bullets, callout, code_block, figure_diagram  # noqa: E402
from interview_lens import (  # noqa: E402
    guide_shell,
    page_meta_bar,
    prerequisites,
    what_next,
)

OUT = ROOT / "chapters"
NAV = ROOT / "assets" / "nav.json"


def learning_paths() -> str:
    return f"""
{page_meta_bar(difficulty="Guide", reading_mins=12, master_hours="path-dependent", level_focus="Junior → Principal")}
{prerequisites(["Pick a target role", "Honestly assess current level"])}

<p>These paths are <strong>interview roadmaps</strong>, not documentation tours. Each stop links to
lab questions and book chapters. Do the labs aloud on a timer.</p>

<h2>Backend Engineer</h2>
{page_meta_bar(difficulty="Medium→Hard", reading_mins=0, master_hours="8–12 weeks", level_focus="Mid–Senior")}
<ol class="qa-steps">
<li>Coding patterns: <a href="interview-cp.html">Coding Lab</a> Q1–Q20 (timed).</li>
<li>Fundamentals: <a href="21-scaling.html">Scaling</a>, <a href="22-caching.html">Caching</a>,
<a href="23-databases.html">SQL/NoSQL</a>, <a href="26-queues.html">Queues</a>.</li>
<li>Design drills: <a href="interview-sd.html">System Design Lab</a> Q1, Q3, Q4, Q7, Q9, Q13, Q16.</li>
<li>Comparisons: <a href="comparisons.html">Kafka vs RabbitMQ, Redis vs Memcached, REST vs GraphQL</a>.</li>
<li>Behavioral: <a href="behavioral.html">STAR + leadership stories</a>.</li>
</ol>
{what_next([("Company guides", "company-guides.html"), ("System Design Lab", "interview-sd.html")])}

<h2>AI Engineer</h2>
{page_meta_bar(difficulty="Hard", reading_mins=0, master_hours="6–10 weeks", level_focus="Mid–Staff")}
<ol class="qa-steps">
<li>Core book: <a href="35-llms.html">LLMs</a> → <a href="37-rag.html">RAG</a> →
<a href="39-agents.html">Agents</a> → <a href="40-mcp.html">MCP</a>.</li>
<li>Lab: <a href="interview-ai.html">AI Lab</a> all Q1–Q17 (especially Q1, Q3, Q4, Q11, Q12, Q16).</li>
<li>Serving &amp; cost: Q8, Q11, Q13.</li>
<li>Eval &amp; shipping: Q3, Q17.</li>
<li>Optional coding: sliding window + graphs for general screens.</li>
</ol>
{what_next([("AI Lab", "interview-ai.html"), ("Design an AI agent chapter", "42-ai-agent.html")])}

<h2>Data Engineer</h2>
{page_meta_bar(difficulty="Medium→Hard", reading_mins=0, master_hours="6–10 weeks", level_focus="Mid–Senior")}
<ol class="qa-steps">
<li>Queues &amp; logs: <a href="26-queues.html">Queues</a>, SD Lab <a href="interview-sd.html#q16">Q16 Kafka</a>.</li>
<li>Storage: <a href="23-databases.html">SQL/NoSQL</a>, <a href="24-replication.html">Replication</a>,
SD <a href="interview-sd.html#q15">KV store</a>.</li>
<li>Batch/stream tradeoffs; feature store AI Lab <a href="interview-ai.html#q15">Q15</a>.</li>
<li>Coding: arrays, heaps, sorting intervals for screens.</li>
</ol>

<h2>DevOps / Platform</h2>
{page_meta_bar(difficulty="Medium→Hard", reading_mins=0, master_hours="6–10 weeks", level_focus="Mid–Staff")}
<ol class="qa-steps">
<li>Scaling &amp; LB: <a href="21-scaling.html">Scaling</a>, rate limiter SD <a href="interview-sd.html#q4">Q4</a>.</li>
<li>Caching CDN: <a href="22-caching.html">Caching</a>, SD <a href="interview-sd.html#q9">Q9</a>.</li>
<li>Observability, degradations, backpressure (SD scaling drills).</li>
<li>AI gateway quotas if platform-for-AI: AI Lab Q8, Q11.</li>
</ol>

<h2>Staff / Principal Engineer</h2>
{page_meta_bar(difficulty="Staff→Principal", reading_mins=0, master_hours="ongoing", level_focus="Staff–Principal")}
<ol class="qa-steps">
<li>Every SD answer must include failure modes, org interfaces, and migration plans.</li>
<li>Deep labs: payments Q13, KV Q15, feed Q2, video Q6, RAG platform Q1+Q8+Q11.</li>
<li>Write comparison tradeoffs from <a href="comparisons.html">Comparisons</a> without notes.</li>
<li>Behavioral: conflict, influence without authority, technical strategy —
<a href="behavioral.html">Behavioral lab</a>.</li>
<li>Teach: explain a design to a junior in 10 minutes (interviewers test this).</li>
</ol>

<h2>How to use levels on each question</h2>
<p>Open any Interview Lab card: use <strong>Level expectations</strong> to self-score. Junior =
correct solution; Mid = clean + follow-ups; Senior = production examples + tradeoffs; Staff =
platform/org impact; Principal = multi-year strategy and risk.</p>
"""


def comparisons() -> str:
    return f"""
{page_meta_bar(difficulty="Medium→Hard", reading_mins=25, master_hours="1–2 weeks", level_focus="Mid–Staff")}
{prerequisites(["Basic HTTP and databases", "One message queue exposure helps"])}

<p>Interviewers love comparisons because they force <strong>trade-offs</strong>, not memorized
definitions. For each pair: say when to use A, when to use B, and when neither.</p>

<h2>Kafka vs RabbitMQ</h2>
{page_meta_bar(difficulty="Hard", reading_mins=8, master_hours="3–5 days", level_focus="Senior")}
<div class="table-wrap"><table>
<caption>Interview cheat comparison</caption>
<thead><tr><th>Dimension</th><th>Kafka</th><th>RabbitMQ</th></tr></thead>
<tbody>
<tr><td>Model</td><td>Durable partitioned log</td><td>Smart broker queues / exchanges</td></tr>
<tr><td>Ordering</td><td>Per partition key</td><td>Per queue (with caveats)</td></tr>
<tr><td>Replay</td><td>Native via offsets / retention</td><td>Not the primary design</td></tr>
<tr><td>Routing</td><td>Coarse (topics/keys)</td><td>Rich exchanges/bindings</td></tr>
<tr><td>Throughput</td><td>Very high sequential I/O</td><td>Lower; flexible patterns</td></tr>
<tr><td>Use when</td><td>Event streaming, analytics, replay</td><td>Task queues, complex routing, RPC-ish</td></tr>
</tbody></table></div>
{callout("Expected interview answer", "<p>Kafka is a distributed commit log for high-throughput streams and replay. RabbitMQ is a message broker optimized for flexible routing and work queues. Choose Kafka for event sourcing/stream processing; Rabbit for task distribution with rich routing. Never promise global order on Kafka.</p>")}
{callout("Common mistakes", bullets(["Calling Kafka a 'queue' only", "Using Rabbit for multi-day replay lakes", "Ignoring consumer group rebalance costs"]))}
{callout("Production", bullets(["LinkedIn created Kafka for activity streams", "Many Uber/Netflix pipelines are log-centric", "Rabbit remains common for background jobs in Rails/JVM apps"]))}
<p><strong>Follow-ups:</strong> Exactly-once? Poison messages? Multi-region mirror?</p>
{what_next([("SD Lab: Message queue", "interview-sd.html#q16"), ("Queues chapter", "26-queues.html")])}

<h2>Redis vs Memcached</h2>
{page_meta_bar(difficulty="Medium", reading_mins=6, master_hours="2–3 days", level_focus="Mid–Senior")}
<div class="table-wrap"><table>
<thead><tr><th>Dimension</th><th>Redis</th><th>Memcached</th></tr></thead>
<tbody>
<tr><td>Data structures</td><td>Rich (strings, ZSET, hashes, streams)</td><td>Simple key/value blobs</td></tr>
<tr><td>Persistence</td><td>Optional AOF/RDB</td><td>Ephemeral</td></tr>
<tr><td>Clustering</td><td>Redis Cluster</td><td>Client-side sharding historically</td></tr>
<tr><td>Use when</td><td>Counters, leaderboards, locks, queues, cache</td><td>Simple hot-blob cache at huge QPS</td></tr>
</tbody></table></div>
{callout("Expected answer", "<p>Memcached is a fast ephemeral slab allocator for opaque values. Redis is a data-structure server that can also cache. Prefer Memcached for simple massive get/set caches; Redis when you need atomic structures, TTLs with logic, or persistence.</p>")}
{callout("Production", bullets(["Facebook historic Memcached scale", "GitHub/Twitter Redis use cases", "AWS ElastiCache offers both"]))}
{what_next([("SD Lab: Distributed cache", "interview-sd.html#q9"), ("Caching chapter", "22-caching.html")])}

<h2>REST vs GraphQL</h2>
{page_meta_bar(difficulty="Medium", reading_mins=7, master_hours="2–4 days", level_focus="Mid–Senior")}
<div class="table-wrap"><table>
<thead><tr><th>Dimension</th><th>REST</th><th>GraphQL</th></tr></thead>
<tbody>
<tr><td>Contract</td><td>Resources + verbs</td><td>Schema + queries/mutations</td></tr>
<tr><td>Over/under fetch</td><td>Common without BFF</td><td>Client specifies fields</td></tr>
<tr><td>Caching</td><td>HTTP cache-friendly</td><td>Harder at edge; need persisted queries</td></tr>
<tr><td>Complexity</td><td>Many endpoints</td><td>Resolver/N+1 risks</td></tr>
<tr><td>Use when</td><td>Public APIs, simple CRUD, cacheable GETs</td><td>BFF for varied clients, graph-shaped data</td></tr>
</tbody></table></div>
{callout("Expected answer", "<p>REST maps cleanly to HTTP semantics and CDNs. GraphQL reduces round-trips for product UIs but shifts complexity to the server (authz per field, query cost limits, N+1). Many companies use both: REST/gRPC internally, GraphQL at the BFF edge.</p>")}
{callout("Common mistakes", bullets(["No query depth/cost limits in GraphQL", "Ignoring HTTP caching benefits of REST", "Equating GraphQL with 'no versioning needed'"]))}
{callout("Production", bullets(["GitHub public GraphQL API", "Netflix/Shopify BFF patterns", "Twitter/X and many mobile BFFs"]))}
{what_next([("Approaching SD", "19-approaching-sd.html"), ("Rate limiter (API edge)", "interview-sd.html#q4")])}

<h2>SQL vs NoSQL (interview framing)</h2>
{page_meta_bar(difficulty="Medium", reading_mins=6, master_hours="3–5 days", level_focus="Mid–Senior")}
<p>See also the book chapter <a href="23-databases.html">SQL vs NoSQL</a>. In interviews, lead with
<strong>access patterns</strong>, transactions, and query flexibility — not hype.</p>
{callout("Expected answer", "<p>SQL when relations + multi-row transactions matter. NoSQL when partition key access dominates and you need horizontal scale with simpler transactions. Secondary access patterns need indexes, search, or carefully designed dual writes.</p>")}
{what_next([("Databases chapter", "23-databases.html"), ("Replication", "24-replication.html")])}

<h2>Strong consistency vs availability (CAP lite)</h2>
<p>Ticket booking and payments need strong inventory/ledger correctness. Feeds and likes often
choose availability + eventual consistency. Say the product consequence out loud — that is the
interview.</p>
{what_next([("CAP chapter", "25-cap.html"), ("Ticketmaster lab", "interview-sd.html#q10"), ("Payments lab", "interview-sd.html#q13")])}
"""


def company_guides() -> str:
    return f"""
{page_meta_bar(difficulty="Guide", reading_mins=20, master_hours="per-company 1–2 weeks", level_focus="All")}
{prerequisites(["Coding Lab basics", "One system design drill"])}

<p>Company guides below are distilled from publicly discussed interview patterns (candidate
reports, engineering blogs). They are <strong>preparation heuristics</strong>, not leaked
questions.</p>

<h2>Google</h2>
{page_meta_bar(difficulty="Hard", reading_mins=5, master_hours="2–4 weeks", level_focus="L3–L6")}
<ul>
<li><strong>Coding:</strong> Prefer patterns over memorization — graphs, BS on answer, hard DP.
Labs: Islands, Word Ladder, Alien Dictionary, Median/rotated search family.</li>
<li><strong>Design:</strong> Crawler, Maps, Drive, YouTube, rate limiter, KV. Emphasize scale +
freshness + failure.</li>
<li><strong>AI roles:</strong> RAG eval, serving, retrieval quality.</li>
<li><strong>Evaluating:</strong> Clarity, generalization, testing mindset.</li>
</ul>
{what_next([("Web crawler", "interview-sd.html#q12"), ("Maps", "interview-sd.html#q18"), ("AI Lab", "interview-ai.html")])}

<h2>Amazon</h2>
{page_meta_bar(difficulty="Medium→Hard", reading_mins=5, master_hours="2–4 weeks", level_focus="SDE I–II / L5–L6")}
<ul>
<li><strong>Behavioral first:</strong> Leadership Principles with STAR — Ownership, Customer
Obsession, Dive Deep, Bias for Action, Disagree and Commit. See <a href="behavioral.html">Behavioral</a>.</li>
<li><strong>Coding:</strong> Speed + working code. OA favorites: Two Sum family, LRU, islands,
rotting oranges, stock, top-k.</li>
<li><strong>Design:</strong> Shortener, rate limiter, Dynamo-style KV, payments, notifications.</li>
</ul>
{what_next([("Behavioral", "behavioral.html"), ("KV store", "interview-sd.html#q15"), ("Payments", "interview-sd.html#q13")])}

<h2>Meta</h2>
{page_meta_bar(difficulty="Hard", reading_mins=5, master_hours="2–4 weeks", level_focus="E3–E5+")}
<ul>
<li><strong>Coding:</strong> Often two mediums in one round — windows, trees, intervals, heaps.
Min window, meeting rooms, serialize tree.</li>
<li><strong>Design:</strong> News feed, chat, Instagram stories adjacency, counters.</li>
<li><strong>Speed + product sense</strong> matter.</li>
</ul>
{what_next([("Feed lab", "interview-sd.html#q2"), ("Chat lab", "interview-sd.html#q3"), ("Min window", "interview-cp.html#q12")])}

<h2>Microsoft</h2>
{page_meta_bar(difficulty="Medium→Hard", reading_mins=4, master_hours="2–3 weeks", level_focus="L59–L63+")}
<ul>
<li>Coding similar to FAANG mediums; design often Teams/Azure flavored: chat, storage, identity.</li>
<li>Expect collaboration and debugging narratives.</li>
</ul>
{what_next([("Dropbox/Drive", "interview-sd.html#q11"), ("Chat", "interview-sd.html#q3")])}

<h2>Netflix</h2>
{page_meta_bar(difficulty="Hard", reading_mins=4, master_hours="1–3 weeks", level_focus="Senior+")}
<ul>
<li>Video edge + recommendations + resilience culture (circuit breakers, chaos).</li>
<li>Labs: YouTube/video Q6, recsys AI Q6, caching Q9, comparisons CDN/cache.</li>
</ul>
{what_next([("Video lab", "interview-sd.html#q6"), ("Recsys", "interview-ai.html#q6")])}

<h2>Uber / Lyft</h2>
{page_meta_bar(difficulty="Hard", reading_mins=4, master_hours="1–3 weeks", level_focus="Senior+")}
<ul>
<li>Geo, marketplace dispatch, ETA, city sharding — SD Q5. Kafka-heavy data paths Q16.</li>
</ul>
{what_next([("Uber lab", "interview-sd.html#q5"), ("Queues", "26-queues.html")])}

<h2>OpenAI-adjacent / AI platforms</h2>
{page_meta_bar(difficulty="Hard", reading_mins=4, master_hours="2–4 weeks", level_focus="Mid–Staff")}
<ul>
<li>Full <a href="interview-ai.html">AI Lab</a>: RAG, agents, eval, serving, tenancy, security.</li>
</ul>

<h2>Red Hat / enterprise open source</h2>
<ul>
<li>Expect Linux/Kubernetes, operators, observability, and design for on-prem constraints.</li>
<li>Map to scaling, queues, and reliable upgrades — emphasize operable systems.</li>
</ul>
"""


def behavioral() -> str:
    return f"""
{page_meta_bar(difficulty="Medium", reading_mins=18, master_hours="1–2 weeks", level_focus="All")}
{prerequisites(["5–8 real stories from your career", "Target company values if known"])}

<p>Behavioral rounds fail strong coders who cannot tell true, structured stories. Use STAR:
<strong>Situation, Task, Action, Result</strong> — with metrics.</p>

<h2>Story bank checklist</h2>
{bullets([
    "Owned a production incident end-to-end",
    "Disagreed with a lead and changed the outcome",
    "Delivered under tight deadline with tradeoffs",
    "Mentored or multiplied a teammate",
    "Made a technical bet that failed — and what you learned",
    "Cross-team influence without authority",
    "Customer/user obsession example",
    "Simplified a complex system",
])}

<h2>Amazon Leadership Principles — sample mapping</h2>
<div class="table-wrap"><table>
<thead><tr><th>Principle</th><th>What to prove</th><th>Avoid</th></tr></thead>
<tbody>
<tr><td>Customer Obsession</td><td>User impact metrics</td><td>Purely internal vanity metrics</td></tr>
<tr><td>Ownership</td><td>You drove beyond your ticket</td><td>“That was another team’s job”</td></tr>
<tr><td>Dive Deep</td><td>Data you personally inspected</td><td>Hand-wavy root cause</td></tr>
<tr><td>Bias for Action</td><td>Reversible decision speed</td><td>Reckless changes with no safety</td></tr>
<tr><td>Disagree and Commit</td><td>Real dissent then commit</td><td>Fake conflict</td></tr>
</tbody></table></div>

<h2>Mock prompts (practice aloud)</h2>
<details class="qa"><summary><span>Tell me about a time you disagreed with your manager</span></summary>
<div class="qa-body">
<div class="qa-label">Expected shape</div>
<p>Concrete decision, your data, how you escalated respectfully, final outcome, what you’d repeat.</p>
<div class="qa-label">Common mistakes</div>
{bullets(["Trashing your manager", "No resolution", "No learning"])}
</div></details>

<details class="qa"><summary><span>Describe a production outage you handled</span></summary>
<div class="qa-body">
<div class="qa-label">Expected shape</div>
<p>Detection → mitigation → root cause → prevention. Include timelines and customer impact.</p>
<div class="qa-label">Follow-ups</div>
{bullets(["What would you automate?", "How did you communicate?", "What monitors were missing?"])}
</div></details>

<details class="qa"><summary><span>Resume deep-dive: walk me through Project X on your resume</span></summary>
<div class="qa-body">
<p>Interviewers probe anything you wrote. For each resume bullet prepare: problem, your role,
architecture sketch, hardest bug, metric, tradeoff.</p>
{callout("Practice", "<p>Pick every project on your resume and deliver a 90-second version and a 5-minute version.</p>")}
</div></details>

<details class="qa"><summary><span>HR / recruiter screen: Why this company? Why leave?</span></summary>
<div class="qa-body">
{bullets([
    "Be specific about product/tech — not ‘prestige only’",
    "No badmouthing employers",
    "Compensation: defer detailed numbers until later stages if possible; know your range",
])}
</div></details>

<h2>Leveling behavioral differences</h2>
{callout("Junior", "<p>Learning speed, coachability, ownership of small scopes.</p>")}
{callout("Senior", "<p>End-to-end delivery, mentoring, cross-team clear communication.</p>")}
{callout("Staff+", "<p>Org-level impact, technical strategy, multiplying others, managing ambiguity.</p>")}

{what_next([("Company guides", "company-guides.html"), ("Learning paths", "learning-paths.html"), ("System Design Lab", "interview-sd.html")])}
"""


def interview_playbook() -> str:
    return f"""
{page_meta_bar(difficulty="Guide", reading_mins=10, master_hours="read once, reuse forever", level_focus="All")}

<p>This site is optimized for <strong>interviews</strong>, not documentation. Every serious topic
should answer the same questions an interviewer is silently scoring.</p>

<h2>Universal article / answer structure</h2>
<ol class="qa-steps">
<li><strong>Overview</strong> — one sentence + scope.</li>
<li><strong>Why interviewers ask</strong> — skill signal.</li>
<li><strong>What they evaluate</strong> — checklist.</li>
<li><strong>Level expectations</strong> — Junior → Principal.</li>
<li><strong>Expected answer shape</strong> — the arc to hit.</li>
<li><strong>Key concepts / solution</strong> — diagrams + steps.</li>
<li><strong>Follow-ups</strong> — timed probes.</li>
<li><strong>Common mistakes</strong> — fail patterns.</li>
<li><strong>Production examples</strong> — Google/Netflix/Uber/Amazon…</li>
<li><strong>Best practices &amp; when NOT to use</strong>.</li>
<li><strong>Summary + practice</strong> + related next topics.</li>
</ol>

<h2>Where this lives on the site</h2>
{bullets([
    "<a href=\"interview-cp.html\">Coding Lab</a> — each question enriched with the structure above",
    "<a href=\"interview-sd.html\">System Design Lab</a> — same",
    "<a href=\"interview-ai.html\">AI Lab</a> — same",
    "<a href=\"comparisons.html\">Comparisons</a> — tradeoff articles",
    "<a href=\"learning-paths.html\">Learning paths</a> — role roadmaps",
    "<a href=\"cheat-sheets.html\">Cheat sheets</a> — last-minute flashcards",
    "<a href=\"company-guides.html\">Company guides</a>",
    "<a href=\"behavioral.html\">Behavioral / HR / resume</a>",
])}

<h2>Difficulty &amp; time</h2>
<p>Cards and guides show difficulty, rehearsal minutes, and mastery estimates. Use them to plan
sprints — not to read passively.</p>

{what_next([("Learning paths", "learning-paths.html"), ("Coding Lab", "interview-cp.html")])}
"""


def cheat_sheets() -> str:
    return f"""
{page_meta_bar(difficulty="Easy→Hard", reading_mins=15, master_hours="night-before refresh", level_focus="All")}
{prerequisites(["Have practiced the labs once", "Do not first-learn from cheat sheets"])}

<p>One-page revision notes for last-minute prep. Expand a card, say it aloud in under two minutes,
then close it.</p>

<details class="qa" open><summary><span>Coding patterns flashcard</span></summary>
<div class="qa-body">
{bullets([
    "Hash map — complement, frequency, first unique",
    "Two pointers — sorted pair, container, linked-list mid",
    "Sliding window — fixed / variable; maintain invariant",
    "Binary search — on index or on answer space",
    "BFS/DFS — islands, shortest unweighted, topo",
    "Heap — top-k, merge k, streaming median",
    "Intervals — sort by start; sweep for rooms",
    "DP — define state, transition, base; space optimize last",
])}
<p><a href="interview-cp.html">Open Coding Lab</a> · <a href="17-cheat-sheet.html">CP chapter cheat sheet</a></p>
</div></details>

<details class="qa"><summary><span>System design whiteboard arc</span></summary>
<div class="qa-body">
<ol class="qa-steps">
<li>Clarify functional + non-functional (QPS, size, latency, consistency).</li>
<li>API + data model sketch.</li>
<li>High-level boxes + request flow.</li>
<li>Deep dive hottest path (cache, shard key, queue).</li>
<li>Failure modes + scale bottlenecks.</li>
<li>Trade-offs and what you’d build in v1 vs v2.</li>
</ol>
<p><a href="interview-sd.html">System Design Lab</a> · <a href="comparisons.html">Comparisons</a></p>
</div></details>

<details class="qa"><summary><span>AI / RAG interview flashcard</span></summary>
<div class="qa-body">
{bullets([
    "RAG = retrieve → augment prompt → generate; eval retrieval and answer separately",
    "Chunking, embeddings, hybrid search, rerank — name failure modes",
    "Agents = loop with tools + memory + stop conditions; watch cost/latency",
    "MCP = tool/protocol boundary; authz and least privilege",
    "Serving: batching, KV cache, quantization, tenancy quotas",
])}
<p><a href="interview-ai.html">AI Lab</a></p>
</div></details>

<details class="qa"><summary><span>Behavioral STAR in 60 seconds</span></summary>
<div class="qa-body">
<p><strong>S/T</strong> 15s context · <strong>A</strong> 30s your moves · <strong>R</strong> 15s metric + learning.</p>
<p><a href="behavioral.html">Behavioral lab</a></p>
</div></details>

{what_next([("Interview playbook", "interview-playbook.html"), ("Company guides", "company-guides.html")])}
"""


GUIDES = [
    {
        "slug": "interview-playbook",
        "part": "front",
        "eyebrow": "How to prepare",
        "title": "Interview-focused playbook",
        "subtitle": "The structure every answer and article should follow — what interviewers score.",
        "body": interview_playbook,
        "after": "contents",
        "nav_title": "Interview playbook",
    },
    {
        "slug": "learning-paths",
        "part": "front",
        "eyebrow": "Roadmaps",
        "title": "Learning paths by role",
        "subtitle": "Backend, AI, Data, DevOps, and Staff/Principal — prerequisites and what to do next.",
        "body": learning_paths,
        "after": "interview-playbook",
        "nav_title": "Learning paths",
    },
    {
        "slug": "cheat-sheets",
        "part": "front",
        "eyebrow": "Quick revision",
        "title": "Cheat sheets & flashcards",
        "subtitle": "Last-minute one-pagers for coding patterns, system design arcs, AI, and behavioral.",
        "body": cheat_sheets,
        "after": "learning-paths",
        "nav_title": "Cheat sheets",
    },
    {
        "slug": "comparisons",
        "part": "sd",
        "eyebrow": "Trade-offs",
        "title": "Technology comparisons for interviews",
        "subtitle": "Kafka vs RabbitMQ, Redis vs Memcached, REST vs GraphQL, and more — with expected answers.",
        "body": comparisons,
        "after": "interview-sd",
        "nav_title": "Comparisons",
    },
    {
        "slug": "company-guides",
        "part": "front",
        "eyebrow": "Company prep",
        "title": "Company-specific interview guides",
        "subtitle": "Google, Amazon, Meta, Microsoft, Netflix, Uber, AI labs, and enterprise patterns.",
        "body": company_guides,
        "after": "cheat-sheets",
        "nav_title": "Company guides",
    },
    {
        "slug": "behavioral",
        "part": "front",
        "eyebrow": "Behavioral & HR",
        "title": "Behavioral, HR, and resume interviews",
        "subtitle": "STAR stories, Leadership Principles, resume deep-dives, and mock prompts.",
        "body": behavioral,
        "after": "company-guides",
        "nav_title": "Behavioral & HR",
    },
]


def update_nav() -> None:
    data = json.loads(NAV.read_text())
    chapters = [c for c in data["chapters"] if c["id"] not in {g["slug"] for g in GUIDES}]
    by_id = {c["id"]: i for i, c in enumerate(chapters)}
    for g in GUIDES:
        entry = {
            "id": g["slug"],
            "num": None,
            "title": g["nav_title"],
            "part": g["part"],
            "href": f"chapters/{g['slug']}.html",
            "guide": True,
        }
        after = g["after"]
        insert_at = by_id.get(after, len(chapters) - 1) + 1
        chapters.insert(insert_at, entry)
        by_id = {c["id"]: i for i, c in enumerate(chapters)}
    data["chapters"] = chapters
    NAV.write_text(json.dumps(data, indent=2) + "\n")
    print(f"nav updated ({len(chapters)} entries)")


def main() -> None:
    for g in GUIDES:
        html = guide_shell(
            slug=g["slug"],
            part=g["part"],
            eyebrow=g["eyebrow"],
            title=g["title"],
            subtitle=g["subtitle"],
            body=g["body"](),
        )
        path = OUT / f"{g['slug']}.html"
        path.write_text(html)
        print("wrote", path.name)
    update_nav()


if __name__ == "__main__":
    main()
