# Evaluation and observability

[← Guide overview](README.md) | [Next work](10-next.md)

**Status:** Planned · product implementation pending. Snapshot: 6 September 2026.

**How will we know that the system works?**

Run the real pipeline on varied history, inspect its decisions and measure whether added memory actually improves supported outcomes.

```mermaid
flowchart LR
  n0["Corpus and reviewed questions"]
  n1["Run comparable pipelines"]
  n2["Inspect evidence and failures"]
  n3["Freeze, evaluate and reproduce"]
  n0 --> n1 --> n2 --> n3
```

## Step by step

1. **Prepare realistic cases** Create approximately 500 paired transcript records with recurring people and events, contradictions, missing metadata and multilingual examples.

2. **Compare useful baselines** Compare full permitted history where it fits, keyword source search, optional hybrid source search and hybrid search with typed memories.

3. **Inspect every layer** Trace source input, extraction/admission, retrieved evidence, corrections and final behavior. Measure unsupported claims, missed evidence, abstention, personalization, actual tool outcomes, latency, database size and usage.

4. **Separate tuning from final proof** Tune on development cases, freeze the candidate, then evaluate held-out cases. Preserve failures and test the documented clean-checkout review procedure.

## Example

A fluent answer fails if it uses the wrong person's budget, relies on a superseded value, cites irrelevant text or retrieves information the user forgot.

## Remaining work and decisions

- Build the corpus, reviewed questions and reproducible evaluation runner.
- Run real application integrity tests and measure quality, latency and cost.
- Produce evaluation results, setup/reset instructions and a clean-checkout rehearsal.

<details>
<summary>Technical details — open when needed</summary>

- Current evidence is only an isolated SQLite contract experiment: 12/12 checks passed. It does not prove semantic accuracy, real concurrency, disk recovery, model reliability or performance.
- Proposed protocol: 80 reviewed questions, split 30 development / 50 sealed; an additional 50-source extraction audit, split 20 / 30. Separate whole narratives/templates and keep gold labels out of ingestion.
- Integrity cases include repeated imports, restart/retry, stale workers, current corrections, forgetting during generation, scope violations, hostile historical instructions and uncertain tool outcomes.
- The final submission needs a real normal-user UI/backend, schema/migrations, seed data, corpus, results, README with AI-use disclosure, RUN.md, an environment example, another-corpus import and a tested reset procedure.
- Admission, quality, latency and cost thresholds in the main architecture are proposed, unachieved gates. Small evaluation samples do not establish universal reliability.

</details>

## Related processes

- [01 · Memory extraction and admission](01-learning.md)
- [04 · Retrieval and evidence selection](04-retrieval.md)
- [07 · Correction, forgetting and user control](07-controls.md)
- [08 · Backend and application integration](08-application.md)
- [Next · What to do next](10-next.md)

Canonical reference: [ARCHITECTURE.md](../ARCHITECTURE.md), Sections 12 and 14–16.

[← Backend and application integration](08-application.md) · [What to do next →](10-next.md)
