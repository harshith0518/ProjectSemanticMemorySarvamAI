# 07 — Evaluation plan

**Recommendation:** evaluate admission, retrieval, and grounded answers separately using a small, sealed, manually reviewed dictation suite. The 500 development records are source material, **not 500 independent tests**. An unseen single-user corpus cannot establish generalization across users.

## Evidence and applicability

- [LongMemEval, ICLR 2025](https://arxiv.org/html/2410.10813v2) provides 500 curated questions covering extraction, multi-session reasoning, temporal reasoning, updates, and abstention. It separates answer grading from evidence Recall@k/NDCG@k. Borrow this decomposition; its generated chat histories differ from noisy dictation.
- [LoCoMo, ACL 2024](https://aclanthology.org/2024.acl-long.747/) uses generated, human-verified long conversations for QA, event summarization, and dialogue generation. Borrow temporal and cross-record probes; its scores do not validate Hindi/Hinglish ASR handling.
- [LOCOMO-CONV, September 2026 preprint](https://arxiv.org/abs/2609.03467) tests dialog, implicit, counterfactual, and composed queries, finding retrieval gaps and useful personalization without explicitly repeating remembered facts. This motivates incidental-use tests; the very recent findings remain preliminary.
- [LongMemEval-V2, May 2026 work in progress](https://arxiv.org/abs/2605.12493) evaluates environment experience, premise awareness, and accuracy/latency tradeoffs. Its web-agent setting is less directly applicable; borrow false-premise checks, not headline accuracy targets.

## Local suite and leakage controls

After inspecting the corpus, target 80 human-reviewed probes across direct facts, cross-record reasoning, dates, corrected facts, unknown/conflicted facts, and incidental personalization. Report actual counts and unsupported categories rather than manufacturing coverage. Each probe needs a query timestamp, acceptable answer/rubric, supporting record IDs and spans, and answerability label.

Use approximately 30 development and 50 sealed probes, grouping shared evidence episodes and paraphrases together. Ingest only records available before each query. Freeze prompts, thresholds, and configuration before opening sealed answers; reset stores between runs. Earlier history may support later queries, but no future records or gold answers enter extraction/indexing. Keep generated probes and noise perturbations in a separately reported stress suite; never let the answering model write its own gold labels. Development results remain development results even after a local holdout.

Inspect raw ASR against formatted text: formatting is not automatically factual ground truth. Include Hindi, Romanized Hindi, Hinglish, aliases, negation, and naturally occurring ASR errors where present. Bilingual human review resolves meaning and scorer disagreement; token overlap alone is inadequate.

## Comparisons and measurements

Hold answer model, prompt, and retrieval token budget fixed. Compare no memory, full available history (only when it fits; disclose truncation), BM25 over original records, and proposed hybrid retrieval with admitted facts plus source evidence. Use gold-evidence input as a diagnostic reader ceiling. Ablate admission filtering, temporal supersession, lexical retrieval, and formatted-only versus paired-source indexing one at a time.

- **Admission:** annotate candidate facts independently of extraction; report precision/recall, unsupported writes, wrong subject, rejected valid facts, and mistaken updates.
- **Retrieval:** evidence Recall@1/5/10 plus fraction retrieving *all* required evidence; deduplicate by source record and disclose token budget.
- **Answers:** per-category correctness, claim-level citation support and citation completeness; separate right-answer/wrong-evidence failures.
- **Updates/abstention:** current and historical-state accuracy, stale-answer rate, false answers on unknowns, false abstentions, and accuracy versus answered coverage.
- **Personalization:** blind paired review against no memory for useful contextual adaptation and irrelevant/invented personalization.
- **Operations:** ingestion and query p50/p95 latency separately; cold/warm runs, timeout/error rate, tokens, calls, and cost per 500-record ingest/per query. Report sample counts and paired uncertainty; tiny samples do not justify p99 claims.

**Two-day priority:** day one labels and baselines; day two sealed comparisons, critical ablations, and an error ledger. Select the simplest configuration with supported gains; predeclare acceptance criteria before scoring.
