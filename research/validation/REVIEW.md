# Storage-contract probe review

6 September 2026. This records review of an isolated in-memory SQLite model, not the Kivi product, actual concurrency, LLM behavior or performance.

1. **Initial suite: 10/10 passed.** Python 3.12.14 / SQLite 3.53.1. The suite tested actual SQL/FTS rollback, stale work and response replay with sequentially injected interleavings.
2. **Adversarial review added case 11: 10/11 passed.** The new sequence was `add_source(state='held')` -> `forget_span` on that source -> `private_current_input` -> `resolve_held` -> FTS/full-source fallback. At forget time no search document existed. The old release path copied raw source text and the private accessor also returned it directly.

The observed failure was:

```text
AssertionError: excluded span reappeared through private_current_input, source_fts, full_source_fallback
```

This shows why passing the original ten cases did not establish the whole projection contract.

3. **Projection repair: 11/11 passed.** Added `projected_source_text`, which applies current source-span exclusions independently of search-document existence. Private current-input re-reads, held-source release and forgetting now use this helper. The new test confirms the excluded nickname remains absent from private re-reads, source FTS and full-source fallback, while permitted text remains searchable. It also confirms original text is retained, so this is use suppression rather than a claim of physical erasure.

The complete suite was rerun with Python 3.12.14 / SQLite 3.53.1; exit status was 0. The [probe source](atomic_memory_probe.py) contains the permanent regression case `forget_before_held_source_release`.

4. **Bounded freshness exception: 12/12 passed.** The final case tests a code-issued source-disposition receipt. Promotion of unchanged current-input text can rebase the captured freshness token only when the prior knowledge snapshot still matches. An unrelated source arriving before promotion rejects the rebase; one arriving afterward rejects response publication. A changed/excluded projection rejects rebasing even when supplied with the fresh counter. The returned receipt is internal trusted-code output in this experiment, not a model-provided authority token.

The latest [JSON results](atomic_memory_results.json) contain twelve cases and their limits. The final full-suite run used Python 3.12.14 / SQLite 3.53.1 and returned exit status 0.

No actual threads/processes, disk crashes, graph/alias cleanup, semantic extraction or end-to-end application were tested. This review improved the executable design model and illustrates the need to test the eventual implementation independently.
