# Prompt: Risk-Based Test Prioritizer

## Purpose

Suggest a transparent ordering for existing tests using impact, likelihood, and detectability evidence, while leaving the final decision with the QA owner.

## Prompt

```text
Role:
You are assisting a QA lead with risk-based test selection.

Feature/release context:
{{CONTEXT}}

Test cases (IDs and summaries):
{{TEST_CASES}}

Available evidence:
- User/business impact: {{IMPACT_EVIDENCE_OR_UNKNOWN}}
- Failure likelihood/history: {{LIKELIHOOD_EVIDENCE_OR_UNKNOWN}}
- Detection difficulty/observability: {{DETECTION_EVIDENCE_OR_UNKNOWN}}
- Time or environment constraints: {{CONSTRAINTS_OR_NONE}}

Task:
Rank the supplied cases for execution. Do not add, remove, or rewrite tests. Do not invent incident history, probability, business impact, or deadlines.

For each case return:
- id
- rank
- suggested_tier: P0, P1, P2, or P3
- impact: high, medium, low, or unknown
- likelihood: high, medium, low, or unknown
- detectability: easy, moderate, difficult, or unknown
- evidence: exact supplied evidence or "not provided"
- rationale: explain the proposed tier and name unknown factors
- human_override: null (reserved for the reviewer)

Output exactly one JSON object with ranked_cases and information_gaps. Preserve all input IDs exactly and include each exactly once. Explain that scores are advisory and require QA-owner approval.
```

## Review rule

The model may organize evidence; it cannot create it. Override the suggested order when domain knowledge or release context changes the risk, and record why.
