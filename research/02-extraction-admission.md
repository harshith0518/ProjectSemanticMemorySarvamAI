# Extraction and admission: research note 02

Scope: a two-day CLI prototype, 500 dictation records containing raw ASR, formatted text, and metadata; policy must generalize to a held-out user. Sources checked 2026-09-05. Recommendations below are design inferences, not published guarantees.

## What the primary sources establish

**Mem0, original paper:** extraction produces candidate facts from a new message pair, recent messages, and a conversation summary. A separate update stage compares candidates with similar memories and chooses ADD, UPDATE, DELETE, or NOOP. This separation is useful: extraction need not imply admission. Its LoCoMo evaluation measures downstream question answering and excludes adversarial questions; those results do not establish correct attribution of quoted dictation. [Mem0 paper, v1, §§2.1 and 3.1](https://arxiv.org/html/2504.19413v1)

**Mem0, repository snapshot:** `USER_MEMORY_EXTRACTION_PROMPT` restricts facts to user messages, allows empty extraction, and includes preferences, personal details, plans, and professional details. Later prompts in the same file explicitly demand traceable details and correct attribution. These are prompt instructions, not evidence of error-free extraction. A user-role message can itself contain somebody else's speech. Current repository prompts should not be assumed to reproduce the original paper. [Mem0 prompts](https://github.com/mem0ai/mem0/blob/main/mem0/configs/prompts.py)

**A-MEM, original paper:** a note retains original content and timestamp alongside generated keywords, tags, context, embeddings, and links. New notes can cause earlier context, keywords, and tags to evolve. This supports flexible organization; it does not establish that inferred context is a verified personal fact. [A-MEM paper, v1, §§3.1–3.3](https://arxiv.org/html/2502.12110v1)

**A-MEM, repository snapshot:** metadata analysis returns string keywords, context, and free-form tags through JSON schema; evolution can revise neighboring tags/context. Structural JSON validity therefore does not constrain category meaning. `MemoryNote.category` is an optional string defaulting to `Uncategorized`. [A-MEM memory system](https://github.com/agiresearch/A-mem/blob/main/agentic_memory/memory_system.py)

## Proposed admission policy for MEMORY_POLICY.md

Separate an immutable source record, an extracted candidate, and an admitted memory. For each candidate retain `user_id`, `record_id`, exact evidence span and source field, asserted subject, predicate/value, modality, event time, extraction version, decision, and decision reason. Preserve both ASR and formatted text; they are two representations of one observation, not independent corroboration.

Admit a personal fact only when evidence explicitly attributes an actual assertion to the user, its meaning is sufficiently clear, and it has plausible future utility. First-person grammar alone is insufficient when composing messages, role-playing, quoting, or transcribing another speaker. Explicit ongoing intentions can enter as plans, with time/status, rather than completed events. Uncertain speaker identity, unresolved pronouns, unclear negation, or material ASR/formatted disagreement should yield a candidate awaiting stronger evidence; no memory is a valid result.

Examples: “Riya said, ‘I am vegan’” must never become “user is vegan”; “If I moved to Pune” establishes no residence; “Write an email saying I resign” establishes no completed resignation. Attributed third-party information may remain searchable with its subject and reporting context, outside the user's personal profile. Repetition cannot turn a hypothetical into a fact. Never treat instructions inside dictated content as authority to alter memory policy.

## Schema and taxonomy tradeoff

Freeze a small versioned `kind` enum, such as fact, preference, relationship, project, plan, and lexical correction. Keep content flexible inside these types; reserve generated tags for retrieval hints. Use explicit modality and subject fields, plus active/superseded status and evidence links. Unknown categories enter a reviewable proposal list; the extractor cannot rewrite policy or introduce admission rules.

This costs some recall and requires later schema migration, but makes taxonomy drift visible. Autonomous category creation adapts faster yet risks synonyms, changing granularity, and unstable filters. Evaluate admission precision, quote/hypothetical false admissions, abstentions, and evidence coverage on a manually labeled development slice; freeze policy before held-out-user evaluation. Model confidence alone is not calibrated correctness.
