#!/usr/bin/env python3
"""System design interview Q&As — deep, diagrammed L4–L6 whiteboard tracks."""
from __future__ import annotations

from interview_helpers import (
    bullets,
    callout,
    code_block,
    drill_section,
    figure_diagram,
    qa_block,
    steps,
)


def sd_questions() -> list[str]:
    q: list[str] = []

    q.append(
        qa_block(
            qnum=1,
            title="Design a URL Shortener (Bitly)",
            asked="Amazon, Google, Microsoft, Uber — most common system-design opener",
            difficulty="Medium",
            pattern="Hashing · base62 IDs · read-heavy cache",
            prompt=(
                "Design a service like bit.ly: users submit a long URL and get a short link; "
                "opening the short link redirects to the original. Expect ~100M new URLs/month "
                "and a much higher read:write ratio. Walk a full 45-minute design."
            ),
            sections=[
                (
                    "Clarify",
                    bullets(
                        [
                            "Custom aliases? Expiry? Auth?",
                            "Analytics (click counts) required?",
                            "Latency: redirect p99 &lt; 100ms?",
                            "Availability target (e.g. 99.9%)?",
                            "Assume ~7-char base62 codes unless they specify otherwise.",
                        ]
                    ),
                ),
                (
                    "Diagram",
                    figure_diagram("url-shortener-detailed", "URL shortener write and read paths"),
                ),
                (
                    "Step-by-step whiteboard",
                    steps(
                        [
                            "<strong>API:</strong> <code>POST /shorten {url, alias?}</code> → "
                            "code; <code>GET /{code}</code> → 302 Location: long URL.",
                            "<strong>Capacity:</strong> 100M/mo ≈ 40 writes/s avg; reads can be "
                            "thousands/s — cache is mandatory. Storage: 100M × ~500B ≈ 50GB+/yr "
                            "metadata (order-of-magnitude OK).",
                            "<strong>ID generation (pick one &amp; defend):</strong> "
                            "(1) distributed counter + base62; (2) hash URL + collision handling; "
                            "(3) pre-generated key pool for bursts.",
                            "<strong>Data model:</strong> code → {long_url, user_id, created, "
                            "expires, clicks?}. KV/NoSQL or sharded SQL by code hash.",
                            "<strong>Read path:</strong> edge/CDN optional → LB → app → Redis → "
                            "DB. Prefer <strong>302</strong> (mapping can change; analytics stay "
                            "server-side) unless they insist on 301.",
                            "<strong>Analytics:</strong> async click events to Kafka/queue — "
                            "never block redirect.",
                            "<strong>Abuse:</strong> rate-limit shorten; malware URL scan offline.",
                        ]
                    ),
                ),
                (
                    "Deep dives",
                    bullets(
                        [
                            "<strong>Hot keys:</strong> viral links — cache replicas / local caches.",
                            "<strong>Enumeration:</strong> avoid raw sequential public IDs; "
                            "salt / skip / encrypt.",
                            "<strong>Multi-region:</strong> replicate read-only mappings; write "
                            "to primary with async replication.",
                            "<strong>Custom aliases:</strong> conditional put; reject if taken.",
                        ]
                    ),
                ),
                (
                    "What strong answers sound like",
                    callout(
                        "Signal",
                        "<p>One ID scheme with collision story, short read path, analytics "
                        "explicitly async, and a clear 301 vs 302 opinion.</p>",
                    ),
                ),
            ],
        )
    )

    q.append(
        qa_block(
            qnum=2,
            title="Design Instagram / News Feed",
            asked="Meta, Instagram, Twitter/X interviews",
            difficulty="Hard",
            pattern="Hybrid fan-out · timeline cache · media CDN",
            prompt=(
                "Design a photo-sharing social network: follow users, upload photos, see a home "
                "feed of posts from people you follow (roughly reverse-chronological with light "
                "ranking)."
            ),
            sections=[
                (
                    "Clarify",
                    bullets(
                        [
                            "Scale: hundreds of millions of users?",
                            "Celebrity / mega-follower problem in scope?",
                            "Stories? Likes counters? Ranking ML?",
                            "Consistency: eventual feed OK?",
                        ]
                    ),
                ),
                (
                    "Diagram",
                    figure_diagram("feed-hybrid-fanout", "Hybrid fan-out for news feed"),
                ),
                (
                    "Step-by-step whiteboard",
                    steps(
                        [
                            "<strong>Write media:</strong> pre-signed upload → object store + CDN; "
                            "metadata row (post_id, author, caption, media_url, ts).",
                            "<strong>Fan-out on write:</strong> push post_id into each follower's "
                            "timeline cache (Redis lists) — great for normal users.",
                            "<strong>Fan-out on read / pull:</strong> for celebrities, do <em>not</em> "
                            "push to tens of millions of timelines; merge recent posts at read time.",
                            "<strong>Hybrid:</strong> write-fanout for normals, pull for celebs "
                            "(or inactive users).",
                            "<strong>Read path:</strong> auth → timeline cache → hydrate posts → "
                            "CDN URLs.",
                            "<strong>Ranking:</strong> start chronological; add retrieval + re-rank "
                            "stage later.",
                            "<strong>Sharding:</strong> user_id for timelines; post_id for posts.",
                        ]
                    ),
                ),
                (
                    "Deep dives",
                    bullets(
                        [
                            "Counters (likes/views): sharded in-memory with periodic flush; "
                            "approximate display OK.",
                            "Notifications / stories: separate services + queues.",
                            "Feed can be eventually consistent; durable post metadata is enough "
                            "for ACK.",
                        ]
                    ),
                ),
            ],
        )
    )

    q.append(
        qa_block(
            qnum=3,
            title="Design WhatsApp / Chat",
            asked="Meta, WhatsApp, Slack, Discord-style rounds",
            difficulty="Hard",
            pattern="WebSocket · durable log · presence · group fan-out",
            prompt=(
                "Design 1:1 and group messaging with delivery receipts, online presence, and "
                "media sharing. Focus on low latency and reliability."
            ),
            sections=[
                (
                    "Clarify",
                    bullets(
                        [
                            "E2E encryption in scope?",
                            "Max group size?",
                            "Multi-device sync?",
                            "Message history retention?",
                        ]
                    ),
                ),
                (
                    "Diagram",
                    figure_diagram("chat-message-path", "Chat message delivery path"),
                ),
                (
                    "Step-by-step whiteboard",
                    steps(
                        [
                            "<strong>Connections:</strong> sticky WebSocket/MQTT to chat servers; "
                            "presence map user→server in Redis.",
                            "<strong>Send path:</strong> client → chat server → durable queue/log "
                            "(Kafka) → fan-out to recipient inboxes → push to online sockets or "
                            "store-and-forward if offline.",
                            "<strong>ACK:</strong> persist before ACK to sender (at-least-once); "
                            "clients de-dupe by message_id.",
                            "<strong>Ordering:</strong> per-conversation monotonic sequence from "
                            "a single partition/writer.",
                            "<strong>Groups:</strong> small → fan-out to members; large → group "
                            "log + members catch up / notify online only.",
                            "<strong>Media:</strong> upload to blob store; message carries URL/"
                            "thumbnail.",
                            "<strong>Presence:</strong> heartbeats with short TTL.",
                            "<strong>Receipts:</strong> separate lightweight events; do not block "
                            "delivery.",
                        ]
                    ),
                ),
                (
                    "E2E note",
                    callout(
                        "If asked",
                        "<p>Server stores ciphertext + metadata; keys on devices. Acknowledge "
                        "feature tradeoffs (server-side search hard).</p>",
                    ),
                ),
            ],
        )
    )

    q.append(
        qa_block(
            qnum=4,
            title="Design a Rate Limiter",
            asked="Amazon, Stripe, Cloudflare, Google — building-block favorite",
            difficulty="Medium",
            pattern="Token bucket · sliding window · Redis",
            prompt=(
                "Design a distributed rate limiter for an API gateway: e.g. 100 requests per "
                "user per minute, consistent across many gateway instances."
            ),
            sections=[
                (
                    "Algorithms (know 3)",
                    bullets(
                        [
                            "<strong>Token bucket:</strong> refill rate r; burst capacity — "
                            "industry default.",
                            "<strong>Leaky bucket:</strong> smooth constant outflow.",
                            "<strong>Fixed window:</strong> simple counters; edge burst problem.",
                            "<strong>Sliding window log/counter:</strong> fairer, more cost.",
                        ]
                    ),
                ),
                (
                    "Diagram",
                    figure_diagram("rate-limiter-token", "Gateway + Redis token bucket"),
                ),
                (
                    "Step-by-step whiteboard",
                    steps(
                        [
                            "Gateways call a shared store (Redis) before forwarding.",
                            "Use atomic ops (INCR+EXPIRE or Lua) for token bucket — avoid races.",
                            "On deny: HTTP 429 + Retry-After.",
                            "Dimensions: per API key / IP / endpoint / tenant.",
                            "Multi-region: regional limiters + global budget, or accept "
                            "approximate limits.",
                            "Redis down: product call — fail open vs fail closed.",
                        ]
                    ),
                ),
                (
                    "Pseudo Redis check",
                    code_block(
                        "text",
                        """# token bucket keys: tokens={key}, ts={key}
# atomic Lua: refill based on elapsed time, consume 1 if tokens>=1
# else return limited""",
                    ),
                ),
            ],
        )
    )

    q.append(
        qa_block(
            qnum=5,
            title="Design Uber / Ride Sharing",
            asked="Uber, Lyft, DoorDash-adjacent geo interviews",
            difficulty="Hard",
            pattern="Geo index · matching · trip state machine",
            prompt=(
                "Design ride-hailing: riders request trips, nearby drivers are matched, locations "
                "update in realtime, pricing/ETA computed."
            ),
            sections=[
                (
                    "Clarify",
                    bullets(
                        [
                            "Cities / regions in scope?",
                            "ETA accuracy expectations?",
                            "Surge pricing?",
                            "Driver app battery / update frequency?",
                        ]
                    ),
                ),
                (
                    "Diagram",
                    figure_diagram("uber-matching", "Geo index and ride matching"),
                ),
                (
                    "Step-by-step whiteboard",
                    steps(
                        [
                            "<strong>Location stream:</strong> drivers send GPS every few seconds → "
                            "update geo index (geohash / S2 cells in Redis or specialized store).",
                            "<strong>Request:</strong> rider → query nearby cells → filter "
                            "status/vehicle → rank by ETA/rating → offer with timeout → expand "
                            "ring on miss.",
                            "<strong>Double dispatch:</strong> atomic claim / CAS on driver "
                            "status with lease; only one rider wins.",
                            "<strong>Trip lifecycle:</strong> requested → matched → enroute → "
                            "ongoing → completed (state machine + events to billing/notify).",
                            "<strong>ETA:</strong> map-match + traffic-aware routing service; "
                            "cache segments.",
                            "<strong>Surge:</strong> demand/supply per cell, smoothed (EMA), "
                            "capped rate of change.",
                            "<strong>Scale:</strong> shard by city/region — traffic is local.",
                        ]
                    ),
                ),
            ],
        )
    )

    q.append(
        qa_block(
            qnum=6,
            title="Design YouTube / Video Streaming",
            asked="Google, Netflix, Meta — storage + CDN heavy",
            difficulty="Hard",
            pattern="Transcoding pipeline · CDN · adaptive bitrate",
            prompt=(
                "Design video upload and streaming: users upload; millions watch with adaptive "
                "quality worldwide."
            ),
            sections=[
                (
                    "Diagram",
                    figure_diagram("youtube-cdn-pipeline", "Upload, transcode, CDN playback"),
                ),
                (
                    "Step-by-step whiteboard",
                    steps(
                        [
                            "<strong>Upload:</strong> pre-signed URL → direct to object store; "
                            "metadata = processing.",
                            "<strong>Pipeline:</strong> queue workers transcode many resolutions/"
                            "codecs, thumbs, duration → HLS/DASH segments → mark ready. "
                            "Fast-start low-res first.",
                            "<strong>Playback:</strong> client fetches manifest; CDN serves "
                            "segments; origin is object store; ABR by bandwidth.",
                            "<strong>Hot titles:</strong> heavy edge caching; short TTL for live.",
                            "<strong>Live:</strong> separate ingest POPs → packager → CDN; not "
                            "the VOD path.",
                            "<strong>Cost:</strong> lifecycle to cold storage; fewer bitrates for "
                            "rarely watched; copyright fingerprinting async.",
                            "<strong>Recs:</strong> offline ML + online re-rank — off the play path.",
                        ]
                    ),
                ),
                (
                    "Key principle",
                    callout(
                        "Never",
                        "<p>Never transcode on the user-facing request path. Processing is a "
                        "pipeline; serving is CDN.</p>",
                    ),
                ),
            ],
        )
    )

    q.append(
        qa_block(
            qnum=7,
            title="Design a Notification System",
            asked="Amazon, Meta, Uber, Slack",
            difficulty="Medium",
            pattern="Fan-out · priority queues · templates · DLQ",
            prompt=(
                "Design multi-channel notifications: push, email, SMS, in-app — with preferences, "
                "retries, and high throughput."
            ),
            sections=[
                (
                    "Diagram",
                    figure_diagram("notification-pipeline", "Notification fan-out pipeline"),
                ),
                (
                    "Step-by-step whiteboard",
                    steps(
                        [
                            "Producers enqueue jobs (do not block product writes).",
                            "Preferences/quiet-hours gate before send.",
                            "Kafka topics by priority/channel → workers render templates → "
                            "provider adapters (APNs/FCM, SES, Twilio).",
                            "Idempotency keys; rate-limit per user and per provider.",
                            "Retries with exponential backoff → DLQ for poison messages.",
                            "Large audiences: chunked fan-out tasks.",
                            "Aim at-least-once + idempotent display — not exactly-once fantasy.",
                        ]
                    ),
                ),
            ],
        )
    )

    q.append(
        qa_block(
            qnum=8,
            title="Design Typeahead / Search Autocomplete",
            asked="Google, Amazon, Twitter",
            difficulty="Medium",
            pattern="Trie · top-k · edge cache",
            prompt=(
                "Design search autocomplete that returns top suggestions as the user types, with "
                "low latency and some trending awareness."
            ),
            sections=[
                (
                    "Diagram",
                    figure_diagram("autocomplete-trie", "Prefix index autocomplete"),
                ),
                (
                    "Step-by-step whiteboard",
                    steps(
                        [
                            "<strong>Offline:</strong> aggregate query logs → top-k per prefix → "
                            "build trie/prefix index → ship snapshots to servers/edge.",
                            "<strong>Online:</strong> client debounces; request prefix → memory "
                            "trie returns top-k (&lt;50ms); light personalization/trending re-rank.",
                            "Cache popular prefixes at CDN/edge.",
                            "Limit prefix length; store only top-k not full postings.",
                            "Shard trie by first character(s) if needed.",
                            "Refresh index on minutes cadence — not per keystroke.",
                        ]
                    ),
                ),
            ],
        )
    )

    q.append(
        qa_block(
            qnum=9,
            title="Design a Distributed Cache",
            asked="Amazon, Microsoft, Oracle — Redis/Memcached style",
            difficulty="Hard",
            pattern="Consistent hashing · replication · eviction",
            prompt=(
                "Design a distributed in-memory cache: get/put/delete, TTL, HA, horizontal scale."
            ),
            sections=[
                (
                    "Diagram",
                    figure_diagram("consistent-hash-cache", "Consistent hashing ring"),
                ),
                (
                    "Step-by-step whiteboard",
                    steps(
                        [
                            "Client or proxy uses consistent hashing → shard.",
                            "Each shard: primary + replicas (async or semi-sync).",
                            "Eviction: LRU/LFU + TTL per node.",
                            "Membership via gossip/config service; virtual nodes for balance.",
                            "<strong>Hot keys:</strong> replicate popular keys; local caches.",
                            "<strong>Stampede:</strong> soft TTL + singleflight / probabilistic "
                            "early expire.",
                            "Write strategies: invalidate-on-write common; write-through / "
                            "behind when justified.",
                            "CAP: prefer AP for cache; miss → load DB.",
                            "Persistence optional — usually ephemeral by design.",
                        ]
                    ),
                ),
            ],
        )
    )

    q.append(
        qa_block(
            qnum=10,
            title="Design Ticketmaster / Event Booking",
            asked="Amazon, Ticketmaster-style concurrency interviews",
            difficulty="Hard",
            pattern="Inventory locks · holds · idempotent payment",
            prompt=(
                "Design ticketing for concerts: browse events, hold seats, pay, issue tickets — "
                "without double-selling under spikes."
            ),
            sections=[
                (
                    "Diagram",
                    figure_diagram("ticket-hold-checkout", "Seat hold and checkout"),
                ),
                (
                    "Step-by-step whiteboard",
                    steps(
                        [
                            "<strong>Browse:</strong> read replicas + CDN for event pages; "
                            "seat maps cached carefully.",
                            "<strong>Inventory states:</strong> available → held → sold.",
                            "<strong>Hold:</strong> soft lock with short TTL (2–10 min) via Redis "
                            "or conditional row update.",
                            "<strong>Checkout:</strong> create hold → payment intent → on success "
                            "commit seats + ticket IDs; on fail/expiry release hold.",
                            "<strong>Idempotency:</strong> keys on payment webhooks — no double "
                            "charge / double sell.",
                            "<strong>Consistency:</strong> strong on inventory (CAS / "
                            "<code>UPDATE … WHERE status='available'</code>).",
                            "<strong>Scale:</strong> shard by event_id; waiting rooms / queues for "
                            "mega on-sales.",
                        ]
                    ),
                ),
                (
                    "Strong closer",
                    callout(
                        "Contrast with feeds",
                        "<p>Feeds can be eventually consistent. Ticket inventory cannot. Say "
                        "that contrast out loud — interviewers love it.</p>",
                    ),
                ),
            ],
        )
    )

    return q


