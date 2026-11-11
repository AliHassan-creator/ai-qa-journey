# QA-Copilot Prompt Library

Prompts are plain Markdown so they can be reviewed and versioned with Git. Each prompt defines its task, source-of-truth inputs, constraints, output contract, and human-review boundary.

## Five prompts

1. [`testcase_gen.md`](testcase_gen.md) — create traceable manual test-case drafts from stories and acceptance criteria.
2. [`ambiguity_finder.md`](ambiguity_finder.md) — turn vague or conflicting requirements into answerable questions.
3. [`test_data_generator.md`](test_data_generator.md) — create synthetic partition/boundary data only from stated constraints.
4. [`risk_prioritizer.md`](risk_prioritizer.md) — rank supplied cases from evidence and keep human overrides explicit.
5. [`bug_report_writer.md`](bug_report_writer.md) — turn observed notes into a factual bug-report draft.

[`ai_output_review_checklist.md`](ai_output_review_checklist.md) is the shared eight-point review checklist used across prompt outputs; it is a companion guardrail, not a sixth generation prompt.

## Change discipline

- Make prompts small, task-specific, and diffable.
- Change one prompt behavior at a time and inspect the resulting diff.
- Keep sample inputs synthetic and non-sensitive.
- Record prompt changes with examples and tests where output has a machine-readable contract.
- Never treat a prompt instruction as a security boundary or replace human review with model confidence.
