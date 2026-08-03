#!/usr/bin/env python3
"""Interview-lens enrichment for every lab question (why / levels / mistakes / production)."""
from __future__ import annotations

# lab_id -> qnum -> enrichment dict
# Fields: why, evaluating[], levels{}, expected, followups[], mistakes[], production[], reading_mins

def _L(junior="", mid="", senior="", staff="", principal=""):
    d = {}
    if junior:
        d["Junior"] = junior
    if mid:
        d["Mid"] = mid
    if senior:
        d["Senior"] = senior
    if staff:
        d["Staff"] = staff
    if principal:
        d["Principal"] = principal
    return d


ENRICHMENT: dict[str, dict[int, dict]] = {
    "cp": {},
    "sd": {},
    "ai": {},
}


def _cp(n, **kwargs):
    ENRICHMENT["cp"][n] = kwargs


def _sd(n, **kwargs):
    ENRICHMENT["sd"][n] = kwargs


def _ai(n, **kwargs):
    ENRICHMENT["ai"][n] = kwargs


# ---- Coding (1–20) ----
_cp(
    1,
    why="Warmup that reveals whether you reach for hash maps instinctively instead of nested loops.",
    evaluating=["Clarify indices vs values", "Brute → optimal narrative", "Self-pair edge case", "Complexity"],
    levels=_L(
        "Working O(n) map solution",
        "Clean code + edge cases + follow-ups",
        "Discuss streaming / multi-pair variants",
        "API design if generalized to k-sum service",
        "Rarely asked; expect teaching clarity",
    ),
    expected="State O(n²) → complement map → code → complexity → one follow-up.",
    followups=["Return all pairs?", "Sorted array variant?", "Memory-constrained stream?"],
    mistakes=["Store before check (self-pair)", "Return values not indices", "List.contains → O(n²)"],
    production=["Ad targeting join keys", "Deduping request IDs in gateways", "Amazon cart coupon matching patterns"],
    reading_mins=8,
)
_cp(
    2,
    why="Tests sliding-window fluency — Meta/Amazon medium staple.",
    evaluating=["Window invariant", "Last-seen index correctness", "Empty/all-unique edges"],
    levels=_L("Correct O(n) window", "Articulate invariant", "Variant: at most k distinct", "Optimize for unicode/streams", ""),
    expected="Define duplicate-free window → expand/shrink rule → code → traps.",
    followups=["Longest with at most k distinct?", "Minimum window covering t?"],
    mistakes=["Moving left without last[ch] >= left check", "Off-by-one length"],
    production=["Session uniqueness checks", "Log tokenization windows", "Rate windows in analytics"],
    reading_mins=10,
)
_cp(
    3,
    why="Scheduling/calendar signal — sort + linear merge is the expected pattern.",
    evaluating=["Sort justification", "Overlap definition", "Touching intervals"],
    levels=_L("Correct merge", "Meeting Rooms II link", "Online insert into merged list", "Calendar product constraints", ""),
    expected="Sort by start → single pass merge → complexity → rooms follow-up.",
    followups=["Insert interval?", "Min rooms?", "Min removals?"],
    mistakes=["Forgetting sort", "Using < instead of ≤ for touching"],
    production=["Google Calendar free/busy", "AWS capacity reservation windows", "Ad flight dates"],
    reading_mins=10,
)
_cp(
    4,
    why="Highest cross-company design+code question — composition under O(1) constraints.",
    evaluating=["Why map+DLL", "Draw structure", "Update vs insert", "Capacity-1"],
    levels=_L("OrderedDict OK if explained", "Hand-rolled DLL", "Thread-safety discussion", "Distributed LRU / cache tiering", "Multi-tier cache policy design"),
    expected="Explain structures → helpers → get/put → eviction → complexity.",
    followups=["LFU?", "TTL?", "Concurrent access?"],
    mistakes=["O(n) scan for LRU", "Forgetting update refreshes recency"],
    production=["Redis approximate LRU", "CDN edge caches", "CPU page cache intuition"],
    reading_mins=15,
)
_cp(
    5,
    why="Grid DFS/BFS literacy — Amazon/Google classic.",
    evaluating=["Component counting", "Visited discipline", "4 vs 8 connectivity"],
    levels=_L("DFS flood fill", "BFS + recursion limits", "Variants (max area)", "Union-find framing", ""),
    expected="Scan → flood → count → complexity → one variant.",
    followups=["Max area?", "Closed islands?", "Pacific Atlantic?"],
    mistakes=["Diagonal connections", "Not marking visited"],
    production=["Map region labeling", "Image connected components", "Game fog-of-war floods"],
    reading_mins=10,
)
_cp(
    6,
    why="Cycle detection / topo sort — dependency systems.",
    evaluating=["Graph model", "Kahn vs DFS colors", "Order vs boolean"],
    levels=_L("canFinish correct", "Return order (II)", "Parallel semesters", "Build systems analogy", ""),
    expected="Edges b→a → indegree Kahn → compare count to n.",
    followups=["Course Schedule II?", "Minimum semesters?"],
    mistakes=["Wrong edge direction", "Forgetting nodes with no edges"],
    production=["CI pipeline deps", "Package managers", "Airflow/DAG schedulers"],
    reading_mins=12,
)
_cp(
    7,
    why="Unbounded knapsack DP — distinguishes DP from greedy.",
    evaluating=["State definition", "Why greedy fails", "Bottom-up loops"],
    levels=_L("dp[] works", "Explain counterexample", "Coin Change II contrast", "Memory optimize", ""),
    expected="dp[x] definition → transition → code → greedy trap.",
    followups=["Number of combinations?", "Limited coin counts?"],
    mistakes=["Confusing with Coin Change II", "Assuming US coins greedy"],
    production=["Change-making POS", "Resource allocation DP", "Game economy crafting"],
    reading_mins=12,
)
_cp(
    8,
    why="BFS shortest path in an implicit graph — Google classic.",
    evaluating=["Model as graph", "Neighbor generation", "Visited discipline"],
    levels=_L("BFS correct", "Wildcard buckets optimize", "Bidirectional BFS", "Production dictionary scale", ""),
    expected="Words as nodes → BFS → remove on enqueue → complexity.",
    followups=["Return the path?", "Bidirectional BFS?"],
    mistakes=["DFS (not shortest)", "Not removing visited words"],
    production=["Typo correction graphs", "Chemical edit distance search", "Knowledge graph hops"],
    reading_mins=14,
)
_cp(
    9,
    why="Encoding/decoding + tree fluency — Meta favorite.",
    evaluating=["Invertible format", "Null markers", "Empty tree"],
    levels=_L("BFS serialize works", "Preorder alternative", "Compact encodings", "Schema evolution talk", ""),
    expected="Choose format → serialize → deserialize → edge cases.",
    followups=["BST serialize without nulls?", "Compress?"],
    mistakes=["Losing null structure", "Delimiter bugs"],
    production=["Protobuf-like tree payloads", "UI component trees", "AST persistence"],
    reading_mins=14,
)
_cp(
    10,
    why="Hard two-pointer / geometry reasoning under pressure.",
    evaluating=["Water formula", "Two-pointer justification", "O(1) space"],
    levels=_L("Prefix arrays OK", "Two pointers", "Monotonic stack", "Generalize to 2D", ""),
    expected="min(left_max,right_max)-h → two pointers → O(1).",
    followups=["Return trapped indices?", "Histogram largest rectangle?"],
    mistakes=["Wrong bound when advancing pointers"],
    production=["Hydrology sims", "Capacity planning metaphors", "Image pooling analogies"],
    reading_mins=12,
)
_cp(
    11,
    why="One-pass scan with running state — easiest DP gateway.",
    evaluating=["Single transaction constraint", "All decreasing → 0"],
    levels=_L("Correct one pass", "Relate to Kadane", "Multi-transaction variants", "Online trading constraints", ""),
    expected="Track min → max profit → variants.",
    followups=["Unlimited transactions?", "Cooldown + cooldown?"],
    mistakes=["Allowing sell before buy"],
    production=["Simple PnL calculators", "Promo best-discount windows"],
    reading_mins=6,
)
_cp(
    12,
    why="Hard window with counts — Meta speed round staple.",
    evaluating=["need/have counters", "Minimal window shrink", "Duplicates in t"],
    levels=_L("Correct window", "O(1) validation", "Unicode / streaming", "Library API design", ""),
    expected="need map → expand → shrink while valid → best.",
    followups=["Permutation in string?", "Find all anagram starts?"],
    mistakes=["O(|t|) scans inside while"],
    production=["Log field extractors", "DNA motif covering", "Search snippet covering queries"],
    reading_mins=15,
)
_cp(
    13,
    why="Kadane — Amazon OA classic for array DP.",
    evaluating=["Extend vs restart", "All-negative arrays"],
    levels=_L("Kadane code", "Return indices", "2D maximal rectangle", "Streaming version", ""),
    expected="best_ending transition → global max.",
    followups=["Circular max?", "Return subarray bounds?"],
    mistakes=["Resetting to 0 on all-negative"],
    production=["Max streak metrics", "Signal processing windows"],
    reading_mins=8,
)
_cp(
    14,
    why="Binary search with a twist — Meta/Amazon favorite.",
    evaluating=["Identify sorted half", "Invariant", "Duplicates follow-up"],
    levels=_L("Distinct rotated search", "With duplicates", "Find min in rotated", "General rotated structures", ""),
    expected="Draw array → sorted-half test → code.",
    followups=["Find minimum?", "Duplicates allowed?"],
    mistakes=["Searching unsorted half"],
    production=["Rotated ring buffers", "Time-wrapped schedules"],
    reading_mins=12,
)
_cp(
    15,
    why="Heap vs bucket tradeoff — universal medium.",
    evaluating=["Count then select", "O(n log k) vs O(n)", "Stability not required"],
    levels=_L("Heap solution", "Bucket sort", "Quickselect talk", "Distributed top-k", ""),
    expected="Counter → heap or buckets → return k.",
    followups=["Top-k by other metrics?", "Approximate top-k?"],
    mistakes=["Full sort only"],
    production=["Trending topics", "Error-code dashboards", "Search query popularity"],
    reading_mins=10,
)
_cp(
    16,
    why="Interval + heap — Meta premium classic.",
    evaluating=["Sort by start", "Reuse rule", "Peak rooms"],
    levels=_L("Heap solution", "Sweep line", "Online bookings", "Resource packing product", ""),
    expected="Sort → min-heap ends → len(heap).",
    followups=["Merge intervals link?", "Max concurrent online?"],
    mistakes=["Sorting by end first incorrectly"],
    production=["Meeting room products", "Cloud VM concurrent capacity", "Call-center staffing"],
    reading_mins=10,
)
_cp(
    17,
    why="Stack literacy warmup across companies.",
    evaluating=["Push/pop matching", "Empty stack rules"],
    levels=_L("Correct validator", "Min remove to valid", "Generate parentheses", "Parser talk", ""),
    expected="Stack openings → match closings → empty at end.",
    followups=["Longest valid?", "Min add/remove?"],
    mistakes=["Not checking type match"],
    production=["IDE bracket matchers", "Config/JSON validators", "Template engines"],
    reading_mins=6,
)
_cp(
    18,
    why="Multi-source BFS — Amazon graph/grid favorite.",
    evaluating=["Queue all sources", "Level = time", "Impossible case"],
    levels=_L("BFS correct", "In-place mutation", "0-1 BFS variants", "Epidemic models", ""),
    expected="Enqueue all rotten → level BFS → fresh left?",
    followups=["Walls and gates?", "Shortest path in grid?"],
    mistakes=["Single-source BFS only"],
    production=["Content freshness propagation", "Infection/simulation jobs", "Warehouse spill models"],
    reading_mins=12,
)
_cp(
    19,
    why="Build graph from constraints — Meta/Google hard closer.",
    evaluating=["Edge from consecutive words", "Invalid prefix case", "Cycle → empty"],
    levels=_L("Build edges + Kahn", "All invalid cases", "Unique vs any order", "Grammar induction talk", ""),
    expected="Compare pairs → edges → topo → cycle check.",
    followups=["Multiple valid orders?", "Verify order against words?"],
    mistakes=["Comparing non-consecutive words only"],
    production=["Locale collation debugging", "Build order from logs", "Schema evolution ordering"],
    reading_mins=15,
)
_cp(
    20,
    why="Selection algorithms — heap vs quickselect signal.",
    evaluating=["kth largest vs smallest", "Heap size k", "Average O(n) option"],
    levels=_L("Heap", "Quickselect", "Worst-case linear", "Distributed quantile", ""),
    expected="Clarify kth largest → heap or quickselect → complexity.",
    followups=["K closest points?", "Running median?"],
    mistakes=["Off-by-one k"],
    production=["Latency percentile approx", "Leaderboard cutoffs", "Priority aging"],
    reading_mins=8,
)

