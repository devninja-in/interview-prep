#!/usr/bin/env python3
"""System design interview Q&As — classic FAANG / unicorn rounds."""
from __future__ import annotations

from interview_helpers import drill_section, qa_block


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
                "and a much higher read:write ratio."
            ),
            sections=[
                (
                    "Clarify first",
                    "<p>Custom aliases? Expiry? Analytics? Auth? Assume: 7-character base62 codes, "
                    "optional expiry, basic click counts, 100:1 read:write, 99.9% availability, "
                    "redirect latency &lt; 100ms p99.</p>",
                ),
                (
                    "Core design",
                    "<p><strong>API:</strong> <code>POST /shorten {url}</code> → code; "
                    "<code>GET /{code}</code> → 302 to long URL.</p>"
                    "<p><strong>ID generation:</strong> (1) counter + base62 encode — simple, "
                    "needs a distributed counter (Redis INCR / Snowflake); (2) hash long URL "
                    "(MD5/sha) then take prefix — handle collisions; (3) pre-generated key "
                    "pool for write bursts.</p>"
                    "<p><strong>Storage:</strong> key-value of code → {long_url, user, created, "
                    "expires}. Cassandra/DynamoDB or sharded MySQL by code hash. Cache hot "
                    "redirects in Redis with TTL.</p>"
                    "<p><strong>Redirect path:</strong> CDN/edge optional → load balancer → "
                    "app → Redis → DB. Prefer 302 (allows updating mapping) unless they ask "
                    "for browser caching with 301.</p>",
                ),
                (
                    "Deep dive topics",
                    "<ul>"
                    "<li>Capacity: 100M/mo ≈ 40 writes/s average; reads maybe thousands/s — "
                    "cache is mandatory.</li>"
                    "<li>Hot keys: viral links — replicate in cache, consider read replicas.</li>"
                    "<li>Analytics: async click events to Kafka → warehouse; do not block redirect.</li>"
                    "<li>Abuse: rate limit shorten API; malware URL scanning offline.</li>"
                    "</ul>",
                ),
                (
                    "What strong answers sound like",
                    "<p>They pick one ID scheme and defend collision handling, draw the read "
                    "path shorter than the write path, and mention why redirects must not wait "
                    "on analytics.</p>",
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
            pattern="Fan-out · timeline cache · media CDN",
            prompt=(
                "Design a photo-sharing social network: follow users, upload photos, and see a "
                "home feed of posts from people you follow, ranked roughly reverse-chronological "
                "with light ranking."
            ),
            sections=[
                (
                    "Clarify",
                    "<p>Scale: hundreds of millions of users; celebrity fan-out problem; feed "
                    "freshness vs cost; media sizes; soft deletes.</p>",
                ),
                (
                    "Core design",
                    "<p><strong>Write path:</strong> upload image → object store (S3) + CDN; "
                    "metadata in DB (post_id, author, caption, media_url, ts).</p>"
                    "<p><strong>Feed generation:</strong> "
                    "<em>Fan-out on write</em> — push post_id into each follower's timeline "
                    "cache (Redis lists) — great for normal users; "
                    "<em>Fan-out on read</em> — merge recent posts from followees at read time "
                    "— required for celebrities with millions of followers. Hybrid: fan-out "
                    "write for regulars, pull for celebs.</p>"
                    "<p><strong>Read path:</strong> auth → timeline cache → hydrate post "
                    "objects → CDN URLs for media.</p>",
                ),
                (
                    "Deep dives",
                    "<ul>"
                    "<li>Ranking: start chronological; add ML ranker later as a re-rank stage.</li>"
                    "<li>Sharding: user_id for timelines; post_id for post store.</li>"
                    "<li>Notifications &amp; stories: separate services, async via queues.</li>"
                    "<li>Consistency: feed can be eventually consistent; posting ACK after "
                    "metadata durable is enough.</li>"
                    "</ul>",
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
            pattern="WebSocket · message queue · presence",
            prompt=(
                "Design a 1:1 and group messaging system with delivery receipts, online "
                "presence, and media sharing. Focus on low latency and reliability."
            ),
            sections=[
                (
                    "Core design",
                    "<p><strong>Connections:</strong> sticky WebSocket/MQTT to chat servers; "
                    "connection service maps user_id → server instance (Redis).</p>"
                    "<p><strong>Message flow:</strong> client → chat server → durable queue/"
                    "log (Kafka) → fan-out to recipients' inbox stores → push to online sockets "
                    "or store-and-forward for offline. Persist before ACK to sender for "
                    "at-least-once; clients de-dupe by message_id.</p>"
                    "<p><strong>Group chat:</strong> small groups: fan-out to each member; "
                    "large groups: write to group inbox + notify members (or hybrid).</p>"
                    "<p><strong>Media:</strong> upload to blob store, send message with URL/"
                    "thumbnail; encrypt if E2E is in scope.</p>",
                ),
                (
                    "Hard parts interviewers probe",
                    "<ul>"
                    "<li>Ordering per conversation (per-chat sequence numbers).</li>"
                    "<li>Unread counts and last-seen (eventual OK).</li>"
                    "<li>Presence heartbeats with short TTL.</li>"
                    "<li>E2E encryption: server stores ciphertext only; key exchange on devices.</li>"
                    "</ul>",
                ),
            ],
        )
    )

    q.append(
        qa_block(
            qnum=4,
            title="Design a Rate Limiter",
            asked="Amazon, Stripe, Cloudflare, Google — often a building-block question",
            difficulty="Medium",
            pattern="Token bucket · sliding window · Redis",
            prompt=(
                "Design a distributed rate limiter used by an API gateway: e.g. 100 requests "
                "per user per minute, consistent across many gateway instances."
            ),
            sections=[
                (
                    "Algorithms to know",
                    "<ul>"
                    "<li><strong>Token bucket:</strong> tokens refill at rate r; request costs 1; "
                    "allows short bursts — industry default.</li>"
                    "<li><strong>Leaky bucket:</strong> smooths to constant outflow.</li>"
                    "<li><strong>Fixed window:</strong> simple counters; burst at window edges.</li>"
                    "<li><strong>Sliding window log / counter:</strong> fairer, more storage/CPU.</li>"
                    "</ul>",
                ),
                (
                    "Distributed design",
                    "<p>Centralize counters in Redis (INCR + EXPIRE, or Lua for token bucket "
                    "atomicity). Gateways call Redis before forwarding. For multi-region, "
                    "use regional limiters with a global budget, or accept approximate limits. "
                    "Return <code>429</code> with <code>Retry-After</code>.</p>",
                ),
                (
                    "Talking points",
                    "<p>Compare accuracy vs performance; mention race conditions without atomic "
                    "scripts; discuss per-IP vs per-API-key vs per-endpoint limits; graceful "
                    "degradation if Redis is down (fail open vs fail closed — product call).</p>",
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
            pattern="Geo index · matching · realtime location",
            prompt=(
                "Design a ride-hailing app: riders request trips, nearby drivers are matched, "
                "locations update in realtime, pricing/ETA are computed."
            ),
            sections=[
                (
                    "Core design",
                    "<p><strong>Location stream:</strong> drivers send GPS every few seconds → "
                    "location service → update geo index (geohash / S2 cells in Redis or "
                    "specialized store).</p>"
                    "<p><strong>Matching:</strong> rider request → query drivers in nearby cells "
                    "→ filter by status/vehicle → ranking (ETA, rating) → offer with timeout → "
                    "retry ring expansion.</p>"
                    "<p><strong>Trip lifecycle:</strong> state machine (requested → matched → "
                    "enroute → ongoing → completed) in a trip service; events to billing, "
                    "notifications, analytics.</p>",
                ),
                (
                    "Deep dives",
                    "<ul>"
                    "<li>ETA: map/routing service; cache road graph segments.</li>"
                    "<li>Surge pricing: demand/supply per cell, smoothed to avoid thrash.</li>"
                    "<li>Consistency: matching must avoid double-booking — optimistic lock / "
                    "atomic claim on driver.</li>"
                    "<li>Scale: shard by city/region; most traffic is local.</li>"
                    "</ul>",
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
                "Design a video upload and streaming platform: users upload videos; millions "
                "watch with adaptive quality worldwide."
            ),
            sections=[
                (
                    "Core design",
                    "<p><strong>Upload:</strong> client gets pre-signed URL → direct to blob "
                    "store; metadata row = processing.</p>"
                    "<p><strong>Processing pipeline:</strong> queue workers transcode to multiple "
                    "resolutions/codecs, generate thumbnails, extract duration; store HLS/DASH "
                    "segments; mark ready.</p>"
                    "<p><strong>Playback:</strong> client fetches manifest; CDN serves segments; "
                    "origin is object store. Adaptive bitrate based on bandwidth.</p>",
                ),
                (
                    "Deep dives",
                    "<ul>"
                    "<li>Hot videos: heavy CDN caching; popular titles at edge.</li>"
                    "<li>Recommendations: offline ML + online re-rank (separate from serving path).</li>"
                    "<li>Copyright / abuse: async fingerprinting and review queues.</li>"
                    "<li>Cost: storage tiers, cold archive for old rarely watched content.</li>"
                    "</ul>",
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
            pattern="Fan-out · priority queues · templates",
            prompt=(
                "Design a multi-channel notification platform: push, email, SMS, in-app, with "
                "user preferences, retries, and high throughput."
            ),
            sections=[
                (
                    "Core design",
                    "<p>Producer APIs enqueue notification jobs → Kafka topics by priority/"
                    "channel → workers render templates → provider adapters (APNs/FCM, SES, "
                    "Twilio) → delivery receipts back for status.</p>"
                    "<p>Preferences service gates channel/quiet hours. Deduplicate with "
                    "idempotency keys. Rate-limit per user and per provider.</p>",
                ),
                (
                    "Failure modes",
                    "<p>Provider outages → exponential backoff + DLQ. Partial fan-out for "
                    "large audiences (celebrity posts) via chunked tasks. Exactly-once is "
                    "unrealistic — aim for at-least-once + idempotent display.</p>",
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
                "Design search autocomplete that returns top suggestions as the user types, "
                "with low latency and trending awareness."
            ),
            sections=[
                (
                    "Core design",
                    "<p>Offline: aggregate query logs → compute top-k per prefix → build trie "
                    "or prefix index; ship snapshots to servers / edge.</p>"
                    "<p>Online: client debounces; request prefix → memory trie returns top-k "
                    "(&lt;50ms). Personalization and trending as a light re-rank layer. Cache "
                    "popular prefixes at CDN/edge.</p>",
                ),
                (
                    "Scale tricks",
                    "<p>Limit prefix length; store only top-k not full postings; AJAX results "
                    "tiny; update index periodically (minutes) not per keystroke. For "
                    "distributed tries, shard by first character(s).</p>",
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
                "Design a distributed in-memory cache used by many microservices: get/put/"
                "delete, TTL, high availability, horizontal scale."
            ),
            sections=[
                (
                    "Core design",
                    "<p>Client or proxy uses consistent hashing to pick a shard. Each shard "
                    "is a primary + replicas (async or semi-sync). LRU/LFU/TTL eviction "
                    "per node. Gossip or config service for membership.</p>",
                ),
                (
                    "Deep dives",
                    "<ul>"
                    "<li>Hot keys: replicate popular keys to many nodes or add local caches.</li>"
                    "<li>Thundering herd: soft TTL + singleflight refresh.</li>"
                    "<li>Persistence optional (AOF/RDB) — usually cache is ephemeral.</li>"
                    "<li>CAP: prefer AP for cache; clients tolerate miss and load DB.</li>"
                    "</ul>",
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
            pattern="Inventory locks · idempotency · flash sales",
            prompt=(
                "Design a ticketing system for concerts: browse events, hold seats, pay, and "
                "issue tickets — without double-selling under huge spikes."
            ),
            sections=[
                (
                    "Core design",
                    "<p><strong>Inventory:</strong> seat map per event/section; state "
                    "available → held → sold. Hold = soft lock with short TTL (2–10 min) in "
                    "Redis or row-level locks.</p>"
                    "<p><strong>Checkout:</strong> create hold → payment intent → on success "
                    "commit seats + generate ticket IDs; on fail/expiry release hold. "
                    "Idempotency keys on payment webhooks.</p>"
                    "<p><strong>Scale:</strong> shard by event_id; queue waiting rooms for "
                    "mega-events; read replicas for browse; CDN for static event pages.</p>",
                ),
                (
                    "Consistency",
                    "<p>This is one design where strong consistency on inventory matters. "
                    "Use conditional updates (COMPARE_AND_SET / SQL WHERE status='available'). "
                    "Never trust client-side seat claims alone.</p>",
                ),
            ],
        )
    )

    return q


def sd_lab_body() -> str:
    intro = """<p>These are the system-design prompts that appear again and again in L4–L6 loops:
URL shortener as a warmup, then chat, feed, rides, video, or a focused building block like
rate limiting. Each card mirrors how a strong 45-minute whiteboard session should unfold —
clarify, propose API + data model, draw the path, then deep-dive.</p>
<p class="drill-intro">Structure every answer: requirements → capacity sketch → API → high-level
diagram → data model → deep dives → failures. Interviewers interrupt; practice recovering.</p>
"""
    return intro + "\n".join(sd_questions())


def sd_chapter_drills() -> dict[str, str]:
    return {
        "28-url-shortener": drill_section(
            "Interview drill",
            "If you only practice one design end-to-end, make it this.",
            [
                qa_block(
                    qnum=1,
                    title="Design Bitly",
                    asked="Amazon, Google, Microsoft",
                    difficulty="Medium",
                    pattern="KV store + cache",
                    prompt="Shorten URLs and redirect with analytics.",
                    sections=[
                        (
                            "Approach",
                            "<p>Base62 IDs, KV mapping, Redis on read path, async clicks. "
                            "Full walkthrough: <a href=\"interview-sd.html\">System Design Lab Q1</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Custom aliases &amp; collisions",
                    asked="Follow-up at Google/Amazon",
                    difficulty="Medium",
                    pattern="Uniqueness constraints",
                    prompt="How do you support user-chosen short codes safely?",
                    sections=[
                        (
                            "Approach",
                            "<p>Reserve alias with conditional put; reject if taken; rate-limit "
                            "alias creation; validate charset length; scan for phishing patterns.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="301 vs 302",
                    asked="Common redirect follow-up",
                    difficulty="Easy",
                    pattern="HTTP caching semantics",
                    prompt="Which status code for redirects and why?",
                    sections=[
                        (
                            "Approach",
                            "<p>302/307 keep control (mapping can change, analytics stay server-side). "
                            "301 caches in browsers — faster but harder to update or count.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Global latency",
                    asked="Microsoft, Amazon",
                    difficulty="Medium",
                    pattern="Multi-region + CDN",
                    prompt="Users worldwide need fast redirects.",
                    sections=[
                        (
                            "Approach",
                            "<p>Replicate read-only mappings regionally; edge cache hot codes; "
                            "writes to primary region with async replication.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Predictable IDs / enumeration",
                    asked="Security follow-up",
                    difficulty="Medium",
                    pattern="Security",
                    prompt="Sequential IDs leak creation volume — what do you do?",
                    sections=[
                        (
                            "Approach",
                            "<p>Use salted hashes, skip-count counters, or encrypted IDs; "
                            "rate-limit guessing; do not expose autoincrement publicly.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-sd.html",
        ),
        "29-whatsapp": drill_section(
            "Interview drill",
            "Chat designs hinge on connections, durability, and fan-out — not UI.",
            [
                qa_block(
                    qnum=1,
                    title="Design WhatsApp",
                    asked="Meta, WhatsApp",
                    difficulty="Hard",
                    pattern="WebSocket + inbox",
                    prompt="1:1 and group messaging with receipts.",
                    sections=[
                        (
                            "Approach",
                            "<p>Sticky sockets, durable log, per-user inbox, offline store-and-forward. "
                            "<a href=\"interview-sd.html\">Lab Q3</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Read receipts at scale",
                    asked="Follow-up",
                    difficulty="Medium",
                    pattern="Async events",
                    prompt="How do blue ticks work without melting the DB?",
                    sections=[
                        (
                            "Approach",
                            "<p>Receipts are separate lightweight events; batch writes; eventual "
                            "consistency OK; do not block message delivery on receipt fan-out.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Large group chats",
                    asked="Discord / Slack style follow-up",
                    difficulty="Hard",
                    pattern="Fan-out strategies",
                    prompt="10k-member group — fan-out on write or read?",
                    sections=[
                        (
                            "Approach",
                            "<p>Write to group log; members pull/catch up; push notify only online "
                            "subscribers. Pure write fan-out explodes.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="End-to-end encryption",
                    asked="Signal/WhatsApp rounds",
                    difficulty="Hard",
                    pattern="E2E keys",
                    prompt="Where do keys live and what does the server store?",
                    sections=[
                        (
                            "Approach",
                            "<p>Server stores ciphertext + metadata; identity/prekeys on devices; "
                            "server cannot read bodies — acknowledge tradeoffs for search/features.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Message ordering",
                    asked="Meta",
                    difficulty="Medium",
                    pattern="Per-conversation seq",
                    prompt="How do you order messages in a chat?",
                    sections=[
                        (
                            "Approach",
                            "<p>Per-chat monotonic sequence from a single writer partition; "
                            "clients sort by seq; vector clocks only if multi-device concurrent edits matter.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-sd.html",
        ),
        "30-instagram": drill_section(
            "Interview drill",
            "Feeds are a fan-out problem dressed as a product question.",
            [
                qa_block(
                    qnum=1,
                    title="Design Instagram feed",
                    asked="Meta",
                    difficulty="Hard",
                    pattern="Hybrid fan-out",
                    prompt="Home feed for follows + media.",
                    sections=[
                        (
                            "Approach",
                            "<p>Fan-out on write for normals, pull for celebs; CDN for media. "
                            "<a href=\"interview-sd.html\">Lab Q2</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Celebrity problem",
                    asked="Twitter/Meta",
                    difficulty="Hard",
                    pattern="Fan-out on read",
                    prompt="User with 50M followers posts — what breaks?",
                    sections=[
                        (
                            "Approach",
                            "<p>Do not push to 50M timelines. Store post; mix into followers' "
                            "feeds at read/merge time; precompute for active users only if needed.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Feed ranking",
                    asked="Meta",
                    difficulty="Medium",
                    pattern="Retrieval + ranker",
                    prompt="Not purely chronological — how?",
                    sections=[
                        (
                            "Approach",
                            "<p>Candidate retrieval from follow graph / timeline cache → feature "
                            "join → lightweight ranker → diversity rules. Keep ranking async-friendly.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Counter service",
                    asked="Instagram classic",
                    difficulty="Medium",
                    pattern="Sharded counters",
                    prompt="Likes and view counts at huge QPS.",
                    sections=[
                        (
                            "Approach",
                            "<p>Sharded in-memory counters with periodic flush; accept approximate "
                            "display counts; exact counts via batch reconciliation.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Stories vs feed",
                    asked="Meta",
                    difficulty="Medium",
                    pattern="TTL data",
                    prompt="Ephemeral stories architecture?",
                    sections=[
                        (
                            "Approach",
                            "<p>Separate store with 24h TTL; ring/view fan-out smaller; media still "
                            "on CDN/blob with lifecycle policies.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-sd.html",
        ),
        "34-uber": drill_section(
            "Interview drill",
            "Geo + matching + state machines — keep the diagram regional.",
            [
                qa_block(
                    qnum=1,
                    title="Design Uber",
                    asked="Uber, Lyft",
                    difficulty="Hard",
                    pattern="Geo index + matching",
                    prompt="Match riders to nearby drivers in realtime.",
                    sections=[
                        (
                            "Approach",
                            "<p>Geohash location updates; ring matching; trip state machine. "
                            "<a href=\"interview-sd.html\">Lab Q5</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Avoid double dispatch",
                    asked="Uber",
                    difficulty="Hard",
                    pattern="Atomic claim",
                    prompt="Two riders matched to the same driver?",
                    sections=[
                        (
                            "Approach",
                            "<p>Driver status CAS to 'offered/busy'; offer lease with timeout; "
                            "only one claim wins.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="ETA accuracy",
                    asked="Follow-up",
                    difficulty="Medium",
                    pattern="Routing service",
                    prompt="How is ETA computed?",
                    sections=[
                        (
                            "Approach",
                            "<p>Map-matching GPS to roads; routing over traffic-aware graph; "
                            "cache segments; update with live speeds.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Surge pricing",
                    asked="Uber",
                    difficulty="Medium",
                    pattern="Demand/supply per cell",
                    prompt="Design surge without wild oscillation.",
                    sections=[
                        (
                            "Approach",
                            "<p>Compute per-geocell imbalance on a short window; smooth with "
                            "EMA; cap rate of change; show multiplier before confirm.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="City sharding",
                    asked="Scale follow-up",
                    difficulty="Medium",
                    pattern="Regional deployment",
                    prompt="How do you shard the system?",
                    sections=[
                        (
                            "Approach",
                            "<p>Most state is city-local — shard services and data by region/city; "
                            "global for identity/billing only.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-sd.html",
        ),
        "22-caching": drill_section(
            "Interview drill",
            "Caching questions separate people who have operated systems from people who memorized buzzwords.",
            [
                qa_block(
                    qnum=1,
                    title="Design a distributed cache",
                    asked="Amazon, Microsoft",
                    difficulty="Hard",
                    pattern="Consistent hashing",
                    prompt="Build Redis-like get/put across nodes.",
                    sections=[
                        (
                            "Approach",
                            "<p>Consistent hash ring, replicas, LRU/TTL. "
                            "<a href=\"interview-sd.html\">Lab Q9</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Cache stampede",
                    asked="Amazon",
                    difficulty="Medium",
                    pattern="Singleflight / soft TTL",
                    prompt="Hot key expires — thousands hit DB.",
                    sections=[
                        (
                            "Approach",
                            "<p>Soft TTL with background refresh; request coalescing; probabilistic "
                            "early expiration.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Write strategies",
                    asked="Microsoft",
                    difficulty="Medium",
                    pattern="Write-through / behind / around",
                    prompt="When do you write the cache vs DB first?",
                    sections=[
                        (
                            "Approach",
                            "<p>Write-through for strong freshness; write-behind for write throughput "
                            "(risk); write-around for write-heavy rarely-read data. Invalidate on write "
                            "is the common microservice pattern.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="CDN vs app cache",
                    asked="All companies",
                    difficulty="Easy",
                    pattern="Edge vs origin",
                    prompt="What belongs on a CDN?",
                    sections=[
                        (
                            "Approach",
                            "<p>Static &amp; cacheable HTTP responses near users. Personalized or "
                            "auth-sensitive data stays in app/Redis closer to origin logic.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Rate limiter with Redis",
                    asked="Stripe, Amazon",
                    difficulty="Medium",
                    pattern="Token bucket",
                    prompt="Enforce per-API-key limits across gateways.",
                    sections=[
                        (
                            "Approach",
                            "<p>Atomic Redis Lua token bucket; 429 + Retry-After. "
                            "<a href=\"interview-sd.html\">Lab Q4</a>.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-sd.html",
        ),
        "21-scaling": drill_section(
            "Interview drill",
            "Scaling rounds test whether you can move from one box to a fleet thoughtfully.",
            [
                qa_block(
                    qnum=1,
                    title="Horizontal scale a read-heavy API",
                    asked="Amazon, Google",
                    difficulty="Medium",
                    pattern="LB + replicas + cache",
                    prompt="Traffic grew 20× — what do you change first?",
                    sections=[
                        (
                            "Approach",
                            "<p>Measure bottleneck; add LB + stateless app replicas; read replicas "
                            "or cache; only then shard. Order matters.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Load balancer choice",
                    asked="Amazon",
                    difficulty="Medium",
                    pattern="L4 vs L7",
                    prompt="When L4 vs L7? Sticky sessions?",
                    sections=[
                        (
                            "Approach",
                            "<p>L4 for raw TCP/WS scale; L7 for path-based routing and auth at edge. "
                            "Prefer external session store over sticky when possible.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Graceful degradation",
                    asked="Netflix-style",
                    difficulty="Medium",
                    pattern="Feature flags / fallbacks",
                    prompt="Dependency is down — what does the user see?",
                    sections=[
                        (
                            "Approach",
                            "<p>Timeouts, circuit breakers, cached fallbacks, disable non-critical "
                            "widgets. Explicit SLO per dependency.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Backpressure",
                    asked="Google, Uber",
                    difficulty="Medium",
                    pattern="Queues + load shedding",
                    prompt="Producers outrun consumers.",
                    sections=[
                        (
                            "Approach",
                            "<p>Bounded queues, 503/retry-after, drop low-priority work, autoscale "
                            "consumers, rate-limit producers.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Idempotent APIs",
                    asked="Stripe, Amazon",
                    difficulty="Medium",
                    pattern="Idempotency keys",
                    prompt="Clients retry — how do you not double-charge?",
                    sections=[
                        (
                            "Approach",
                            "<p>Client idempotency key stored with request hash/result; replays "
                            "return the first result.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-sd.html",
        ),
        "33-youtube": drill_section(
            "Interview drill",
            "Video designs are pipelines plus CDN — keep processing off the request path.",
            [
                qa_block(
                    qnum=1,
                    title="Design YouTube",
                    asked="Google, Netflix",
                    difficulty="Hard",
                    pattern="Transcode + CDN",
                    prompt="Upload and stream adaptive video worldwide.",
                    sections=[
                        (
                            "Approach",
                            "<p>Direct upload to blob; async transcode to HLS/DASH; CDN playback. "
                            "<a href=\"interview-sd.html\">Lab Q6</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Processing lag",
                    asked="Follow-up",
                    difficulty="Medium",
                    pattern="Queue priorities",
                    prompt="User uploads — when is video watchable?",
                    sections=[
                        (
                            "Approach",
                            "<p>Fast-start low-res rendition first; higher qualities land later; "
                            "show processing state in UI.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Hot live event",
                    asked="Twitch/YouTube",
                    difficulty="Hard",
                    pattern="Live ingest + edge",
                    prompt="Millions watch a live stream.",
                    sections=[
                        (
                            "Approach",
                            "<p>Ingest → transcode ladder → packager → CDN with short segment "
                            "TTL; separate from VOD pipeline; regional ingest POPs.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Storage cost control",
                    asked="Cost deep-dive",
                    difficulty="Medium",
                    pattern="Tiering",
                    prompt="Petabytes of old video.",
                    sections=[
                        (
                            "Approach",
                            "<p>Lifecycle to colder storage; fewer bitrates for rarely watched; "
                            "dedupe; delete derivatives on takedown.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Thumbnails &amp; previews",
                    asked="Product follow-up",
                    difficulty="Easy",
                    pattern="Derived assets",
                    prompt="Where do thumbnails fit?",
                    sections=[
                        (
                            "Approach",
                            "<p>Generated in the same pipeline; stored as objects; heavily CDN "
                            "cached; can A/B multiple thumbs via metadata.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-sd.html",
        ),
        "26-queues": drill_section(
            "Interview drill",
            "Queues show up inside almost every other design — master the vocabulary.",
            [
                qa_block(
                    qnum=1,
                    title="Design a notification system",
                    asked="Amazon, Uber",
                    difficulty="Medium",
                    pattern="Priority topics + workers",
                    prompt="Push/email/SMS with preferences and retries.",
                    sections=[
                        (
                            "Approach",
                            "<p>Kafka by priority/channel; template workers; provider adapters; DLQ. "
                            "<a href=\"interview-sd.html\">Lab Q7</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="At-least-once vs exactly-once",
                    asked="All companies",
                    difficulty="Medium",
                    pattern="Delivery semantics",
                    prompt="What can you actually promise?",
                    sections=[
                        (
                            "Approach",
                            "<p>Most systems: at-least-once + idempotent consumers. Exactly-once "
                            "needs transactional outbox / dedupe store — costly; use when money moves.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Poison messages",
                    asked="Amazon",
                    difficulty="Medium",
                    pattern="DLQ",
                    prompt="A message crashes consumers forever.",
                    sections=[
                        (
                            "Approach",
                            "<p>Max receive count → dead-letter queue; alert; replay after fix; "
                            "never block the partition on one bad payload.</p>",
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
                            "<p>Per partition key only. Choose key = entity_id (user/order). "
                            "Global order does not scale — do not promise it.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Async vs sync boundaries",
                    asked="Meta, Amazon",
                    difficulty="Easy",
                    pattern="Product judgment",
                    prompt="What must be synchronous in checkout?",
                    sections=[
                        (
                            "Approach",
                            "<p>Payment authorization and inventory commit usually sync; email, "
                            "recommendations, search indexing async.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-sd.html",
        ),
    }
