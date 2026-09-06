# Temporal graphs for Kivi memory

Research checked 5 September 2026. Recommendation: adopt temporal graph semantics, but start with a relational fact store plus hybrid retrieval. A dedicated graph database is optional at approximately 500 records; it should earn its integration cost through measured retrieval improvements.

## Source findings

The Zep paper separates raw episodes, semantic entities/facts, and community summaries. Facts retain links to source episodes and four timestamps: when the fact became valid, stopped being valid, was recorded, and was expired. Relative dates use the episode timestamp. Retrieval combines semantic similarity, BM25, and graph traversal. These are useful architectural ideas; the vendor-authored evaluation does not establish superiority on noisy Hindi/Hinglish ASR. Its reported latency improvements compare against long full-context prompts, so they do not isolate the benefit of a graph database. [Zep paper, sections 2–4](https://arxiv.org/html/2501.13956v1)

Current Graphiti entity resolution first retrieves candidates using name embeddings, then applies deterministic similarity and LLM deduplication; unresolved entities remain separate. The inspected code uses a candidate limit of 15 and cosine threshold of 0.6. These are implementation settings, not calibrated multilingual identity guarantees. Its current candidate pipeline differs from the paper's hybrid-search description. [Entity resolution implementation](https://github.com/getzep/graphiti/blob/main/graphiti_core/utils/maintenance/node_operations.py)

Edge processing distinguishes duplicates from contradiction candidates. Temporal resolution preserves nonoverlapping facts and can close an older fact's validity at a newer fact's start time. Newly ingested historical information can itself be expired when a later contradictory fact is already known. The code's expiry logic depends on available, strictly ordered validity timestamps; missing or equal dates do not automatically resolve every conflict. [Edge resolution implementation](https://github.com/getzep/graphiti/blob/main/graphiti_core/utils/maintenance/edge_operations.py)

Graphiti depends on reliable structured LLM output and supports multiple database backends. Its README currently deprecates Kuzu and recommends Neo4j or FalkorDB for new projects. Pin a tested release: current `main`, the paper, and hosted Zep should not be assumed behaviorally identical. [Official repository](https://github.com/getzep/graphiti)

## Architecture implications — engineering inference

- Preserve each record's raw ASR and formatted text under one immutable episode ID. They are two representations of one source, not independent corroboration. Every assertion needs source record IDs and quoted evidence spans; retain conflicting representations.
- Use tables for `episodes`, `entities`, `aliases`, `assertions`, and `assertion_sources`. Assertions should carry subject, predicate, object/value, event-time bounds, ingestion time, source, extraction version, status, and `supersedes_id`. Separate unknown dates from known timestamps; retain the original temporal phrase.
- Distinguish a real change (“moved to Delhi”) from a correction (“I said Delhi, but meant Pune”). A change closes a previously true interval; a correction retracts an erroneous assertion while retaining its audit trail. Latest ingestion alone must not decide truth.
- Resolve Hindi script, Latin transliterations, abbreviations, and ASR variants with conservative alias candidates. Require contextual identity evidence before merging; keep uncertain identities separate. A mistaken merge contaminates every connected fact.
- Handle mutually exclusive predicates with explicit conflict groups. Parallel compatible facts must coexist. Return current facts by default, historical facts for temporal questions, and abstain or expose alternatives when evidence cannot resolve a conflict.
- Precompute extraction and embeddings during ingestion. Retrieve both passages and facts with lexical plus multilingual vector search; optionally expand one or two entity hops using indexed SQL joins. Return evidence with answers. Evaluate correction accuracy, source fidelity, unsupported-answer rate, multilingual alias errors, and query/ingestion latency separately.

For the two-day CLI, defer communities and a graph service. Add Graphiti/Neo4j only if an ablation shows repeated multi-hop questions materially benefit beyond these simpler tables and retrieval paths.