# ---- System design (1–18) ----
_sd(
    1,
    why="Perfect first SD question: read-heavy KV, ID generation, caching.",
    evaluating=["Clarify + capacity", "ID scheme", "Read vs write path", "Analytics async"],
    levels=_L(
        "Basic API + DB + redirect",
        "Cache + base62 + 302 vs 301",
        "Multi-region + abuse",
        "Global edge + consistency story",
        "Platform constraints / multi-tenant shorteners",
    ),
    expected="Clarify → nums → API → ID → KV+cache → deep dive.",
    followups=["Custom aliases?", "Enumerate IDs?", "Global latency?"],
    mistakes=["Blocking redirect on analytics", "No collision story"],
    production=["bit.ly / t.co style redirects", "Amazon product short links", "Firebase Dynamic Links patterns"],
    reading_mins=20,
)
_sd(
    2,
    why="Tests fan-out tradeoffs — Meta’s signature problem.",
    evaluating=["Celebrity problem", "Hybrid fan-out", "Media CDN", "Eventual consistency"],
    levels=_L("Chronological pull", "Push fan-out", "Hybrid + ranking stage", "ML ranker + diversity", "Feed platform multi-surface"),
    expected="Upload → fan-out strategy → read path → celebrity → ranking.",
    followups=["Stories?", "Live counters?", "Unfollow consistency?"],
    mistakes=["Push to 50M followers", "No CDN for media"],
    production=["Instagram/FB feed", "LinkedIn feed fanout", "Twitter/X home timeline"],
    reading_mins=25,
)
_sd(
    3,
    why="Realtime systems, durability, fan-out — Meta/Slack loops.",
    evaluating=["WS/sticky", "Persist before ACK", "Group strategy", "Presence"],
    levels=_L("1:1 WS + DB", "Offline store-and-forward", "Large groups + E2E talk", "Multi-device sync", "Global chat fabric"),
    expected="Connections → durable log → inbox → push/offline → groups.",
    followups=["E2E encryption?", "Read receipts scale?", "Message edit/delete?"],
    mistakes=["No durability before ACK", "Fan-out write to huge groups"],
    production=["WhatsApp", "Slack channels", "Discord large guilds patterns"],
    reading_mins=25,
)
_sd(
    4,
    why="Building block that appears inside every API design.",
    evaluating=["Algorithm choice", "Atomic Redis", "Fail open/closed", "Dimensions"],
    levels=_L("Fixed window", "Token bucket + Redis", "Multi-region approx", "Adaptive limits", "Mesh-wide policy engine"),
    expected="Pick algorithm → distributed store → 429 → failure mode.",
    followups=["Per-user vs per-IP?", "Burst vs smooth?", "Redis down?"],
    mistakes=["Non-atomic INCR races", "Only local in-memory limits"],
    production=["AWS API Gateway", "Cloudflare rate limiting", "Stripe API limits"],
    reading_mins=15,
)
_sd(
    5,
    why="Geo + matching + state machines — Uber/Lyft signature.",
    evaluating=["Geo index", "Double-dispatch", "Trip FSM", "City sharding"],
    levels=_L("Basic nearby query", "Ring matching + ETA", "Surge + CAS claim", "Multi-product dispatch", "Marketplace optimization"),
    expected="GPS stream → geo index → match → claim → trip events.",
    followups=["Surge?", "ETA accuracy?", "Airport queues?"],
    mistakes=["Global single DB", "No atomic driver claim"],
    production=["Uber/Lyft dispatch", "DoorDash courier matching", "Gojek regional stacks"],
    reading_mins=25,
)
_sd(
    6,
    why="Pipeline + CDN — Google/Netflix media systems.",
    evaluating=["Async transcode", "ABR", "CDN hot path", "Cost/tiering"],
    levels=_L("Upload + single bitrate", "Ladder + CDN", "Live vs VOD", "Global POP ingest", "Encoding marketplace"),
    expected="Upload blob → queue encode → HLS/DASH → CDN play.",
    followups=["Viral cold cache?", "DRM?", "Thumbnails A/B?"],
    mistakes=["Transcode on request path"],
    production=["YouTube", "Netflix encoding + Open Connect", "Twitch live ladder"],
    reading_mins=25,
)
_sd(
    7,
    why="Async fan-out with preferences — almost every company.",
    evaluating=["Channels", "Prefs", "Retries/DLQ", "Idempotency"],
    levels=_L("Single channel worker", "Multi-channel + prefs", "Priority + chunking", "Global quiet hours/compliance", "Notification platform"),
    expected="Enqueue → gate prefs → workers → providers → DLQ.",
    followups=["Exactly-once?", "Celebrity fan-out?", "Digest bundling?"],
    mistakes=["Sync send on request path"],
    production=["Amazon SES+SNS", "Uber notifications", "LinkedIn notification service"],
    reading_mins=18,
)
_sd(
    8,
    why="Prefix systems + offline top-k — Google classic.",
    evaluating=["Trie/top-k", "Offline vs online", "Edge cache", "Personalization light touch"],
    levels=_L("In-memory trie", "Snapshots + CDN", "Trending re-rank", "Personalization + spell", "Multi-locale platform"),
    expected="Offline top-k → trie → debounce → cache.",
    followups=["Personalization?", "Typo tolerance?", "Abuse?"],
    mistakes=["Query DB per keystroke"],
    production=["Google Suggest", "Amazon search box", "Twitter typeahead"],
    reading_mins=15,
)
_sd(
    9,
    why="Distributed systems fundamentals — Amazon/Microsoft.",
    evaluating=["Consistent hashing", "Replication", "Stampede", "CAP for cache"],
    levels=_L("Single Redis", "Shard + replica", "Hot keys + soft TTL", "Multi-region cache", "Cache platform SLOs"),
    expected="Ring → replicas → eviction → stampede → miss path.",
    followups=["Write-through vs invalidate?", "Persistence?"],
    mistakes=["Treating cache as source of truth"],
    production=["ElastiCache/Memorystore", "Netflix EVCache", "Facebook Memcached fleet"],
    reading_mins=20,
)
_sd(
    10,
    why="Strong consistency under flash sales — inventory correctness.",
    evaluating=["Holds/TTL", "CAS", "Idempotent pay", "Waiting room"],
    levels=_L("Row lock booking", "Hold+pay saga", "Event shard + queue", "Global onsale fabric", "Marketplace inventory mesh"),
    expected="States → hold → pay → commit → failure paths.",
    followups=["Overbooking airlines?", "Seat maps cache?"],
    mistakes=["Eventual consistency on seats"],
    production=["Ticketmaster", "Amazon Lightning Deals inventory", "Airline PSS holds"],
    reading_mins=22,
)
_sd(
    11,
    why="Metadata vs blob + sync protocol — Dropbox/Drive interviews.",
    evaluating=["Chunking/dedupe", "Conflict handling", "Notify devices"],
    levels=_L("Upload whole file", "Chunked hash sync", "Conflicts + sharing ACL", "Block-level sync", "Collab editing add-on"),
    expected="Metadata DB + object chunks → sync delta → notify.",
    followups=["Simultaneous edits?", "Very large files?"],
    mistakes=["Storing huge blobs in SQL"],
    production=["Dropbox", "Google Drive", "OneDrive"],
    reading_mins=22,
)
_sd(
    12,
    why="Distributed scheduling + politeness — Google classic.",
    evaluating=["Frontier", "Dedupe", "Per-host limits", "Budget/priority"],
    levels=_L("Single crawler", "Distributed frontier", "Freshness/recrawl", "JS rendering farm", "Web-scale crawl platform"),
    expected="Frontier → fetch → extract → dedupe → politeness.",
    followups=["JavaScript-heavy pages?", "Change rates?"],
    mistakes=["Ignoring robots.txt", "Hammering one host"],
    production=["Googlebot", "Amazon product crawlers", "Bing crawler"],
    reading_mins=20,
)
_sd(
    13,
    why="Money systems — Stripe/Amazon bar for correctness.",
    evaluating=["Idempotency", "Ledger", "Webhooks", "PCI boundary"],
    levels=_L("Charge API + DB flag", "Idempotent intents + ledger", "Saga/outbox", "Multi-rail orchestration", "Global payments platform"),
    expected="Idempotency → intent → ledger → processor → webhooks.",
    followups=["Partial capture?", "Chargebacks?", "Multi-currency?"],
    mistakes=["Mutable balance rows as source of truth"],
    production=["Stripe", "PayPal", "Amazon Payments"],
    reading_mins=25,
)
_sd(
    14,
    why="Realtime ranking primitives — games + social.",
    evaluating=["ZSET ops", "Shard strategy", "Ties"],
    levels=_L("One Redis ZSET", "Season snapshots", "Sharded boards", "Approx global top-k", "Tournament platform"),
    expected="ZADD/ZREVRANGE/ZREVRANK → scale story.",
    followups=["Historical seasons?", "Friends-only board?"],
    mistakes=["ORDER BY on hot SQL without care"],
    production=["Game leaderboards", "Duolingo leagues", "Amazon bestseller ranks"],
    reading_mins=12,
)
_sd(
    15,
    why="Dynamo paper literacy — Amazon/Google distributed DB.",
    evaluating=["Hash ring", "Quorum R/W", "Conflict versions", "Anti-entropy"],
    levels=_L("Replicated KV", "Tunable quorum", "Vector clocks", "Multi-datacenter", "Storage engine internals"),
    expected="Ring → N replicas → quorum → conflicts → repair.",
    followups=["Why not Paxos always?", "Sloppy quorum?"],
    mistakes=["Equating with cache design"],
    production=["Amazon DynamoDB lineage", "Cassandra", "Riak"],
    reading_mins=25,
)
_sd(
    16,
    why="Log-based messaging — LinkedIn/Uber data infra.",
    evaluating=["Partitions/order", "Consumer groups", "Retention", "ISR acks"],
    levels=_L("Single topic queue", "Partitions + groups", "Exactly-once talk", "Multi-cluster mirror", "Streaming platform"),
    expected="Partitions → keys → consumers → offsets → retention.",
    followups=["Kafka vs RabbitMQ?", "Reorder?", "Poison messages?"],
    mistakes=["Promising global order"],
    production=["LinkedIn Kafka", "Uber uReplicator era", "Amazon MSK/Kinesis cousins"],
    reading_mins=20,
)
_sd(
    17,
    why="Easier SD warmup after URL shortener.",
    evaluating=["ID + storage tier", "Expiry GC", "Abuse"],
    levels=_L("DB paste", "Blob for large", "CDN + TTL", "Enterprise private pastes", ""),
    expected="Create id → store → fetch → expire.",
    followups=["Syntax highlight?", "Password pastes?"],
    mistakes=["No rate limits"],
    production=["pastebin.com", "GitHub gists", "Internal snippet tools"],
    reading_mins=10,
)
_sd(
    18,
    why="Geo + routing — Google Maps / Uber adjacency.",
    evaluating=["Tiles", "Road graph", "ETA traffic", "Reroute"],
    levels=_L("Static route", "A*/CH routing", "Traffic-aware ETA", "Lane-level / multimodal", "Global maps platform"),
    expected="Tiles CDN → places → graph route → ETA → client polyline.",
    followups=["Offline maps?", "Traffic incidents?"],
    mistakes=["Dijkstra on raw planetary graph without preprocessing"],
    production=["Google Maps", "Apple Maps", "Uber route service"],
    reading_mins=22,
)

