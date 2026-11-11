# QA-Copilot

Starter structure for a reusable, human-reviewed QA assistant. Modules will be added incrementally as the five-week plan progresses.

- `core/`: schemas and deterministic validation helpers for schema, duplicate, and traceability checks
- `runner/`: test execution adapters
- `prompts/`: versioned prompt templates
- `samples/`: sanitized sample inputs and outputs
- `tests/`: automated checks for the toolkit
- `prompts/`: five versioned prompts for test design, ambiguity, test data, risk, and bug reports, plus the AI-output review checklist
- `tests/test_validators.py`: offline unit tests for deterministic output validation

Keep credentials in a local `.env` file based on the repository's `.env.example`.
