#!/usr/bin/env python3
"""AI / ML system design interview Q&As — deep, diagrammed, company-ready."""
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


def ai_questions() -> list[str]:
    q: list[str] = []

    # ---------- Q1 RAG ----------
    q.append(
        qa_block(
            qnum=1,
            title="Design a ChatGPT-like Assistant with Company Knowledge (RAG)",
            asked="Google, Meta, Stripe, OpenAI-adjacent, enterprise AI (most common AI design)",
            difficulty="Hard",
            pattern="RAG · chunking · hybrid retrieval · grounded generation · ACL",
            prompt=(
                "Design an internal chatbot that answers employee questions using private "
                "wikis, tickets, and PDFs. It must cite sources, respect permissions, and "
                "minimize hallucinations. Walk the interviewer from requirements to a "
                "production architecture."
            ),
            sections=[
                (
                    "Clarify (say these out loud)",
                    bullets(
                        [
                            "<strong>Users &amp; ACL:</strong> all employees, or role-based doc access?",
                            "<strong>Latency:</strong> streaming first token &lt;1s? full answer &lt;5s?",
                            "<strong>Freshness:</strong> wiki updates visible in minutes or hours?",
                            "<strong>Modalities:</strong> text only, or tables/images/code?",
                            "<strong>Languages:</strong> English only vs multilingual?",
                            "<strong>Escalation:</strong> handoff to human / ticket create?",
                            "<strong>Compliance:</strong> retention, audit logs, no training on prompts?",
                        ]
                    ),
                ),
                (
                    "Whiteboard diagram",
                    figure_diagram("rag-detailed", "Detailed RAG ingest and query paths"),
                ),
                (
                    "Step-by-step solution",
                    steps(
                        [
                            "<strong>Split two pipelines.</strong> Ingest is async; query is online. "
                            "Never embed on the request path for large corpora.",
                            "<strong>Ingest:</strong> connectors (Confluence/Drive/Ticket APIs) → "
                            "normalize HTML/PDF → chunk (start 400–800 tokens, 10–15% overlap, "
                            "split on headings) → embed → upsert <code>{vector, text, source_url, "
                            "doc_id, updated_at, acl_tags}</code> into a vector store + keep raw "
                            "docs in object storage.",
                            "<strong>Query:</strong> auth user → optional query rewrite / HyDE → "
                            "embed query → <em>hybrid</em> retrieve (ANN + BM25) <em>with ACL "
                            "filter in the query</em> → rerank top 50→5–10 → build prompt "
                            "(\"answer ONLY from context; cite [n]\") → stream tokens → return "
                            "answer + citation links.",
                            "<strong>Abstain:</strong> if top score / reranker confidence is low, "
                            "say \"I could not find this in company docs\" instead of guessing.",
                            "<strong>Observe:</strong> log trace_id, retrieved chunk ids, prompt "
                            "version, latency, thumbs — feed eval (Q3).",
                        ]
                    ),
                ),
                (
                    "Capacity sketch (example)",
                    "<p>1M docs × ~5 chunks = 5M vectors at 1536-d ≈ tens of GB raw; with HNSW/"
                    "PQ plan memory carefully. 50 QPS peak with p95 &lt; 2s is typical internal "
                    "scale — cache frequent queries; autoscale embed + LLM separately.</p>",
                ),
                (
                    "Prompt skeleton",
                    code_block(
                        "text",
                        """System:
You are a company knowledge assistant. Use ONLY the Context passages.
If Context is insufficient, say you do not know. Cite sources as [1], [2].

Context:
[1] (source: wiki/Benefits.md, updated: 2026-01-12)
...passage...
[2] ...

User:
How many days of parental leave do we get?""",
                    ),
                ),
                (
                    "Follow-ups &amp; strong answers",
                    bullets(
                        [
                            "<strong>Tables/code?</strong> Keep table chunks intact; use "
                            "structure-aware splitters; sometimes summarize tables into facts.",
                            "<strong>ACL?</strong> Filter at retrieval with the user's groups — "
                            "never retrieve then hope the LLM hides secrets.",
                            "<strong>Updates?</strong> CDC / webhooks → rechunk changed docs; "
                            "tombstone deletes; show <code>updated_at</code> in citations.",
                            "<strong>Eval?</strong> Gold Q&amp;A: retrieval recall@k, "
                            "groundedness, citation accuracy, latency, cost.",
                        ]
                    ),
                ),
                (
                    "Common failure modes",
                    callout(
                        "What fails interviews",
                        bullets(
                            [
                                "Drawing only \"LLM + vector DB\" with no ingest, ACL, or eval.",
                                "Putting permissions only in the system prompt.",
                                "No abstain path — model always invents an answer.",
                                "Ignoring chunking / metadata as \"implementation details\".",
                            ]
                        ),
                    ),
                ),
            ],
        )
    )

    # ---------- Q2 Vector search ----------
    q.append(
        qa_block(
            qnum=2,
            title="Design Semantic Search / Vector Search at Scale",
            asked="Google, Amazon, Notion, OpenAI platform, search-infra interviews",
            difficulty="Hard",
            pattern="Embeddings · ANN (HNSW/IVF-PQ) · hybrid · rerank",
            prompt=(
                "Design search that finds relevant documents by meaning for ~100M documents "
                "with p95 retrieval under ~100ms (before generation). Cover indexing, query "
                "path, and tradeoffs."
            ),
            sections=[
                (
                    "Clarify",
                    bullets(
                        [
                            "Recall target (e.g. recall@100 ≥ 0.95)?",
                            "Freshness: seconds, minutes, or daily rebuilds?",
                            "Multilingual? Filters (time, type, tenant)?",
                            "Is this retrieval-only or part of RAG?",
                        ]
                    ),
                ),
                (
                    "Diagram",
                    figure_diagram("hybrid-search", "Hybrid BM25 + dense retrieval with fusion"),
                ),
                (
                    "Step-by-step solution",
                    steps(
                        [
                            "<strong>Document store:</strong> source of truth in object/SQL; "
                            "search index holds vectors + lean metadata + doc_id.",
                            "<strong>Embedding service:</strong> batch embed offline; online "
                            "embed queries (cache popular query vectors).",
                            "<strong>ANN index:</strong> start with HNSW for high recall; for "
                            "100M+ consider IVF-PQ / disk-ANN to control RAM. Shard by "
                            "collection or tenant.",
                            "<strong>Hybrid:</strong> run BM25 in parallel; fuse with Reciprocal "
                            "Rank Fusion (RRF). Lexical saves error codes, SKUs, rare names.",
                            "<strong>Rerank:</strong> cross-encoder on top 50–100 for quality; "
                            "budget latency (e.g. +30–50ms).",
                            "<strong>Versioning:</strong> model upgrades need re-embed — store "
                            "<code>embedding_model_version</code>; blue/green index swap.",
                        ]
                    ),
                ),
                (
                    "Numbers to mention",
                    "<p>100M × 768-d float32 ≈ 300GB raw vectors — compression (PQ) and sharding "
                    "are not optional. Query embed ~10–30ms; ANN ~5–20ms; rerank dominates if "
                    "naive. Cap candidates early.</p>",
                ),
                (
                    "Tradeoffs interviewers expect",
                    bullets(
                        [
                            "Recall vs latency vs memory (efSearch / nprobe knobs).",
                            "Filtered ANN: pre-filter vs post-filter vs metadata-aware indexes.",
                            "Exact kNN is a non-starter at this scale — say so.",
                            "Multilingual: one multilingual encoder vs per-language indexes.",
                        ]
                    ),
                ),
            ],
        )
    )

    # ---------- Q3 Eval ----------
    q.append(
        qa_block(
            qnum=3,
            title="Design an LLM Evaluation Pipeline",
            asked="OpenAI, Anthropic-adjacent, Google, AI platform / applied-science loops",
            difficulty="Medium–Hard",
            pattern="Offline gates · online metrics · LLM-as-judge · traces",
            prompt=(
                "You ship prompt, model, and RAG changes weekly. Design a system that catches "
                "quality regressions before and after production — without blocking the team "
                "forever."
            ),
            sections=[
                (
                    "Diagram",
                    figure_diagram("eval-pipeline", "Offline eval gates plus online feedback"),
                ),
                (
                    "Step-by-step solution",
                    steps(
                        [
                            "<strong>Split retrieval vs generation metrics.</strong> A bad answer "
                            "may be bad retrieve or bad generate — measure both.",
                            "<strong>Gold datasets:</strong> curated questions with expected "
                            "docs / answers / rubrics. Tag slices (safety, ACL, freshness, "
                            "multilingual).",
                            "<strong>Offline runner:</strong> for each candidate config, execute "
                            "pipeline → compute recall@k, EM/F1 where applicable, "
                            "faithfulness/groundedness, toxicity, latency, $/query.",
                            "<strong>LLM-as-judge:</strong> rubric prompts + reference answers; "
                            "calibrate with human labels; spot-check weekly.",
                            "<strong>Gate:</strong> compare to baseline; block deploy if primary "
                            "metrics regress beyond threshold (or safety worsens at all).",
                            "<strong>Online:</strong> shadow traffic, A/B, thumbs, regenerate "
                            "rate, task success. Trace store: prompt version, chunk ids, tools, "
                            "tokens, cost.",
                            "<strong>Human loop:</strong> sample failures into annotation queues "
                            "→ grow gold set.",
                        ]
                    ),
                ),
                (
                    "Example gate table",
                    """<div class="table-wrap"><table>
<caption>Ship / no-ship example</caption>
<thead><tr><th>Metric</th><th>Baseline</th><th>Candidate</th><th>Rule</th></tr></thead>
<tbody>
<tr><td>Retrieval recall@5</td><td>0.81</td><td>0.84</td><td>must not drop &gt;2pp</td></tr>
<tr><td>Groundedness</td><td>0.88</td><td>0.85</td><td>block</td></tr>
<tr><td>p95 latency</td><td>2.1s</td><td>2.4s</td><td>warn if &gt;+15%</td></tr>
<tr><td>$ / 1k queries</td><td>$4.2</td><td>$3.9</td><td>informational</td></tr>
</tbody></table></div>""",
                ),
                (
                    "Pitfalls",
                    bullets(
                        [
                            "Judges without rubrics → noisy, gameable scores.",
                            "Only online thumbs → slow and biased.",
                            "One aggregate score hides slice failures (e.g. ACL questions).",
                            "Ignoring cost — a \"better\" model can be 10× spend.",
                        ]
                    ),
                ),
            ],
        )
    )

    # ---------- Q4 Agent ----------
    q.append(
        qa_block(
            qnum=4,
            title="Design a Tool-Using Agent (Flight Booking Assistant)",
            asked="Google, Amazon, Microsoft, AI startups — top 2024–2026 agent question",
            difficulty="Hard",
            pattern="Planner · tool schemas · HITL · budgets · idempotency",
            prompt=(
                "Design an agent that searches flights, compares options, and books with user "
                "confirmation. It must call external APIs safely and not run away on cost or "
                "side effects."
            ),
            sections=[
                (
                    "Diagram",
                    figure_diagram("agent-tools", "Agent planner with gated tools and budgets"),
                ),
                (
                    "Step-by-step solution",
                    steps(
                        [
                            "<strong>Define tools as the product API.</strong> "
                            "<code>search_flights</code>, <code>get_fare_rules</code>, "
                            "<code>create_hold</code>, <code>confirm_booking</code>, "
                            "<code>charge_payment</code> — each with JSON Schema, timeouts, "
                            "auth scopes.",
                            "<strong>Orchestrator loop:</strong> load session state → LLM "
                            "chooses next action (tool or reply) → validate args → execute → "
                            "append observation → repeat until done / need user / budget hit.",
                            "<strong>Session state:</strong> slots (origin, dest, dates, cabin, "
                            "budget) + last search results ids — do not rely on raw chat alone.",
                            "<strong>Gate irreversible tools:</strong> pay/book require explicit "
                            "user confirm in UI; server checks confirm token.",
                            "<strong>Budgets:</strong> max steps (e.g. 12), max tokens, max $, "
                            "detect repeated identical tool calls → stop.",
                            "<strong>Reliability:</strong> idempotency keys on hold/pay; retries "
                            "with backoff; treat tool output as untrusted (prompt injection).",
                            "<strong>Audit:</strong> immutable log of tool calls for support/"
                            "compliance.",
                        ]
                    ),
                ),
                (
                    "Tool schema example",
                    code_block(
                        "json",
                        """{
  "name": "search_flights",
  "description": "Search one-way or round-trip flights",
  "parameters": {
    "type": "object",
    "required": ["from", "to", "date"],
    "properties": {
      "from": {"type": "string", "pattern": "^[A-Z]{3}$"},
      "to": {"type": "string", "pattern": "^[A-Z]{3}$"},
      "date": {"type": "string", "format": "date"},
      "cabin": {"enum": ["economy", "premium", "business"]}
    }
  }
}""",
                    ),
                ),
                (
                    "Pseudo-orchestrator",
                    code_block(
                        "python",
                        '''def run_agent(session, user_msg):
    session.messages.append({"role": "user", "content": user_msg})
    for step in range(MAX_STEPS):
        decision = llm.plan(session.messages, tools=TOOL_SPECS)
        if decision.type == "reply":
            return decision.text
        if decision.tool in IRREVERSIBLE and not session.user_confirmed:
            return ask_confirmation(decision)
        args = validate(decision.tool, decision.args)  # raises on bad schema
        result = runtime.call(decision.tool, args, idem=session.step_key(step))
        session.messages.append({"role": "tool", "name": decision.tool, "content": result})
    return "I hit my step limit — here is what I found so far…"''',
                    ),
                ),
                (
                    "Follow-ups",
                    bullets(
                        [
                            "<strong>Why not one giant prompt?</strong> Tools keep side effects "
                            "explicit and testable.",
                            "<strong>MCP?</strong> Same idea — discovered schemas, scoped auth "
                            "(see MCP chapter / Q follow-ups in drills).",
                            "<strong>When NOT to use an agent?</strong> Fixed workflows → plain "
                            "API + form; agents add latency and failure modes.",
                        ]
                    ),
                ),
            ],
        )
    )

    # ---------- Q5 Moderation ----------
    q.append(
        qa_block(
            qnum=5,
            title="Design Content Moderation with ML + LLMs",
            asked="Meta, TikTok, OpenAI, Trust & Safety / integrity interviews",
            difficulty="Hard",
            pattern="Cascaded classifiers · human review · appeals · policy packs",
            prompt=(
                "Design a system that detects policy-violating user content (text, images, "
                "video) at upload and in feeds — balancing precision, recall, latency, and cost."
            ),
            sections=[
                (
                    "Diagram",
                    figure_diagram("moderation-cascade", "Cascaded moderation pipeline"),
                ),
                (
                    "Step-by-step solution",
                    steps(
                        [
                            "<strong>Policy packs:</strong> machine-readable rules per region/"
                            "product (severity, spam, NSFW, self-harm, etc.).",
                            "<strong>Cascade for cost:</strong> (1) exact/perceptual hashes for "
                            "known CSAM/terror; (2) cheap classifiers; (3) multimodal LLM only "
                            "on uncertain scores; (4) human review for high-severity or appeals.",
                            "<strong>Actions:</strong> block, blur, age-gate, demonetize, "
                            "queue — not only binary delete.",
                            "<strong>Latency tiers:</strong> chat may need &lt;100ms heuristics; "
                            "VOD can be async before publish.",
                            "<strong>Feedback:</strong> moderator labels → training data; "
                            "shadow-deploy new models; track FP/FN by policy.",
                            "<strong>Adversaries:</strong> rate limits, graph features, "
                            "obfuscation detectors — LLM alone is not enough for critical classes.",
                        ]
                    ),
                ),
                (
                    "Interview depth",
                    callout(
                        "Say this",
                        "<p>Critical categories must not depend on a generative model as the "
                        "only line of defense. Use deterministic matchers + specialized "
                        "classifiers; LLMs help on gray areas and explanations for reviewers.</p>",
                    ),
                ),
            ],
        )
    )

    # ---------- Q6 Recsys ----------
    q.append(
        qa_block(
            qnum=6,
            title="Design Recommendations with Embeddings",
            asked="Netflix, Spotify, YouTube, Amazon, Meta ranking interviews",
            difficulty="Hard",
            pattern="Two-tower retrieval · candidate gen · ranking · exploration",
            prompt=(
                "Design recommendations for a media app that suggests what a user engages "
                "with next. Cover candidate generation, ranking, cold start, and metrics."
            ),
            sections=[
                (
                    "Diagram",
                    figure_diagram("recsys-towers", "Two-tower retrieval plus ranking"),
                ),
                (
                    "Step-by-step solution",
                    steps(
                        [
                            "<strong>Problem split:</strong> retrieve ~O(10³–10⁴) candidates "
                            "cheaply, then rank with a heavier model.",
                            "<strong>Two-tower:</strong> user tower and item tower → dot product "
                            "/ cosine; ANN over item embeddings for retrieval.",
                            "<strong>Features:</strong> history, context (time/device), "
                            "freshness, popularity priors for cold start.",
                            "<strong>Ranker:</strong> gradient-boosted trees or deep ranker on "
                            "candidates with cross features.",
                            "<strong>Business rules:</strong> diversity, creator fairness, "
                            "exploration budget (ε-greedy / bandits).",
                            "<strong>Serving:</strong> precompute user embeddings; nearline "
                            "updates from session; feature store for ranker.",
                            "<strong>Metrics:</strong> not only CTR — dwell, completion, "
                            "long-term retention; offline replay + online A/B.",
                        ]
                    ),
                ),
                (
                    "Cold start",
                    bullets(
                        [
                            "New items: content embeddings from title/metadata/audio/video.",
                            "New users: onboarding preferences + popular-in-locale priors.",
                            "Do not wait for collaborative signal only.",
                        ]
                    ),
                ),
            ],
        )
    )

    # ---------- Q7 Transcription ----------
    q.append(
        qa_block(
            qnum=7,
            title="Design Real-Time Meeting Transcription + Summarization",
            asked="Zoom, Microsoft, Google, Otter-style product interviews",
            difficulty="Medium–Hard",
            pattern="Streaming ASR · diarization · structured LLM notes · search",
            prompt=(
                "Design a system that live-transcribes meetings and produces summaries, action "
                "items, and searchable notes afterward."
            ),
            sections=[
                (
                    "Diagram",
                    figure_diagram("transcription-ai", "Streaming ASR to summary and search"),
                ),
                (
                    "Step-by-step solution",
                    steps(
                        [
                            "<strong>Ingest audio:</strong> client or SFU sends stream → "
                            "streaming ASR with partial hypotheses.",
                            "<strong>Diarization:</strong> speaker labels (and optional voice "
                            "profiles) aligned to transcript segments.",
                            "<strong>Live UX:</strong> push partials over WebSocket; accept "
                            "revisions as ASR stabilizes.",
                            "<strong>Notes:</strong> on end (or every N minutes) LLM fills a "
                            "schema: decisions, action items {owner, due}, risks — not free prose "
                            "only.",
                            "<strong>Search:</strong> index segments with BM25 + embeddings; "
                            "link back to timestamps.",
                            "<strong>Privacy:</strong> PII redaction options, retention TTLs, "
                            "region lock; do not train on customer audio by default.",
                        ]
                    ),
                ),
                (
                    "Cost control",
                    "<p>Do not summarize every utterance. Batch windows. Offer \"transcript only\" "
                    "tiers. Cache repeated meeting templates.</p>",
                ),
            ],
        )
    )

    # ---------- Q8 Multi-tenant ----------
    q.append(
        qa_block(
            qnum=8,
            title="Design Multi-Tenant AI SaaS with Cost Controls",
            asked="B2B AI startups, Amazon Bedrock-style, platform engineering interviews",
            difficulty="Medium–Hard",
            pattern="Quotas · routing · isolation · metering · abuse",
            prompt=(
                "You sell an API that wraps foundation models to thousands of tenants. Design "
                "tenancy, billing, noisy-neighbor protection, and data isolation."
            ),
            sections=[
                (
                    "Diagram",
                    figure_diagram("multi-tenant-ai", "Gateway quotas and model routing"),
                ),
                (
                    "Step-by-step solution",
                    steps(
                        [
                            "<strong>Identity:</strong> per-tenant API keys / OAuth; map to "
                            "plan limits.",
                            "<strong>Gateway:</strong> auth → rate limit (RPM + TPM) → "
                            "daily/$ quotas → model router (policy: default model, allowed "
                            "providers, data residency).",
                            "<strong>Metering:</strong> tokens in/out, tool calls, retrieval "
                            "units → billing pipeline; show usage dashboards.",
                            "<strong>Isolation:</strong> encrypt data per tenant where required; "
                            "strict retrieval ACL; no cross-tenant caches of prompts with PII.",
                            "<strong>Abuse:</strong> anomaly detection on token spikes; "
                            "fail closed on quota; priority lanes for enterprise.",
                            "<strong>Agent runaway:</strong> require max_steps / max_$ on "
                            "agent endpoints; estimate cost before loops.",
                        ]
                    ),
                ),
                (
                    "Strong closer",
                    callout(
                        "Product sense",
                        "<p>Quotas, residency, and audit logs are the enterprise product — "
                        "the LLM call is the commodity. Lead with tenancy, then models.</p>",
                    ),
                ),
            ],
        )
    )

    # ---------- Q9 Support bot ----------
    q.append(
        qa_block(
            qnum=9,
            title="Design a Hallucination-Resistant Customer Support Bot",
            asked="Amazon, Shopify, Intercom-like, Stripe support-AI interviews",
            difficulty="Hard",
            pattern="Intent route · grounded RAG · deterministic actions · escalation",
            prompt=(
                "A support bot can explain policies, refund within limits, and reset passwords. "
                "Keep it truthful and prevent unsafe or unauthorized actions."
            ),
            sections=[
                (
                    "Diagram",
                    figure_diagram("grounded-support", "Knowledge vs action paths for support"),
                ),
                (
                    "Step-by-step solution",
                    steps(
                        [
                            "<strong>Intent classifier:</strong> knowledge vs action vs "
                            "frustrated/escalation.",
                            "<strong>Knowledge path:</strong> RAG over approved policy corpus "
                            "with mandatory citations; abstain if empty retrieval; never invent "
                            "policy numbers.",
                            "<strong>Action path:</strong> tools with <em>server-side</em> "
                            "authorization (order ownership, refund caps, fraud checks). The LLM "
                            "proposes; the tool enforces.",
                            "<strong>Separate tones:</strong> helpful chat ≠ authorized action. "
                            "Confirm destructive actions.",
                            "<strong>Escalation:</strong> low confidence, user asks human, "
                            "policy gaps, high $ — hand off transcript.",
                            "<strong>Security:</strong> jailbreak + prompt-injection tests in "
                            "CI; treat ticket text as untrusted.",
                        ]
                    ),
                ),
                (
                    "Refund tool (principle)",
                    code_block(
                        "python",
                        """def refund(order_id, amount_cents, actor_user_id, confirm_token):
    order = db.get_order(order_id)
    assert order.user_id == actor_user_id
    assert amount_cents <= policy.max_auto_refund_cents(order)
    assert confirm_token_valid(confirm_token)
    # LLM cannot bypass these checks
    return payments.refund(order_id, amount_cents, idempotency_key=...)""",
                    ),
                ),
            ],
        )
    )

    # ---------- Q10 Memory ----------
    q.append(
        qa_block(
            qnum=10,
            title="Design Memory for a Long-Running Personal Assistant",
            asked="OpenAI, Google Assistant-style, agent platform interviews",
            difficulty="Hard",
            pattern="Short-term · working state · long-term facts · semantic recall",
            prompt=(
                "Design memory so an assistant remembers preferences and projects across months "
                "without stuffing the entire history into every prompt."
            ),
            sections=[
                (
                    "Diagram",
                    figure_diagram("memory-tiers", "Tiered memory architecture"),
                ),
                (
                    "Step-by-step solution",
                    steps(
                        [
                            "<strong>Short-term:</strong> current thread in the context window; "
                            "when near limit, summarize older turns but pin IDs/numbers into "
                            "structured working state.",
                            "<strong>Working state:</strong> task slots (project name, deadlines) "
                            "as JSON — not only prose summary.",
                            "<strong>Long-term write:</strong> extract durable facts/preferences "
                            "with confidence; prefer explicit \"Remember that…\"; store "
                            "user-visible, editable records.",
                            "<strong>Long-term read:</strong> each turn retrieve top relevant "
                            "memories (metadata filters + embeddings) into the system prompt.",
                            "<strong>Forget:</strong> tombestone/delete APIs; GDPR wipe across "
                            "SQL + vectors + caches.",
                            "<strong>Separation:</strong> personal vs org memory with different "
                            "ACLs in B2B.",
                        ]
                    ),
                ),
                (
                    "Risks to call out",
                    bullets(
                        [
                            "Wrong memories poison future answers — make correction easy.",
                            "Never store passwords or payment secrets in memory.",
                            "Silent inference of sensitive attributes can be creepy/wrong — "
                            "be conservative.",
                        ]
                    ),
                ),
                (
                    "Mini data model",
                    code_block(
                        "text",
                        """MemoryRecord {
  id, user_id, org_id?,
  type: preference | fact | episode,
  text, embedding,
  confidence, source, updated_at,
  deleted_at?
}""",
                    ),
                ),
            ],
        )
    )

    return q


