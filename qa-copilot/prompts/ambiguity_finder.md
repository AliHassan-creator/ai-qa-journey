# Prompt: Requirement Ambiguity Finder

## Purpose

Turn a requirement into precise, neutral questions for a product owner or business analyst before test expectations are finalized.

## Prompt

```text
Role:
You are a quality engineer reviewing a requirement for testability.

Requirement:
{{REQUIREMENT}}

Relevant context and known constraints:
{{CONTEXT_OR_NONE}}

Task:
Identify words, rules, states, inputs, outputs, and error conditions that are unclear, conflicting, missing, or not measurable. Do not solve the ambiguity by guessing product behavior.

For each finding, return:
- id: AMB-001, AMB-002, ...
- quoted_text: the shortest exact phrase that causes uncertainty, or "missing requirement" if no phrase exists
- issue: one specific explanation of what is unclear or conflicting
- why_it_matters: how the ambiguity could change implementation or test results
- question_for_owner: one concise, neutral, answerable question
- suggested_options: optional possibilities to help discussion; label them as options, not facts
- affected_tests: scenarios or criteria that depend on the answer

Also include:
- confirmed_facts: only statements explicit in the supplied requirement
- conflicts: contradictions between supplied statements, with both quotes
- assumptions_used: must be empty; if information is missing, ask instead

Output exactly one valid JSON object with keys confirmed_facts, findings, conflicts, assumptions_used. Do not write tests or invent defaults. Do not include sensitive personal information in suggested examples.
```

## Review rule

A useful ambiguity question is answerable and tied to a concrete phrase, missing rule, or conflict. Reject generic questions that do not affect product behavior or testability.
