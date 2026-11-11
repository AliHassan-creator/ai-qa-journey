# Prompt: Raw Notes to Bug Report

## Purpose

Turn verified observations into a clear, reproducible bug-report draft without inventing steps or claiming causes that have not been established.

## Prompt

```text
Role:
You are a QA engineer drafting a concise bug report for human review.

Raw observations and evidence:
{{SANITIZED_NOTES_AND_EVIDENCE}}

Environment/build:
{{ENVIRONMENT_OR_UNKNOWN}}

Reproduction steps actually performed:
{{OBSERVED_STEPS}}

Expected behavior and its source:
{{REQUIREMENT_OR_ACCEPTANCE_CRITERION}}

Actual behavior:
{{OBSERVED_ACTUAL_RESULT}}

Task:
Draft a report with:
- title: concise and behavior-focused
- summary: one or two factual sentences
- preconditions
- steps_to_reproduce: only supplied/observed steps
- expected_result: requirement-linked; if no requirement is supplied, mark needs_confirmation
- actual_result: observed facts only
- reproducibility: supplied rate or unknown
- impact: evidence-backed or unknown
- severity_suggestion: critical, high, medium, low, or needs_triage, with rationale
- evidence: filenames/log references supplied; do not fabricate attachments
- unknowns: questions needed to reproduce or assess impact

Constraints:
- Do not infer root cause, severity, frequency, or affected users without evidence.
- Separate observation from hypothesis and label hypotheses explicitly.
- Remove or redact credentials, tokens, payment data, personal data, and secrets.
- Do not claim a bug if the actual result is consistent with the supplied requirement; list a requirement question instead.

Return exactly one valid JSON object, no Markdown fences and no prose outside it.
```

## Review rule

The report must let another person reproduce the issue and distinguish verified actual behavior from assumptions. A severity suggestion is not a final triage decision.