def ai_lab_body() -> str:
    intro = """
<p>This lab is built for <strong>AI / ML system design interviews</strong> at product companies
and AI platforms — the loops that ask you to design RAG, agents, eval, and cost-safe platforms
(not derive attention from scratch on a whiteboard).</p>

<p class="drill-intro"><strong>How to use it:</strong> For each question, practice a 35–45 minute
answer: clarify → draw the diagram → narrate the step-by-step path → deep-dive one risky area
(ACL, eval, side effects, cost) → list failure modes. Open a card, study it, then re-explain
from memory without looking.</p>

<figure class="diagram native">
<img src="../assets/diagrams/rag-detailed.svg" alt="RAG interview whiteboard overview" loading="lazy" />
</figure>

<p class="drill-intro">Related chapters: <a href="37-rag.html">RAG</a>,
<a href="39-agents.html">Agents</a>, <a href="38-memory.html">Memory</a>,
<a href="35-llms.html">LLMs</a>, <a href="42-ai-agent.html">Design an AI agent</a>.</p>

<ul class="lab-toc">
  <li><a href="#q1"><span>Q1</span> RAG company knowledge assistant</a></li>
  <li><a href="#q2"><span>Q2</span> Semantic / vector search at scale</a></li>
  <li><a href="#q3"><span>Q3</span> LLM evaluation pipeline</a></li>
  <li><a href="#q4"><span>Q4</span> Tool-using booking agent</a></li>
  <li><a href="#q5"><span>Q5</span> Content moderation cascade</a></li>
  <li><a href="#q6"><span>Q6</span> Embedding recommendations</a></li>
  <li><a href="#q7"><span>Q7</span> Live transcription + notes</a></li>
  <li><a href="#q8"><span>Q8</span> Multi-tenant AI SaaS</a></li>
  <li><a href="#q9"><span>Q9</span> Hallucination-resistant support</a></li>
  <li><a href="#q10"><span>Q10</span> Long-running assistant memory</a></li>
</ul>
"""
    # Add id anchors on each details via wrapping — qa_block doesn't support ids.
    # Post-process: inject id="qN" into details sequentially.
    blocks = ai_questions()
    out = []
    for i, block in enumerate(blocks, start=1):
        out.append(block.replace('<details class="qa">', f'<details class="qa" id="q{i}">', 1))
    return intro + "\n".join(out)


