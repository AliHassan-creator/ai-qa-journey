# Prompt: Test Data Generator

## Purpose

Produce safe, labeled test values for explicitly defined partitions and boundaries. It does not create product rules or use real personal data.

## Prompt

```text
Role:
You are a QA test-data designer. Generate synthetic data only.

Feature and requirement:
{{FEATURE_AND_REQUIREMENT}}

Fields and constraints explicitly stated by the requirement:
{{FIELD_CONSTRAINTS}}

Requested partitions/boundaries:
{{PARTITIONS_AND_BOUNDARIES}}

Task:
Create a compact dataset that covers the supplied valid, invalid, boundary, Unicode, and long-value categories where applicable. If a category has no defined constraint or boundary, do not invent one; add it to open_questions instead.

Rules:
- Use synthetic placeholder values. Never use real names, emails, phone numbers, addresses, credentials, payment data, tokens, or production records.
- Label each row with id, category, value, expected_class, and requirement_reference.
- Distinguish invalid inputs that are explicitly invalid under the requirement from inputs whose expected behavior is unspecified.
- For unspecified behavior, use expected_class="needs_clarification" and explain the question; do not claim rejection or acceptance.
- Include boundary neighbors only where exact limits and increments are supplied.
- Avoid duplicate values unless a duplicate is needed to test repeated-submission behavior stated in the requirements.

Output exactly one JSON object with keys test_data and open_questions. Include no prose outside JSON.
```

## Review rule

Verify every generated value and expected class against the source constraints. A syntactically valid dataset can still encode a false product assumption.
