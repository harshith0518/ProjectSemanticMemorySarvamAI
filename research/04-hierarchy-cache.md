# 04 — Hierarchy, recency, and caching

For roughly 500 dictation records and a two-day CLI build, use a shallow semantic hierarchy over durable records, plus a bounded context selection policy. A hierarchy organizes meaning; a cache reuses previously computed or loaded data. Neither requires discarding older records. Recommendations below are engineering judgments for Kivi, not findings established on this dataset.

**What the research supports.** MemGPT separates the model's limited prompt context from external storage. Its working context holds important facts, a FIFO queue holds recent messages, and search brings older material back into context. This supports a small active-memory layer backed by searchable originals; it does not establish that Kivi needs an autonomous memory-management agent. [MemGPT, §2](https://arxiv.org/html/2310.08560v2)

Generative Agents ranks memories using normalized relevance, importance, and recency. Its recency measures time since *last retrieval*, with exponential decay; this differs from the age of the underlying event. Copying that policy can create a feedback loop where repeatedly retrieved memories remain prominent. Its equal weights and game-hour decay are experimental choices, not universal defaults. [Generative Agents, §4.1](https://arxiv.org/html/2304.03442v2)

RAPTOR recursively clusters and summarizes text, then retrieves original passages and summaries at different abstraction levels. Its chosen retrieval strategy searches across all levels, demonstrating that hierarchical representation need not force a strict root-to-leaf route. Its document-QA results do not directly validate personal dictation memory. [RAPTOR, §3–4](https://arxiv.org/html/2401.18059v1)

**Concrete options.**

- **Recommended baseline:** retain canonical transcripts; ask the LLM for a few reusable category labels and optional subcategories; permit multiple labels per record. Search all originals, treating categories as filters or ranking hints. Assemble context from highly relevant records, a small recent slice, and explicitly pinned durable facts, deduplicated within a token budget. Start without a persistent query cache: 500 records alone does not demonstrate a retrieval bottleneck.
- **Small extension:** create one summary per category or active project, with source record IDs. Retrieve summaries and originals together; expand a summary to its sources for exact details. Add another hierarchy level only if evaluation reveals questions that need broader synthesis.
- **Later option:** a RAPTOR-style recursive tree when the corpus and cross-record synthesis justify its construction and maintenance costs. Research specifically identifies updates to clustered hierarchies as a complication for dynamic datasets. [Recursive Abstractive Processing for Retrieval in Dynamic Datasets](https://arxiv.org/abs/2410.01736)

**Freshness policy.** Assign every record a stable ID and revision. Corrections replace the active revision, regenerate its labels/embedding, invalidate dependent summaries, and purge cached contexts containing it. Deletion excludes the record immediately and invalidates every derived artifact, including pinned facts. Until summaries rebuild, retrieve originals. At this size, invalidating all query results on every corpus mutation is a reasonable simplification; TTL alone cannot guarantee freshness.

Recency should break relevance ties or provide a modest boost, not exclude old evidence. Keep event time, ingestion time, correction time, and access time separate: editing an old event does not make it recent. Evaluate an old exact match against recent distractors, corrected facts, deleted sources, and cross-category queries before tuning weights or adding cache layers.