def sd_lab_body() -> str:
    intro = """
<p>This lab is for <strong>L4–L6 system design loops</strong>: the prompts that show up again and
again — URL shortener as a warmup, then chat, feed, rides, video, or a focused building block
like rate limiting.</p>

<p class="drill-intro"><strong>How to use it:</strong> Practice a 45-minute structure every time —
<strong>clarify → capacity sketch → API → diagram → data model → deep dives → failures</strong>.
Open a card, study it, then redraw from memory on a blank page.</p>

<figure class="diagram native">
<img src="../assets/diagrams/url-shortener-detailed.svg" alt="URL shortener design overview" loading="lazy" />
</figure>

<p class="drill-intro">Related chapters:
<a href="19-approaching-sd.html">Approaching SD</a>,
<a href="21-scaling.html">Scaling</a>,
<a href="22-caching.html">Caching</a>,
<a href="28-url-shortener.html">URL shortener</a>,
<a href="29-whatsapp.html">WhatsApp</a>,
<a href="30-instagram.html">Instagram</a>,
<a href="34-uber.html">Uber</a>.</p>

<ul class="lab-toc">
  <li><a href="#q1"><span>Q1</span> URL shortener</a></li>
  <li><a href="#q2"><span>Q2</span> Instagram / news feed</a></li>
  <li><a href="#q3"><span>Q3</span> WhatsApp / chat</a></li>
  <li><a href="#q4"><span>Q4</span> Rate limiter</a></li>
  <li><a href="#q5"><span>Q5</span> Uber / ride sharing</a></li>
  <li><a href="#q6"><span>Q6</span> YouTube / video</a></li>
  <li><a href="#q7"><span>Q7</span> Notification system</a></li>
  <li><a href="#q8"><span>Q8</span> Search autocomplete</a></li>
  <li><a href="#q9"><span>Q9</span> Distributed cache</a></li>
  <li><a href="#q10"><span>Q10</span> Ticketmaster / booking</a></li>
</ul>
"""
    blocks = sd_questions()
    out = []
    for i, block in enumerate(blocks, start=1):
        out.append(block.replace('<details class="qa">', f'<details class="qa" id="q{i}">', 1))
    return intro + "\n".join(out)