def ai_chapter_drills() -> dict[str, str]:
    """Deeper per-chapter drills pointing at the expanded lab."""
    return {
        "37-rag": drill_section(
            "Interview drill — RAG",
            "Practice the full whiteboard: ingest vs query, ACL in retrieval, abstain, eval.",
            [
                qa_block(
                    qnum=1,
                    title="Company knowledge chatbot (full design)",
                    asked="Google, Meta, Stripe, OpenAI-adjacent",
                    difficulty="Hard",
                    pattern="RAG",
                    prompt="Answer from private docs with citations and permissions.",
                    sections=[
                        (
                            "Step-by-step (short)",
                            steps(
                                [
                                    "Clarify ACL, freshness, latency, languages.",
                                    "Draw ingest (chunk→embed→index) separate from query.",
                                    "Hybrid retrieve + ACL filter + rerank + grounded generate.",
                                    "Abstain on low confidence; log traces for eval.",
                                ]
                            )
                            + figure_diagram("rag-detailed", "RAG detailed pipeline")
                            + "<p>Full solution with prompt skeleton and failure modes: "
                            "<a href=\"interview-ai.html#q1\">AI Lab Q1</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Chunking strategy deep-dive",
                    asked="Follow-up everywhere",
                    difficulty="Medium",
                    pattern="Ingestion",
                    prompt="How do you choose chunk size and boundaries?",
                    sections=[
                        (
                            "Answer",
                            steps(
                                [
                                    "Start 400–800 tokens with overlap; split on headings.",
                                    "Keep tables/code blocks intact when possible.",
                                    "Evaluate recall@k on a gold set — do not bike-shed forever.",
                                    "Store metadata (title, url, updated_at, acl) with every chunk.",
                                ]
                            ),
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="ACL-aware retrieval",
                    asked="Enterprise AI",
                    difficulty="Hard",
                    pattern="Security",
                    prompt="User must not see docs they cannot access.",
                    sections=[
                        (
                            "Answer",
                            "<p>Enforce ACL <em>inside</em> the retriever query (metadata filter / "
                            "partition). Post-hoc prompt instructions are not a control. Index "
                            "permission tags with vectors; test with adversarial users in eval.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Hybrid search",
                    asked="Search + AI",
                    difficulty="Medium",
                    pattern="BM25 + vectors",
                    prompt="When do keywords beat embeddings?",
                    sections=[
                        (
                            "Answer",
                            figure_diagram("hybrid-search", "Hybrid search")
                            + "<p>IDs, error codes, SKUs, rare proper nouns → BM25. Paraphrases → "
                            "dense. Fuse (RRF) then rerank. "
                            "<a href=\"interview-ai.html#q2\">Lab Q2</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Measuring RAG quality",
                    asked="Applied science / platform",
                    difficulty="Medium",
                    pattern="Eval",
                    prompt="What do you measure before shipping a retriever change?",
                    sections=[
                        (
                            "Answer",
                            "<p>Retrieval recall@k on gold questions, groundedness of answers, "
                            "citation accuracy, latency, cost. Separate retrieve vs generate "
                            "failures. <a href=\"interview-ai.html#q3\">Lab Q3</a>.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-ai.html",
        ),
        "39-agents": drill_section(
            "Interview drill — Agents",
            "Tool design + control loops win these interviews — not sci-fi autonomy.",
            [
                qa_block(
                    qnum=1,
                    title="Flight-booking agent",
                    asked="Google, Amazon, AI startups",
                    difficulty="Hard",
                    pattern="Tool loop",
                    prompt="Search and book with confirmation and budgets.",
                    sections=[
                        (
                            "Step-by-step (short)",
                            figure_diagram("agent-tools", "Agent tools")
                            + steps(
                                [
                                    "List tools with JSON Schema and auth scopes.",
                                    "Orchestrate plan→act→observe with session slots.",
                                    "Gate pay/book behind user confirm + server checks.",
                                    "Cap steps/tokens/$; idempotent side effects.",
                                ]
                            )
                            + "<p><a href=\"interview-ai.html#q4\">Full lab solution Q4</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Infinite tool loops",
                    asked="Follow-up",
                    difficulty="Medium",
                    pattern="Guardrails",
                    prompt="Agent keeps calling search forever.",
                    sections=[
                        (
                            "Answer",
                            bullets(
                                [
                                    "Max iterations and wall-clock timeout.",
                                    "Detect repeated identical (tool, args).",
                                    "Force finalize or escalate to user.",
                                    "Budget alarms in the gateway (Q8).",
                                ]
                            ),
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Prompt injection via tool output",
                    asked="Security-minded AI rounds",
                    difficulty="Hard",
                    pattern="Untrusted observations",
                    prompt="A webpage says to ignore policies and refund $10k.",
                    sections=[
                        (
                            "Answer",
                            "<p>Treat tool output as untrusted data, not instructions. Isolate "
                            "from system policy. Allowlist irreversible tools; enforce refunds "
                            "in code. Add injection cases to eval.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Human-in-the-loop",
                    asked="Enterprise agents",
                    difficulty="Medium",
                    pattern="Approvals",
                    prompt="When must a human approve?",
                    sections=[
                        (
                            "Answer",
                            "<p>Payments, deletes, external emails, production changes, anything "
                            "regulated or irreversible. Persist the approval artifact.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="When not to use an agent",
                    asked="Judgment check",
                    difficulty="Easy",
                    pattern="Product sense",
                    prompt="Interviewers love this.",
                    sections=[
                        (
                            "Answer",
                            "<p>If the workflow is a fixed state machine, ship software + RAG. "
                            "Use agents when tool choice truly branches and uncertainty is high.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-ai.html",
        ),
        "35-llms": drill_section(
            "Interview drill — LLMs in production",
            "Production LLM questions: context, decoding, structure, cost, eval.",
            [
                qa_block(
                    qnum=1,
                    title="Context window overflow",
                    asked="All AI product interviews",
                    difficulty="Medium",
                    pattern="Context management",
                    prompt="Conversation exceeds model context.",
                    sections=[
                        (
                            "Answer",
                            steps(
                                [
                                    "Summarize older turns; pin entities into working state.",
                                    "Retrieve long-term memory instead of full history.",
                                    "Truncate least relevant; larger windows are only one lever.",
                                ]
                            )
                            + "<p>See also <a href=\"interview-ai.html#q10\">Lab Q10 memory</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Structured output you can trust",
                    asked="Platform interviews",
                    difficulty="Medium",
                    pattern="JSON / schema",
                    prompt="Pipeline needs reliable JSON.",
                    sections=[
                        (
                            "Answer",
                            "<p>Constrained decoding / JSON schema; validate; retry with repair; "
                            "for critical paths prefer deterministic code over free-form LLM.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Eval before ship",
                    asked="OpenAI-adjacent / Google",
                    difficulty="Medium",
                    pattern="Offline gates",
                    prompt="How do you know a prompt change is safe?",
                    sections=[
                        (
                            "Answer",
                            figure_diagram("eval-pipeline", "Eval pipeline")
                            + "<p>Gold sets, rubrics, regression gates, online A/B. "
                            "<a href=\"interview-ai.html#q3\">Lab Q3</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Cost / latency routing",
                    asked="All companies",
                    difficulty="Medium",
                    pattern="Model routing",
                    prompt="Biggest model on every query is too expensive.",
                    sections=[
                        (
                            "Answer",
                            "<p>Router: small model for easy intents; large for hard; cache; "
                            "trim context; stream for UX; hard max tokens.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Temperature &amp; determinism",
                    asked="Applied ML",
                    difficulty="Easy",
                    pattern="Decoding",
                    prompt="When temperature 0 vs higher?",
                    sections=[
                        (
                            "Answer",
                            "<p>Low/0 for extraction and tool args; higher for brainstorming. "
                            "Even temp 0 is not perfectly deterministic across infra — say so.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-ai.html",
        ),
        "38-memory": drill_section(
            "Interview drill — Memory",
            "Tiered memory is how assistants feel personal without blowing the context window.",
            [
                qa_block(
                    qnum=1,
                    title="Long-running assistant memory",
                    asked="OpenAI, Google",
                    difficulty="Hard",
                    pattern="Tiered memory",
                    prompt="Remember preferences across months.",
                    sections=[
                        (
                            "Answer",
                            figure_diagram("memory-tiers", "Memory tiers")
                            + "<p><a href=\"interview-ai.html#q10\">Full lab Q10</a> — short-term, "
                            "working state, long-term facts, semantic recall, forget APIs.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Wrong memory",
                    asked="Follow-up",
                    difficulty="Medium",
                    pattern="Correction UX",
                    prompt="Assistant remembered the wrong hometown.",
                    sections=[
                        (
                            "Answer",
                            "<p>User-editable memory UI; overwrite/tombstone; prefer explicit "
                            "remember writes; confidence scores on inferred facts.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Privacy deletion",
                    asked="Enterprise / EU",
                    difficulty="Medium",
                    pattern="GDPR",
                    prompt="Delete all memory for a user.",
                    sections=[
                        (
                            "Answer",
                            "<p>Wipe SQL, vector points, cached summaries, and backups per policy; "
                            "audit the deletion.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Org vs user memory",
                    asked="B2B AI",
                    difficulty="Medium",
                    pattern="Tenancy",
                    prompt="Company playbook vs personal notes.",
                    sections=[
                        (
                            "Answer",
                            "<p>Separate stores and ACLs; never leak across tenants in retrieval "
                            "filters.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Summarization loss",
                    asked="Applied",
                    difficulty="Easy",
                    pattern="Compaction",
                    prompt="What do you lose when you summarize a thread?",
                    sections=[
                        (
                            "Answer",
                            "<p>Exact quotes, IDs, amounts — pin critical entities into structured "
                            "state before summarizing prose.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-ai.html",
        ),
        "36-prompting": drill_section(
            "Interview drill — Prompting &amp; grounding",
            "Judgment over poetry: structure, grounding, eval, versioning.",
            [
                qa_block(
                    qnum=1,
                    title="Support bot that must not hallucinate policy",
                    asked="Amazon, Shopify",
                    difficulty="Hard",
                    pattern="Grounded prompting",
                    prompt="Customer asks about refund windows.",
                    sections=[
                        (
                            "Answer",
                            figure_diagram("grounded-support", "Grounded support")
                            + "<p>Retrieve policy; cite; abstain if missing; actions via authz "
                            "tools. <a href=\"interview-ai.html#q9\">Lab Q9</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Few-shot vs fine-tune vs RAG",
                    asked="Applied LLM",
                    difficulty="Medium",
                    pattern="Adaptation",
                    prompt="When each?",
                    sections=[
                        (
                            "Answer",
                            bullets(
                                [
                                    "RAG for changing facts.",
                                    "Few-shot for format/style.",
                                    "Fine-tune for stable high-volume formats when prompting plateaus.",
                                ]
                            ),
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Jailbreak resistance",
                    asked="Trust &amp; safety",
                    difficulty="Medium",
                    pattern="Defense in depth",
                    prompt="User tries to override system rules.",
                    sections=[
                        (
                            "Answer",
                            "<p>Priority of system/developer messages; input/output filters; no "
                            "secrets in prompts; monitors — never \"pretty please\" alone.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Prompt versioning",
                    asked="Platform teams",
                    difficulty="Easy",
                    pattern="Ops",
                    prompt="How do teams manage prompts?",
                    sections=[
                        (
                            "Answer",
                            "<p>Version like code; eval on change; flag rollouts; trace which "
                            "version produced each answer.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Showing chain-of-thought",
                    asked="Google-style",
                    difficulty="Medium",
                    pattern="UX + privacy",
                    prompt="Should users see raw CoT?",
                    sections=[
                        (
                            "Answer",
                            "<p>Usually no — show short justifications; scrub private data; prefer "
                            "structured rationales.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-ai.html",
        ),
        "42-ai-agent": drill_section(
            "Interview drill — Capstone AI design",
            "Combine RAG, tools, memory, eval, and tenancy into one coherent story.",
            [
                qa_block(
                    qnum=1,
                    title="End-to-end AI assistant",
                    asked="Staff / senior AI design",
                    difficulty="Hard",
                    pattern="Full stack AI",
                    prompt="Design the production assistant.",
                    sections=[
                        (
                            "Answer",
                            figure_diagram("ai-assistant", "AI assistant")
                            + steps(
                                [
                                    "Gateway: auth, quota, tracing.",
                                    "Router: chat vs RAG vs agent tools.",
                                    "Memory + retrieval with ACL.",
                                    "Guardrails + HITL for irreversible actions.",
                                    "Offline eval gates + online metrics.",
                                ]
                            )
                            + "<p>Drill the pieces in "
                            "<a href=\"interview-ai.html\">AI Lab Q1, Q4, Q8, Q10</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Multi-tenant cost controls",
                    asked="B2B",
                    difficulty="Medium",
                    pattern="Quotas",
                    prompt="Tenants share model capacity.",
                    sections=[
                        (
                            "Answer",
                            figure_diagram("multi-tenant-ai", "Multi-tenant AI")
                            + "<p><a href=\"interview-ai.html#q8\">Lab Q8</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Observability",
                    asked="Senior rounds",
                    difficulty="Medium",
                    pattern="Tracing",
                    prompt="What do you log?",
                    sections=[
                        (
                            "Answer",
                            "<p>request id, prompt version, retrieved doc ids, tool calls, token "
                            "counts, latency, cost, feedback — redact PII.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Streaming UX",
                    asked="Product + eng",
                    difficulty="Easy",
                    pattern="SSE",
                    prompt="Stream tokens safely.",
                    sections=[
                        (
                            "Answer",
                            "<p>SSE from gateway; cancel on disconnect; buffer tool JSON until "
                            "valid; backpressure.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Moderation in the assistant",
                    asked="Trust",
                    difficulty="Medium",
                    pattern="Cascade",
                    prompt="User pastes disallowed content.",
                    sections=[
                        (
                            "Answer",
                            figure_diagram("moderation-cascade", "Moderation")
                            + "<p><a href=\"interview-ai.html#q5\">Lab Q5</a>.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-ai.html",
        ),
        "40-mcp": drill_section(
            "Interview drill — MCP / tool protocols",
            "Protocols, trust boundaries, and tool retrieval — not buzzword bingo.",
            [
                qa_block(
                    qnum=1,
                    title="Why a tool protocol exists",
                    asked="AI platform interviews",
                    difficulty="Medium",
                    pattern="Interoperability",
                    prompt="Why not hardcode every integration?",
                    sections=[
                        (
                            "Answer",
                            "<p>Standard schemas let many hosts talk to many servers; auth and "
                            "discovery become shared; agents retrieve tools instead of mega-prompts.</p>"
                            + figure_diagram("mcp", "MCP"),
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Trust boundary",
                    asked="Security",
                    difficulty="Hard",
                    pattern="Least privilege",
                    prompt="Third-party tool server is compromised.",
                    sections=[
                        (
                            "Answer",
                            bullets(
                                [
                                    "Scoped tokens per server; user consent.",
                                    "Sandbox; allowlist sensitive tools.",
                                    "Treat returned content as untrusted.",
                                    "Audit every invocation.",
                                ]
                            ),
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Tool overload",
                    asked="Applied agents",
                    difficulty="Medium",
                    pattern="Retrieval over tools",
                    prompt="200 tools destroy accuracy.",
                    sections=[
                        (
                            "Answer",
                            "<p>Retrieve top relevant tool schemas per turn; hierarchical "
                            "routers; tight descriptions.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Idempotent tools",
                    asked="Platform",
                    difficulty="Medium",
                    pattern="Reliability",
                    prompt="Agent retries a side-effecting tool.",
                    sections=[
                        (
                            "Answer",
                            "<p>Idempotency keys in the contract; servers dedupe; agents pass "
                            "stable keys from session+step.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Local vs remote tools",
                    asked="Desktop agents",
                    difficulty="Easy",
                    pattern="Deployment",
                    prompt="Filesystem tool vs cloud API.",
                    sections=[
                        (
                            "Answer",
                            "<p>Local: permission prompts + path sandbox. Remote: OAuth, rate "
                            "limits, residency. Same schema, different policy.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-ai.html",
        ),
    }
