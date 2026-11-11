# Prompt: Generate Reviewable Manual Test Cases

## Purpose

Draft test cases from a user story and acceptance criteria. The result is a proposal for a human QA reviewer—not a source of truth and not an instruction to invent product behavior.

## Prompt template

Copy the prompt below and replace every `{{...}}` field. Keep product requirements separate from assumptions and open questions.

```text
Role:
You are a senior quality engineer designing clear, risk-aware manual tests.

Task:
Draft manual test cases for the user story and acceptance criteria below.
Do not write automation code.

Product context:
{{PRODUCT_CONTEXT}}

User story:
{{USER_STORY}}

Acceptance criteria:
{{ACCEPTANCE_CRITERIA}}

Constraints:
- Treat the supplied story and acceptance criteria as the only source of product behavior.
- Do not invent endpoints, UI controls, validation messages, policies, limits, or data rules.
- If a useful test depends on missing information, do not assert a guessed result. Add it to open_questions.
- Use equivalence partitioning and boundary-value analysis only where the requirements define meaningful input classes or boundaries.
- Prioritize scenarios by user impact, likelihood, and failure cost. Do not invent likelihood data; when it is unknown, base the rationale on the documented impact and state that likelihood is unassessed.
- Include positive, negative, and boundary scenarios when supported by the requirements.
- Avoid duplicate cases; each case must cover a distinct behavior or risk.
- Make steps executable by a person without relying on unstated setup.
- Expected results must be observable and traceable to a supplied acceptance criterion.
- Use fictional, non-sensitive test data. Never request or include real credentials, payment data, or personal data.
- Assign IDs in the form {{ID_PREFIX}}-001, {{ID_PREFIX}}-002, ...
- Set type to one of: functional, negative, boundary, security, usability, compatibility.
- Set priority to one of: critical, high, medium, low.

Output contract:
Return exactly one valid JSON object, with no Markdown fences and no prose before or after it.
The object must have exactly these top-level keys:
{
  "test_cases": [
    {
      "id": "string",
      "title": "string",
      "preconditions": "string",
      "steps": ["string"],
      "expected": "string",
      "priority": "critical | high | medium | low",
      "type": "functional | negative | boundary | security | usability | compatibility"
    }
  ],
  "priority_rationales": [
    {
      "id": "test case ID",
      "rationale": "brief reason for the assigned priority; identify likelihood as unassessed if the requirements provide no likelihood evidence"
    }
  ],
  "assumptions": ["string"],
  "open_questions": ["string"],
  "coverage_notes": [
    {
      "criterion": "exact acceptance-criterion reference",
      "covered_by": ["test case ID"],
      "gaps": ["string"]
    }
  ]
}

Do not put assumptions into expected results. If a criterion cannot be tested as written, explain the gap in coverage_notes and ask a question.
```

## Why the sections matter

- **Role** sets the perspective; it does not guarantee correctness.
- **Story and criteria** ground cases in product requirements and provide traceability.
- **Constraints** reduce invented behavior, duplicated tests, and untestable expectations.
- **Techniques** direct attention to partitions, boundaries, and risk without forcing irrelevant cases.
- **Output contract** makes the response consistent and easier to validate or review.
- **Assumptions and questions** make uncertainty visible instead of hiding it in a test.
- **Human review** remains mandatory: confirm each expected result against an authoritative requirement before execution.

## Schema compatibility note

Each item in `test_cases` follows the existing Day 3 `TestCase` model: `id`, `title`, `preconditions`, `steps`, `expected`, `priority`, and `type`. The wrapper fields (`priority_rationales`, `assumptions`, `open_questions`, and `coverage_notes`) are review metadata and are not `TestCase` instances. Keep rationale metadata separate so the canonical Day 3 case schema is not changed. Extract `test_cases` before passing them to the Day 3 CSV/JSON loader.