def sd_chapter_drills() -> dict[str, str]:
    return {
        "28-url-shortener": drill_section(
            "Interview drill — URL shortener",
            "If you only practice one design cold, make it this.",
            [
                qa_block(
                    qnum=1,
                    title="Design Bitly (full)",
                    asked="Amazon, Google, Microsoft",
                    difficulty="Medium",
                    pattern="KV + cache",
                    prompt="Shorten + redirect + analytics.",
                    sections=[
                        (
                            "Steps",
                            figure_diagram("url-shortener-detailed", "URL shortener")
                            + steps(
                                [
                                    "Clarify + capacity (read-heavy).",
                                    "Pick ID scheme; KV mapping; Redis on read.",
                                    "302 redirect; analytics async.",
                                ]
                            )
                            + "<p><a href=\"interview-sd.html#q1\">Lab Q1</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Custom aliases",
                    asked="Follow-up",
                    difficulty="Medium",
                    pattern="Uniqueness",
                    prompt="User-chosen short codes?",
                    sections=[
                        (
                            "Approach",
                            "<p>Conditional put; reject if taken; rate-limit; validate charset; "
                            "phishing checks.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="301 vs 302",
                    asked="Common follow-up",
                    difficulty="Easy",
                    pattern="HTTP caching",
                    prompt="Which redirect status?",
                    sections=[
                        (
                            "Approach",
                            "<p>302/307 keep control. 301 caches in browsers — faster but harder "
                            "to update or count.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Global latency",
                    asked="Microsoft, Amazon",
                    difficulty="Medium",
                    pattern="Multi-region",
                    prompt="Fast redirects worldwide.",
                    sections=[
                        (
                            "Approach",
                            "<p>Regional read replicas; edge cache hot codes; primary writes.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Predictable IDs",
                    asked="Security follow-up",
                    difficulty="Medium",
                    pattern="Enumeration",
                    prompt="Sequential IDs leak volume.",
                    sections=[
                        (
                            "Approach",
                            "<p>Salted hashes, skip counters, or encrypted IDs; rate-limit guessing.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-sd.html",
        ),
        "29-whatsapp": drill_section(
            "Interview drill — Chat",
            "Connections, durability, fan-out — not UI.",
            [
                qa_block(
                    qnum=1,
                    title="Design WhatsApp",
                    asked="Meta, WhatsApp",
                    difficulty="Hard",
                    pattern="WS + inbox",
                    prompt="1:1 and group messaging.",
                    sections=[
                        (
                            "Steps",
                            figure_diagram("chat-message-path", "Chat path")
                            + "<p><a href=\"interview-sd.html#q3\">Lab Q3</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Read receipts at scale",
                    asked="Follow-up",
                    difficulty="Medium",
                    pattern="Async events",
                    prompt="Blue ticks without melting DB?",
                    sections=[
                        (
                            "Approach",
                            "<p>Separate lightweight events; batch writes; eventual OK; never "
                            "block message delivery.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Large group chats",
                    asked="Discord / Slack",
                    difficulty="Hard",
                    pattern="Fan-out",
                    prompt="10k-member group?",
                    sections=[
                        (
                            "Approach",
                            "<p>Write to group log; members pull/catch up; push only online "
                            "subscribers.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="E2E encryption",
                    asked="Signal/WhatsApp",
                    difficulty="Hard",
                    pattern="Keys on device",
                    prompt="What does the server store?",
                    sections=[
                        (
                            "Approach",
                            "<p>Ciphertext + metadata; identity/prekeys on devices.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Message ordering",
                    asked="Meta",
                    difficulty="Medium",
                    pattern="Per-chat seq",
                    prompt="How do you order messages?",
                    sections=[
                        (
                            "Approach",
                            "<p>Per-chat monotonic sequence from one writer partition.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-sd.html",
        ),
        "30-instagram": drill_section(
            "Interview drill — Feed",
            "Feeds are a fan-out problem.",
            [
                qa_block(
                    qnum=1,
                    title="Design Instagram feed",
                    asked="Meta",
                    difficulty="Hard",
                    pattern="Hybrid fan-out",
                    prompt="Home feed + media.",
                    sections=[
                        (
                            "Steps",
                            figure_diagram("feed-hybrid-fanout", "Hybrid fan-out")
                            + "<p><a href=\"interview-sd.html#q2\">Lab Q2</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Celebrity problem",
                    asked="Twitter/Meta",
                    difficulty="Hard",
                    pattern="Fan-out on read",
                    prompt="50M followers post?",
                    sections=[
                        (
                            "Approach",
                            "<p>Do not push to 50M timelines. Store post; mix at read/merge time.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Feed ranking",
                    asked="Meta",
                    difficulty="Medium",
                    pattern="Retrieve + rank",
                    prompt="Not purely chronological?",
                    sections=[
                        (
                            "Approach",
                            "<p>Candidates from timeline/cache → features → light ranker → diversity.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Counter service",
                    asked="Instagram",
                    difficulty="Medium",
                    pattern="Sharded counters",
                    prompt="Likes at huge QPS.",
                    sections=[
                        (
                            "Approach",
                            "<p>Sharded in-memory counters; flush periodically; approximate OK.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Stories vs feed",
                    asked="Meta",
                    difficulty="Medium",
                    pattern="TTL data",
                    prompt="Ephemeral stories?",
                    sections=[
                        (
                            "Approach",
                            "<p>Separate store with 24h TTL; CDN/blob lifecycle policies.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-sd.html",
        ),
        "34-uber": drill_section(
            "Interview drill — Ride sharing",
            "Geo + matching + state machines — keep it regional.",
            [
                qa_block(
                    qnum=1,
                    title="Design Uber",
                    asked="Uber, Lyft",
                    difficulty="Hard",
                    pattern="Geo + matching",
                    prompt="Match riders to drivers.",
                    sections=[
                        (
                            "Steps",
                            figure_diagram("uber-matching", "Matching")
                            + "<p><a href=\"interview-sd.html#q5\">Lab Q5</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Avoid double dispatch",
                    asked="Uber",
                    difficulty="Hard",
                    pattern="Atomic claim",
                    prompt="Two riders, one driver?",
                    sections=[
                        (
                            "Approach",
                            "<p>CAS driver status; offer lease with timeout; one claim wins.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="ETA accuracy",
                    asked="Follow-up",
                    difficulty="Medium",
                    pattern="Routing",
                    prompt="How is ETA computed?",
                    sections=[
                        (
                            "Approach",
                            "<p>Map-match GPS; traffic-aware routing; cache segments.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Surge pricing",
                    asked="Uber",
                    difficulty="Medium",
                    pattern="Demand/supply",
                    prompt="Surge without wild oscillation?",
                    sections=[
                        (
                            "Approach",
                            "<p>Per-cell imbalance; EMA smooth; cap change rate; show before confirm.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="City sharding",
                    asked="Scale",
                    difficulty="Medium",
                    pattern="Regional",
                    prompt="How do you shard?",
                    sections=[
                        (
                            "Approach",
                            "<p>Most state is city-local; global only for identity/billing.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-sd.html",
        ),
        "22-caching": drill_section(
            "Interview drill — Caching",
            "Operate systems, don't recite buzzwords.",
            [
                qa_block(
                    qnum=1,
                    title="Design a distributed cache",
                    asked="Amazon, Microsoft",
                    difficulty="Hard",
                    pattern="Consistent hashing",
                    prompt="Redis-like get/put fleet.",
                    sections=[
                        (
                            "Steps",
                            figure_diagram("consistent-hash-cache", "Hash ring")
                            + "<p><a href=\"interview-sd.html#q9\">Lab Q9</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Cache stampede",
                    asked="Amazon",
                    difficulty="Medium",
                    pattern="Singleflight",
                    prompt="Hot key expires → DB melt.",
                    sections=[
                        (
                            "Approach",
                            "<p>Soft TTL + background refresh; request coalescing; probabilistic early expire.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Write strategies",
                    asked="Microsoft",
                    difficulty="Medium",
                    pattern="Through / behind / around",
                    prompt="Cache vs DB first?",
                    sections=[
                        (
                            "Approach",
                            "<p>Write-through for freshness; write-behind for throughput (risk); "
                            "invalidate-on-write is the common microservice pattern.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="CDN vs app cache",
                    asked="All",
                    difficulty="Easy",
                    pattern="Edge vs origin",
                    prompt="What belongs on CDN?",
                    sections=[
                        (
                            "Approach",
                            "<p>Cacheable HTTP near users. Personalized/auth data stays in app/Redis.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Rate limiter with Redis",
                    asked="Stripe, Amazon",
                    difficulty="Medium",
                    pattern="Token bucket",
                    prompt="Per-API-key limits across gateways.",
                    sections=[
                        (
                            "Steps",
                            figure_diagram("rate-limiter-token", "Rate limiter")
                            + "<p><a href=\"interview-sd.html#q4\">Lab Q4</a>.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-sd.html",
        ),
        "21-scaling": drill_section(
            "Interview drill — Scaling",
            "One box → fleet thoughtfully.",
            [
                qa_block(
                    qnum=1,
                    title="Horizontal scale a read-heavy API",
                    asked="Amazon, Google",
                    difficulty="Medium",
                    pattern="LB + cache",
                    prompt="Traffic ×20 — what first?",
                    sections=[
                        (
                            "Approach",
                            steps(
                                [
                                    "Measure bottleneck.",
                                    "LB + stateless app replicas.",
                                    "Cache / read replicas.",
                                    "Shard only when needed.",
                                ]
                            ),
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="L4 vs L7 load balancing",
                    asked="Amazon",
                    difficulty="Medium",
                    pattern="LB choice",
                    prompt="When each? Sticky sessions?",
                    sections=[
                        (
                            "Approach",
                            "<p>L4 for raw TCP/WS scale; L7 for path/auth routing. Prefer external "
                            "session store over sticky.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Graceful degradation",
                    asked="Netflix-style",
                    difficulty="Medium",
                    pattern="Fallbacks",
                    prompt="Dependency down?",
                    sections=[
                        (
                            "Approach",
                            "<p>Timeouts, circuit breakers, cached fallbacks, disable non-critical widgets.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Backpressure",
                    asked="Google, Uber",
                    difficulty="Medium",
                    pattern="Queues + shed",
                    prompt="Producers outrun consumers.",
                    sections=[
                        (
                            "Approach",
                            "<p>Bounded queues, 503/retry-after, drop low priority, autoscale consumers.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Idempotent APIs",
                    asked="Stripe, Amazon",
                    difficulty="Medium",
                    pattern="Idempotency keys",
                    prompt="Retries without double-charge?",
                    sections=[
                        (
                            "Approach",
                            "<p>Client key stored with result; replays return first result. "
                            "Critical for booking too — <a href=\"interview-sd.html#q10\">Lab Q10</a>.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-sd.html",
        ),
        "33-youtube": drill_section(
            "Interview drill — Video",
            "Pipelines + CDN. Keep processing off the request path.",
            [
                qa_block(
                    qnum=1,
                    title="Design YouTube",
                    asked="Google, Netflix",
                    difficulty="Hard",
                    pattern="Transcode + CDN",
                    prompt="Upload and stream ABR video.",
                    sections=[
                        (
                            "Steps",
                            figure_diagram("youtube-cdn-pipeline", "Video pipeline")
                            + "<p><a href=\"interview-sd.html#q6\">Lab Q6</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Processing lag",
                    asked="Follow-up",
                    difficulty="Medium",
                    pattern="Priorities",
                    prompt="When is video watchable?",
                    sections=[
                        (
                            "Approach",
                            "<p>Fast-start low-res first; higher qualities later; show processing state.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Hot live event",
                    asked="Twitch/YouTube",
                    difficulty="Hard",
                    pattern="Live ingest",
                    prompt="Millions watch live.",
                    sections=[
                        (
                            "Approach",
                            "<p>Ingest → ladder → packager → CDN short TTL; regional ingest POPs.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Storage cost",
                    asked="Cost deep-dive",
                    difficulty="Medium",
                    pattern="Tiering",
                    prompt="Petabytes of old video.",
                    sections=[
                        (
                            "Approach",
                            "<p>Cold tiers; fewer bitrates for rare views; delete derivatives on takedown.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Thumbnails",
                    asked="Product",
                    difficulty="Easy",
                    pattern="Derived assets",
                    prompt="Where do thumbs fit?",
                    sections=[
                        (
                            "Approach",
                            "<p>Same pipeline; objects on CDN; A/B via metadata.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-sd.html",
        ),
        "26-queues": drill_section(
            "Interview drill — Queues",
            "Queues appear inside almost every other design.",
            [
                qa_block(
                    qnum=1,
                    title="Design a notification system",
                    asked="Amazon, Uber",
                    difficulty="Medium",
                    pattern="Priority topics",
                    prompt="Push/email/SMS with prefs.",
                    sections=[
                        (
                            "Steps",
                            figure_diagram("notification-pipeline", "Notifications")
                            + "<p><a href=\"interview-sd.html#q7\">Lab Q7</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="At-least-once vs exactly-once",
                    asked="All",
                    difficulty="Medium",
                    pattern="Semantics",
                    prompt="What can you promise?",
                    sections=[
                        (
                            "Approach",
                            "<p>Usually at-least-once + idempotent consumers. Exactly-once needs "
                            "outbox/dedupe — use when money moves.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Poison messages",
                    asked="Amazon",
                    difficulty="Medium",
                    pattern="DLQ",
                    prompt="One message crashes forever.",
                    sections=[
                        (
                            "Approach",
                            "<p>Max receive count → DLQ; alert; replay after fix.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Ordering guarantees",
                    asked="Kafka interviews",
                    difficulty="Medium",
                    pattern="Partition keys",
                    prompt="When is order preserved?",
                    sections=[
                        (
                            "Approach",
                            "<p>Per partition key only. Key = entity_id. No global order at scale.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Async vs sync boundaries",
                    asked="Meta, Amazon",
                    difficulty="Easy",
                    pattern="Judgment",
                    prompt="What must be sync in checkout?",
                    sections=[
                        (
                            "Approach",
                            "<p>Payment auth + inventory commit usually sync; email/search index async. "
                            "See also <a href=\"interview-sd.html#q10\">booking</a>.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-sd.html",
        ),
    }
