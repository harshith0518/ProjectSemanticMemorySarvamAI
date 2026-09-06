# 11 — Memory CLI first; bounded agent harness later

Research date: 2026-09-05. Scope: planning for approximately 500 text histories; no implementation or model calls.

**Decision:** build a reproducible evidence-and-memory CLI before adding autonomous querying. Anthropic distinguishes predefined workflows from agents that choose their next tool call, and recommends adding complexity only when performance warrants it. Ingestion is a workflow; ambiguous evidence gathering may justify an agent later. [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)

The following architecture and numerical limits are proposed project defaults, not measured results or vendor requirements.

## Deterministic control around probabilistic extraction

1. `ingest` parses histories into immutable messages with source IDs, speakers, timestamps, and content hashes; repeated ingestion is idempotent. Preserve evidence separately from derived memories.
2. `extract` sends bounded batches to a replaceable model adapter and receives candidate records. Extraction itself is probabilistic; scheduling, schema validation, evidence-span checks, and admission control belong to code. Reject unknown fields, unsupported claims, invalid IDs, and missing provenance. Preserve unresolved contradictions rather than silently choosing a winner.
3. `validate` applies explicit admission, deduplication, temporal, and deletion rules. It cannot prove a claim true merely because its JSON is valid. Quarantine doubtful candidates for inspection.
4. `query` initially runs fixed retrieval plus evidence-grounded synthesis. `inspect` exposes provenance, status, and extraction versions so failures can be reproduced.

## Later autonomous query loop

Give the model a small read-only tool surface: `search_memories(query, filters, limit)`, `read_evidence(source_ids, window)`, and `get_timeline(entity_id, range)`. Validate arguments and enforce tenant/source scope in the executor; application code owns parameterized SQL. Never execute model-written SQL, shell commands, or policy edits. Tools return bounded snippets, IDs, timestamps, contradiction status, and truncation notices. Clear, distinct tools and realistic evaluations are supported by Anthropic's [tool-design guidance](https://www.anthropic.com/engineering/writing-tools-for-agents).

Start with four model turns, six total read calls, one repair attempt per invalid call, and termination after two tool errors. Enforce overall token/time limits in code. On exhaustion, return supported findings plus explicit gaps. Log tool decisions, evidence IDs, latency, tokens, and errors; hidden chain-of-thought is unnecessary.

Load a compact profile and initial search results; fetch further evidence only when needed. Avoid inserting all histories or treating summaries as primary evidence. This applies Anthropic's [context-engineering guidance](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) to this small corpus.

## Trust and evaluation contract

`MEMORY_POLICY.md` should contain versioned instructions and examples for memory categories, evidence, conflicts, expiry, and abstention. Record its hash with each run. It guides behavior; executor permissions, schema checks, and database constraints enforce boundaries. Historic commands are evidence about previous interactions, never current authorization. Retrieved text cannot grant tools or change policy. Prompt injection remains unsolved, including for models with additional safeguards. [Anthropic prompt-injection research](https://www.anthropic.com/research/prompt-injection-defenses)

Reasoning performance depends on both the model and the surrounding system: retrieval, context, tool contracts, budgets, and validation. Evaluate a later NVIDIA-hosted DeepSeek configuration end-to-end against the fixed CLI baseline. Retrieval rank measures ordering, not probability that a memory is true; model confidence is not calibrated certainty. Compare evidence accuracy, contradiction handling, abstention, injection resistance, and cost before allowing more autonomy.