# ---- AI (1–17) ----
_ai(
    1,
    why="Default AI system design in 2025–2026 — grounded enterprise Q&A.",
    evaluating=["Ingest vs query", "ACL in retrieval", "Abstain", "Eval"],
    levels=_L("Naive vector RAG", "Hybrid+rerank+cite", "ACL+freshness+eval", "Multi-corpus platform", "Org-wide knowledge mesh"),
    expected="Ingest pipeline → hybrid retrieve → grounded generate → eval.",
    followups=["Tables/code?", "Multilingual?", "Agentic RAG?"],
    mistakes=["ACL only in prompt", "No abstain path"],
    production=["Google Vertex RAG patterns", "Notion AI / Glean-style search", "Amazon Q Business"],
    reading_mins=25,
)
_ai(
    2,
    why="Retrieval infra depth — ANN tradeoffs at scale.",
    evaluating=["HNSW/IVF-PQ", "Hybrid", "Versioned embeddings"],
    levels=_L("Single FAISS index", "Sharded hybrid", "Filtered ANN", "Multi-billion vectors", "Embedding platform"),
    expected="Embed → ANN → hybrid fuse → rerank → versioning.",
    followups=["Filtered search?", "Re-embed migrations?"],
    mistakes=["Exact kNN at 100M"],
    production=["Pinecone/Weaviate/Vertex Matching Engine", "Pinterest PinCLIP-style retrieval", "Spotify search/recs"],
    reading_mins=20,
)
_ai(
    3,
    why="Shipping LLMs without eval is a fail — platforms probe this.",
    evaluating=["Offline gates", "Online metrics", "Judge calibration", "Slice failures"],
    levels=_L("Manual spot check", "Gold set + judges", "Shadow/A/B", "Eval platform", "Org quality program"),
    expected="Datasets → metrics → gate → online → humans.",
    followups=["Jailbreak suite?", "Cost as metric?"],
    mistakes=["One aggregate score only"],
    production=["OpenAI eval harness culture", "Anthropic constitutional checks", "Google side-by-side evals"],
    reading_mins=18,
)
_ai(
    4,
    why="Tool-using agents are the 2024–2026 hiring wave.",
    evaluating=["Tool schemas", "HITL gates", "Budgets", "Injection"],
    levels=_L("Single tool call", "ReAct loop", "Confirm irreversible", "Multi-agent with policies", "Agent platform"),
    expected="Tools → loop → confirm pay → budgets → audit.",
    followups=["MCP?", "When not agent?"],
    mistakes=["LLM-only authorization"],
    production=["Amazon Alexa tasking", "Google Assistant routines", "Intercom/Fin agent patterns"],
    reading_mins=22,
)
_ai(
    5,
    why="Trust & safety systems — Meta/TikTok/OpenAI.",
    evaluating=["Cascade cost", "Critical vs gray", "Appeals", "Latency tiers"],
    levels=_L("One classifier", "Cascade + humans", "Policy packs", "Adversarial robustness", "Integrity platform"),
    expected="Hash → classifiers → LLM gray → human → feedback.",
    followups=["Regional policy?", "Generative video?"],
    mistakes=["LLM-only for CSAM-class"],
    production=["Meta Integrity", "YouTube Trusted Flaggers pipeline", "OpenAI Moderation API"],
    reading_mins=18,
)
_ai(
    6,
    why="Two-tower + ranker — Netflix/YouTube/Spotify staple.",
    evaluating=["Retrieve vs rank", "Cold start", "Metrics beyond CTR"],
    levels=_L("Popularity baseline", "Two-tower ANN", "Ranker + diversity", "Multi-objective", "Recs platform"),
    expected="Candidates → rank → rules → A/B metrics.",
    followups=["Exploration?", "Position bias?"],
    mistakes=["Optimizing only clicks"],
    production=["Netflix recommendations", "YouTube home", "Spotify Discover Weekly"],
    reading_mins=20,
)
_ai(
    7,
    why="Streaming multimodal + structured notes — Zoom/Meet style.",
    evaluating=["Partial ASR", "Diarization", "Cost batching", "Privacy"],
    levels=_L("Batch transcript", "Streaming captions", "Structured actions", "Org search over meetings", "Meeting intelligence platform"),
    expected="Stream ASR → diarize → captions → summarize schema → index.",
    followups=["Code-switching?", "PII redaction?"],
    mistakes=["Summarize every utterance"],
    production=["Zoom AI Companion", "Google Meet notes", "Otter/Fireflies"],
    reading_mins=15,
)
_ai(
    8,
    why="B2B AI is quotas and tenancy — not just prompts.",
    evaluating=["Quotas", "Routing", "Isolation", "Abuse"],
    levels=_L("API key + limit", "TPM/$ budgets", "Residency + audit", "Priority lanes", "AI gateway platform"),
    expected="Auth → quota → router → meter → isolate.",
    followups=["Agent runaway?", "Exact token billing?"],
    mistakes=["Shared cache leaking tenants"],
    production=["Amazon Bedrock", "Azure OpenAI", "OpenAI platform orgs"],
    reading_mins=15,
)
_ai(
    9,
    why="Grounding + authz — Amazon/Shopify support AI.",
    evaluating=["Knowledge vs action split", "Server authz", "Escalation"],
    levels=_L("FAQ bot", "RAG+cite", "Tool refunds with caps", "Fraud-aware", "Support AI platform"),
    expected="Intent → RAG cite / tool authz → escalate.",
    followups=["Jailbreaks?", "Multi-order users?"],
    mistakes=["LLM deciding refund eligibility alone"],
    production=["Amazon customer service AI", "Shopify Sidekick", "Intercom Fin"],
    reading_mins=18,
)
_ai(
    10,
    why="Long-context products need memory tiers — assistant interviews.",
    evaluating=["Short vs long-term", "Editable memory", "Privacy delete"],
    levels=_L("Window only", "Summaries", "Fact store + recall", "Org vs user memory", "Memory platform"),
    expected="Tiers → extract → retrieve → forget APIs.",
    followups=["Wrong memory UX?", "GDPR wipe?"],
    mistakes=["Dumping full history every turn"],
    production=["ChatGPT memory", "Google Gemini apps memory", "Apple Intelligence personal context (on-device angles)"],
    reading_mins=15,
)
_ai(
    11,
    why="Inference economics — AI infra interviews.",
    evaluating=["Batching", "KV cache", "TTFT vs TPS", "Autoscaling"],
    levels=_L("One GPU one request", "Continuous batching", "Multi-LoRA", "Disaggregated prefill/decode", "Global inference fabric"),
    expected="Gateway → batch → KV → parallel → stream → scale.",
    followups=["Speculative decoding?", "Fairness across tenants?"],
    mistakes=["No batching"],
    production=["vLLM deployments", "NVIDIA Triton/TensorRT-LLM", "OpenAI/Anthropic serving stacks (public patterns)"],
    reading_mins=20,
)
_ai(
    12,
    why="Know when NOT to agentify RAG — senior judgment.",
    evaluating=["Router", "Hop budgets", "Eval multi-hop"],
    levels=_L("Always simple RAG", "Router to agentic", "Critique/reflect loop", "Tool+RAG mesh", "Research agent platform"),
    expected="Default simple → route hard → budgeted loop → eval.",
    followups=["Multi-corpus tools?", "Human confirm?"],
    mistakes=["Agentic for every query"],
    production=["Perplexity-style multi-step search", "Enterprise research copilots", "Google Deep Research-style flows"],
    reading_mins=15,
)
_ai(
    13,
    why="Cost/latency lever every production LLM app needs.",
    evaluating=["Similarity threshold", "Tenant isolation", "Invalidation"],
    levels=_L("Exact cache", "Semantic ANN cache", "Doc-version aware", "Personalized safe cache", "Edge semantic cache"),
    expected="Embed → ANN hit/miss → store → invalidate.",
    followups=["Threshold tuning?", "PII?"],
    mistakes=["Cross-tenant semantic hits"],
    production=["GPTCache-style layers", "CDN + LLM gateways", "Customer support repeat intents"],
    reading_mins=12,
)
_ai(
    14,
    why="IDE AI products — context packing under latency SLOs.",
    evaluating=["Context pack", "Repo retrieval", "FIM vs chat", "Secret safety"],
    levels=_L("Current-file complete", "Repo RAG chat", "Multi-file edit agent", "Org codebase index", "IDE AI platform"),
    expected="Pack context → retrieve → FIM/chat → safety → eval accept rate.",
    followups=["Fill-in-middle?", "License filters?"],
    mistakes=["Sending whole repo every keystroke"],
    production=["GitHub Copilot", "Cursor", "Amazon CodeWhisperer/Q Developer"],
    reading_mins=18,
)
_ai(
    15,
    why="ML platform interviews — train/serve skew killer.",
    evaluating=["Offline/online", "Point-in-time joins", "Skew monitors"],
    levels=_L("Ad-hoc tables", "Feature definitions", "Online KV + streaming", "Discovery/ACL", "Feature platform"),
    expected="Defs → offline PIT → online KV → materialize → skew.",
    followups=["Embedding features?", "On-demand compute?"],
    mistakes=["Training on future labels"],
    production=["Uber Michelangelo", "Airbnb Zipline", "Feast/Tecton-style stores"],
    reading_mins=18,
)
_ai(
    16,
    why="Security interviews for agents that read the open web.",
    evaluating=["Trust boundaries", "Allowlists", "Dual LLM", "Red-team CI"],
    levels=_L("Prompt 'ignore'", "Delimiters + filters", "Tool allowlist + HITL", "Dual-model isolation", "Agent security program"),
    expected="Untrusted data → isolate → allowlist tools → monitor.",
    followups=["Indirect injection?", "URL tool fetch?"],
    mistakes=["Concatenating docs into system prompt"],
    production=["Microsoft Copilot security guidance", "Google secure AI agents patterns", "OWASP LLM Top 10 themes"],
    reading_mins=15,
)
_ai(
    17,
    why="Product ML rigor for LLM features — Meta/Google style.",
    evaluating=["Guardrails", "Bucketing", "Ramp + hold", "Spillover"],
    levels=_L("Ship and pray", "A/B with guardrails", "Sequential testing", "Interleaving/side-by-side", "Experimentation platform"),
    expected="Metrics → bucket → log → ramp → auto-hold.",
    followups=["Novelty effects?", "Offline gate link?"],
    mistakes=["Peeking without plan"],
    production=["Meta XP", "Google Experiment framework", "OpenAI gradual rollouts"],
    reading_mins=12,
)


def get_enrichment(lab: str, qnum: int) -> dict | None:
    return ENRICHMENT.get(lab, {}).get(qnum)
