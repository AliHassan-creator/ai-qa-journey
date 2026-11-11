# Eight-Point AI Output Review Checklist

Use this before accepting AI-generated tests, data, priorities, or bug reports. Automated checks catch structural defects; human review is still required for meaning and product correctness.

1. **Traceability:** Can each expected result link to an explicit acceptance criterion or approved requirement? Flag unlinked cases and uncovered criteria.
2. **Completeness:** Are supplied criteria covered? Are important positive, negative, boundary, and failure paths included when supported?
3. **Expected-result correctness:** Does each expected result follow from the requirement rather than a guessed rule, response, or message?
4. **No invented behavior:** Did the output add policies, limits, controls, endpoints, integrations, or error behavior that were not supplied?
5. **No duplicates:** Are cases distinct behaviors or risks rather than paraphrases? Keep separate cases when inputs or required outcomes differ meaningfully.
6. **Test quality:** Are preconditions, steps, and expected results concrete, observable, reproducible, and independently understandable?
7. **Data and risk integrity:** Are values synthetic and safe? Are boundaries sourced from stated constraints? Are priority claims evidence-based, with unknowns disclosed?
8. **Schema and consistency:** Does structured output parse and follow the canonical `TestCase` schema, allowed enum values, unique IDs, rationale references, and valid coverage references?

## Review decision record

For each finding, record `accepted`, `edited`, or `rejected` and a brief reason. Ask for clarification when an issue changes expected product behavior. A passing schema check is necessary for machine use but does not prove semantic correctness.
