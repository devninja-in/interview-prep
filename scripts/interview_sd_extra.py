#!/usr/bin/env python3
"""Extra system design Q&As from 2025–2026 FAANG frequency research."""
from __future__ import annotations

from interview_helpers import (
    bullets,
    callout,
    figure_diagram,
    qa_block,
    steps,
)


def sd_extra_questions(start: int = 11) -> list[str]:
    q: list[str] = []
    n = start

    q.append(
        qa_block(
            qnum=n,
            title="Design Dropbox / Google Drive",
            asked="Meta, Amazon, Google, Microsoft — top file-storage design",
            difficulty="Hard",
            pattern="Chunked upload · sync · metadata vs blob",
            prompt=(
                "Design a cloud file storage and sync service: upload/download files, sync across "
                "devices, share folders, and handle large files efficiently."
            ),
            sections=[
                (
                    "Clarify",
                    bullets(
                        [
                            "Max file size? Concurrent editors?",
                            "Version history? Offline sync?",
                            "Sharing ACLs / links?",
                        ]
                    ),
                ),
                (
                    "Diagram",
                    figure_diagram("dropbox-sync", "File metadata vs chunked blob storage"),
                ),
                (
                    "Step-by-step",
                    steps(
                        [
                            "<strong>Split metadata and bytes:</strong> metadata DB (file_id, "
                            "path, versions, ACL); blobs in object storage.",
                            "<strong>Chunk files</strong> (e.g. 4MB); content-hash chunks for "
                            "dedupe; upload only missing chunks.",
                            "<strong>Sync protocol:</strong> client keeps local revision; pull "
                            "delta since last sync; conflict → last-write-wins or branch versions.",
                            "<strong>Notifications:</strong> long-poll / websocket for file-change "
                            "events to other devices.",
                            "<strong>Large uploads:</strong> multipart / resumable; commit "
                            "metadata only when all chunks ACK'd.",
                            "<strong>Sharing:</strong> ACL on folder nodes; link tokens with expiry.",
                        ]
                    ),
                ),
                (
                    "Deep dives",
                    bullets(
                        [
                            "Namespace tree sharding by owner_id.",
                            "CDC from metadata → search index.",
                            "Client block-level sync (rsync-like) for huge files.",
                        ]
                    ),
                ),
            ],
        )
    )
    n += 1

    q.append(
        qa_block(
            qnum=n,
            title="Design a Web Crawler",
            asked="Google, Amazon — classic distributed systems question",
            difficulty="Hard",
            pattern="URL frontier · politeness · dedupe",
            prompt=(
                "Design a distributed web crawler that discovers and fetches pages at large "
                "scale while respecting robots.txt and politeness limits."
            ),
            sections=[
                (
                    "Diagram",
                    figure_diagram("web-crawler", "Distributed crawl frontier"),
                ),
                (
                    "Step-by-step",
                    steps(
                        [
                            "<strong>URL frontier:</strong> prioritized queue of URLs to fetch "
                            "(BFS / priority by PageRank estimate).",
                            "<strong>Dedupe:</strong> seen URL set (Bloom + store); canonicalize "
                            "URLs.",
                            "<strong>Politeness:</strong> per-host rate limits; respect robots.txt "
                            "(cache rules).",
                            "<strong>Workers:</strong> fetch → extract links → enqueue new URLs; "
                            "store raw HTML / parse text.",
                            "<strong>Distributed:</strong> shard frontier by host hash so one "
                            "host stays on one worker (politeness).",
                            "<strong>Failure:</strong> retries, crawl budget, blacklist bad hosts.",
                        ]
                    ),
                ),
                (
                    "Google flavor",
                    callout(
                        "Often probed",
                        "<p>How do you avoid drowning in low-value pages? Priority + crawl budget. "
                        "How do you refresh? Recrawl based on change rate.</p>",
                    ),
                ),
            ],
        )
    )
    n += 1

    q.append(
        qa_block(
            qnum=n,
            title="Design a Payment System",
            asked="Stripe, PayPal, Amazon, Square — money-moving design",
            difficulty="Hard",
            pattern="Idempotency · ledger · saga / outbox",
            prompt=(
                "Design a payment service that charges cards, handles retries safely, supports "
                "refunds, and keeps an accurate ledger under failures."
            ),
            sections=[
                (
                    "Diagram",
                    figure_diagram("payment-saga", "Idempotent payment and ledger"),
                ),
                (
                    "Step-by-step",
                    steps(
                        [
                            "<strong>Idempotency keys</strong> on every charge from the client — "
                            "retries must not double-charge.",
                            "<strong>API:</strong> create PaymentIntent → confirm → capture "
                            "(or auth+capture).",
                            "<strong>Ledger:</strong> append-only double-entry journal; balances "
                            "derived — never overwrite money rows.",
                            "<strong>Provider calls:</strong> stripe/processor behind adapter; "
                            "store provider refs; reconcile webhooks with signature verify.",
                            "<strong>Distributed tx:</strong> transactional outbox or saga for "
                            "order ↔ payment; compensating refunds on failure.",
                            "<strong>PCI:</strong> never store raw PAN; use tokens; isolate "
                            "network.",
                        ]
                    ),
                ),
                (
                    "Strong signal",
                    callout(
                        "Say this",
                        "<p>At-least-once webhooks + idempotent handlers. Exactly-once is a "
                        "ledger property you engineer, not a queue guarantee.</p>",
                    ),
                ),
            ],
        )
    )
    n += 1

    q.append(
        qa_block(
            qnum=n,
            title="Design a Leaderboard",
            asked="Amazon, Meta, gaming companies — realtime ranking",
            difficulty="Medium",
            pattern="Sorted sets · sharding · top-k",
            prompt=(
                "Design a game leaderboard that supports updating a player's score and fetching "
                "top-K and a player's rank with low latency."
            ),
            sections=[
                (
                    "Diagram",
                    figure_diagram("leaderboard", "Redis sorted set leaderboard"),
                ),
                (
                    "Step-by-step",
                    steps(
                        [
                            "Redis ZSET (score → member) for one board: ZADD update, ZREVRANGE "
                            "top-K, ZREVRANK for rank — O(log n).",
                            "Scale: shard by competition/season; or by player hash with aggregation "
                            "for global top-K (harder).",
                            "Ties: use score + timestamp composite.",
                            "Historical boards: snapshot immutable ZSET per season.",
                            "Fan-out reads with cache; writes go to primary.",
                        ]
                    ),
                ),
            ],
        )
    )
    n += 1

    q.append(
        qa_block(
            qnum=n,
            title="Design a Distributed Key-Value Store",
            asked="Amazon (Dynamo), Google — fundamentals of distributed DBs",
            difficulty="Hard",
            pattern="Consistent hashing · quorum · replication",
            prompt=(
                "Design a Dynamo-style distributed key-value store with put/get, high "
                "availability, and horizontal scale."
            ),
            sections=[
                (
                    "Step-by-step",
                    steps(
                        [
                            "Consistent hashing ring + virtual nodes for partition.",
                            "N replicas on successor nodes; client or coordinator uses quorum "
                            "R/W (e.g. N=3, R=2, W=2).",
                            "Versioning: vector clocks / version numbers; reconcile conflicts "
                            "(last-write-wins or client merge).",
                            "Hinted handoff + anti-entropy (Merkle trees) for temporary failures.",
                            "Tunable consistency: CAP — prefer AP with eventual consistency for "
                            "shopping-cart style.",
                        ]
                    ),
                ),
                (
                    "Diagram",
                    figure_diagram("consistent-hash-cache", "Consistent hashing for KV shards"),
                ),
                (
                    "Contrast",
                    "<p>Different from a cache: durability, replication, conflict resolution, "
                    "and anti-entropy are first-class.</p>",
                ),
            ],
        )
    )
    n += 1

    q.append(
        qa_block(
            qnum=n,
            title="Design a Distributed Message Queue (Kafka-like)",
            asked="LinkedIn, Amazon, Uber, Confluent-style interviews",
            difficulty="Hard",
            pattern="Partitions · consumer groups · retention",
            prompt=(
                "Design a pub/sub log that supports high-throughput producers, consumer groups, "
                "and durable retention."
            ),
            sections=[
                (
                    "Step-by-step",
                    steps(
                        [
                            "Topics split into partitions (ordered append logs).",
                            "Producers pick partition by key (ordering per key) or round-robin.",
                            "Replicas: leader + followers; ack on ISR.",
                            "Consumer groups: each partition → one consumer in the group; "
                            "commit offsets.",
                            "Retention by time/size; consumers are pull-based.",
                            "Scale: more partitions; rebalance on membership change.",
                        ]
                    ),
                ),
                (
                    "Diagram",
                    figure_diagram("kafka-partitions", "Topic partitions and consumer group"),
                ),
            ],
        )
    )
    n += 1

    q.append(
        qa_block(
            qnum=n,
            title="Design Pastebin",
            asked="Amazon, Meta — easier SD warmup after URL shortener",
            difficulty="Medium",
            pattern="Object storage · short IDs · expiry",
            prompt=(
                "Design a pastebin: users paste text, get a unique URL, optional expiry and "
                "syntax highlighting."
            ),
            sections=[
                (
                    "Step-by-step",
                    steps(
                        [
                            "Similar to URL shortener: generate short id; store content in object "
                            "store or DB (small pastes in DB, large in blob).",
                            "Metadata: id, expiry, visibility, user.",
                            "CDN/cache for public pastes; rate-limit create.",
                            "GC expired pastes with TTL sweeper.",
                            "Optional: raw vs HTML view; password-protected pastes.",
                        ]
                    ),
                ),
            ],
        )
    )
    n += 1

    q.append(
        qa_block(
            qnum=n,
            title="Design Google Maps (navigation basics)",
            asked="Google, Uber — geo + routing",
            difficulty="Hard",
            pattern="Map tiles · graph routing · ETA",
            prompt=(
                "Design the core of a maps/navigation product: show maps, find places, and "
                "compute routes with ETA."
            ),
            sections=[
                (
                    "Step-by-step",
                    steps(
                        [
                            "<strong>Tiles:</strong> pre-render / vector tiles by zoom; CDN heavily.",
                            "<strong>Places search:</strong> geospatial index + text (similar to "
                            "typeahead + geo filter).",
                            "<strong>Road graph:</strong> nodes/edges with travel times; "
                            "Dijkstra / A* / contraction hierarchies for speed.",
                            "<strong>ETA:</strong> traffic-aware edge weights updated nearline.",
                            "<strong>Client:</strong> request route → server returns polyline + "
                            "steps; reroute on deviation.",
                        ]
                    ),
                ),
                (
                    "Tie-in",
                    "<p>Shares geo indexing ideas with Uber matching "
                    "(<a href=\"interview-sd.html#q5\">Q5</a>) but routing graph is the heart.</p>",
                ),
            ],
        )
    )

    return q
