# QA-Copilot: Eight-Point AI Output Review Checklist

Use this checklist before accepting AI-generated test cases, test data, priorities, or bug reports. Validators can catch structural defects; a reviewer must still judge meaning and product correctness.

1. **Traceability:** Can each expected result be linked to an explicit acceptance criterion or an approved requirement? Flag unlinked cases and uncovered criteria.
2. **Completeness:** Are all supplied criteria covered? Are important positive, negative, boundary, and failure paths included where the requirements support them?
3. **Expected-result correctness:** Does each expected result follow from the requirement, rather than a guessed rule, response, or message?
4. **No invented behavior:** Did the output add policies, limits, controls, endpoints, integrations, or error behavior that were not supplied?
5. **No duplicates:** Do cases represent distinct behaviors/risks, or are they paraphrases? Keep separate cases only when inputs or required outcomes differ meaningfully.
6. **Test quality:** Are preconditions, steps, and expected results concrete, observable, reproducible, and independently understandable?
7. **Data and risk integrity:** Are test values synthetic and safe? Are boundaries sourced from stated constraints? Are priority claims grounded in evidence, with unknowns disclosed?
8. **Schema and consistency:** Does structured output parse and match the canonical `TestCase` schema, allowed enum values, unique IDs, rationale references, and valid coverage references?

## Decision

For each finding, record `accepted`, `edited`, or `rejected` and a brief reason. Reject or ask for clarification when an issue changes expected product behavior. A passing schema check is necessary for machine use but does not prove semantic correctness.
