# Uncertainty, clarification and abstention

[← Guide overview](README.md) | [Next work](10-next.md)

**Status:** Planned · product implementation pending. Snapshot: 6 September 2026.

**What happens when memory is missing or ambiguous?**

Answer the supported part, ask only when the missing detail matters, and admit when the history cannot establish an answer.

```mermaid
flowchart LR
  n0["Check evidence sufficiency"]
  n1["Identify material uncertainty"]
  n2["Answer / ask / qualify / abstain"]
  n0 --> n1 --> n2
```

## Step by step

1. **Enough evidence** Answer directly and make supporting sources available.

2. **An unnecessary detail is unknown** Omit that detail and complete the supported task.

3. **An important distinction is missing** Ask one focused question or show supported alternatives. A reversible draft may use a clearly stated assumption.

4. **History contains no answer** Explain what is missing. Do not invent a fact or ask a question merely to avoid acknowledging the gap.

## Example

If “that trip” could mean Jaipur or Goa and the budgets differ, clarify the trip. If the history never names a booked hotel, say that no booking is established.

## Remaining work and decisions

- Implement answer, clarification, partial-result and abstention states.
- Design simple handling for skipped questions and failed actions.
- Measure both unsupported answers and unnecessary abstention.

<details>
<summary>Technical details — open when needed</summary>

- Skipping a clarification is not confirmation; preserve the uncertainty and take the supported fallback.
- Background ingestion should not interrupt the user for every ambiguity. Revisit it when a request actually needs the distinction.
- An LLM's self-reported confidence percentage is not a calibrated probability.
- A missing target or authority blocks the dependent external action, even when a useful draft can still be prepared.

</details>

## Related processes

- [03 · Entity relationships and temporal updates](03-entities-time.md)
- [04 · Retrieval and evidence selection](04-retrieval.md)
- [05 · Context application and personalization](05-context.md)
- [08 · Backend and application integration](08-application.md)

Canonical reference: [ARCHITECTURE.md](../ARCHITECTURE.md), Section 0.4 and sections 7–9.

[← Context application and personalization](05-context.md) · [Correction, forgetting and user control →](07-controls.md)
