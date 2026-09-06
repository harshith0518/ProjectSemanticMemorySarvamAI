# Kivi memory research dossier

Prepared 5 September 2026. Fifteen separately assigned research reviews cover personal memory, retrieval, data systems, ML evaluation, and agent design. The environment supports three concurrent subagents, so the assignments ran in batches. The primary agent reviewed the findings and wrote the synthesis.

## Read in this order

1. [Consolidated project plan and architecture](../ARCHITECTURE.md): the single fresh-start reference, including product intent, assignment requirements, stack, categories/storage, workflow contracts, evaluation, submission and open decisions. It takes precedence over earlier plans.
2. [Five product questions](PRODUCT_QUESTIONS.md): supporting discussion of the user's ideas, Kivi feature verification, clarification, implicit personalization, external actions and NVIDIA preference; its relevant decisions are now included in the consolidated plan.
3. [Earlier end-to-end design](END_TO_END_DESIGN.md) and [architecture proposal](ARCHITECTURE_PROPOSAL.md): additional examples and research background; their runtime contracts are refined by the canonical blueprint.
4. The focused research notes below for evidence, alternatives and limitations.

The final refinement added three independent current-source reviews: [memory and ontology](blueprint-research-memory.md), [storage and cache](blueprint-research-storage.md), and [workflow contracts](blueprint-research-workflow.md). See [validation history](validation/REVIEW.md) for the isolated SQL experiment: initial checks, a reproduced held-source-forget failure, its fix, and final 12/12 passing contract probes. These are not product/LLM/performance results.

Three independent reviews support the 6 September synthesis: [storage and consistency](design-review-storage.md), [evaluation protocol](design-review-evaluation.md), and [harness and tools](design-review-harness.md). They add to the original fifteen research assignments. Their thresholds and scenarios are proposed, not implemented or measured.

These are planning artifacts plus an isolated executable storage-contract experiment. No application, model integration, or performance benchmark was implemented. The user will supply the NVIDIA API key during development. Proposed product commands and model choices are not verified running software. The final assignment still requires a normal-user interface beyond the intermediate CLI.

## Research assignments

| # | Focus | Note |
|---|---|---|
| 1 | Graphiti/Zep, temporal graphs, entity resolution | [Temporal graphs](01-temporal-graphs.md) |
| 2 | Mem0/A-MEM, extraction, attribution, admission and taxonomy | [Extraction and admission](02-extraction-admission.md) |
| 3 | Exact lexical/dense retrieval, RRF, reranking and source coverage | [Hybrid retrieval](03-hybrid-retrieval.md) |
| 4 | MemGPT, RAPTOR, recency, hierarchy and cache invalidation | [Hierarchy and caching](04-hierarchy-cache.md) |
| 5 | LaMP, PrefEval, implicit personal context and unwanted callbacks | [Personalization](05-personalization.md) |
| 6 | Selective clarification, safe fallback and abstention | [Clarification](06-clarification.md) |
| 7 | LongMemEval/LoCoMo, baselines, leakage controls and metrics | [Evaluation](07-evaluation.md) |
| 8 | Forgetting, deletion, evidence, exclusions and prompt injection | [Forgetting and trust](08-forgetting-trust.md) |
| 9 | SQLite/FTS5, pgvector, transactions and import recovery | [Storage](09-storage.md) |
| 10 | Hindi/Hinglish, E5, BGE-M3, Unicode and NVIDIA embeddings | [Multilingual retrieval](10-multilingual.md) |
| 11 | Deterministic workflows, bounded agents and tool contracts | [Agent harness](11-agent-harness.md) |
| 12 | Current OSS licenses, source/hosted disparities and reuse decisions | [Open-source choices](12-oss-choices.md) |
| 13 | Data-system design literature and independent architecture critique | [Data-system review](13-data-system-design.md) |
| 14 | ML-system design literature and independent architecture critique | [ML-system review](14-ml-system-design.md) |
| 15 | Agent-system design literature and independent architecture critique | [Agent-system review](15-agent-system-design.md) |

## How to interpret this research

- **Documented feature:** a capability or contract found in official documentation or inspected code. It does not prove reliability on our corpus.
- **Published finding:** an author's reported experimental result. Its dataset, model, version and evaluation matter.
- **Design inference:** our proposed application of those ideas under this assignment's constraints. It must be evaluated before being called better.
- **Unverified:** native Kivi app interaction, NVIDIA account quotas and live model behavior, local embedding speed, actual hidden-data metadata, and user acceptance of spontaneous personalization.

The public Kivi site was inspected; no installed native-app walkthrough was performed. A built-in chat-project interface was not confirmed. That distinction matters because other Sarvam products expose different workspaces.

The user asked for complete system-design, ML-system-design and agent-system-design books. We reviewed accessible author/publisher material, relevant chapters, short book material and primary papers. We did not read entire unspecified commercial books or all literature in these fields. Each book-review note states its actual scope. No whole-book mastery or exhaustive market coverage is claimed.

Recent preprints are marked as preliminary where used. Citation links point to primary sources; current repository behavior may differ from an earlier paper. Vendor leaderboard numbers have not been used as proof that a particular database or memory product will win this assignment.

This dossier supports understanding and technical planning. It is not a substitute for the applicant's independently written Part One position and vision.
