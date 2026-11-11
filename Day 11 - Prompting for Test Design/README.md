# Day 11: Prompting for Test Design

## Goal

Compare a vague prompt with a structured prompt and judge the resulting test ideas against requirements—not against how confident or polished the AI sounds.

## Prompt anatomy

A useful test-design prompt usually gives the model:

1. **Role:** the perspective to take, such as a quality engineer. This sets the task frame, but does not make the output authoritative.
2. **Context:** the product area, user, and relevant constraints. Context helps prevent generic assumptions.
3. **Story and acceptance criteria:** the source of expected behavior. Tests should be traceable to these statements.
4. **Techniques:** request equivalence partitions, boundary values, negative cases, or risk-based selection where requirements support them.
5. **Constraints:** tell the model what not to invent and how to handle missing information.
6. **Output format:** specify fields, allowed values, and machine-readable JSON requirements.
7. **Review metadata:** ask for assumptions, questions, coverage mapping, and gaps.

A long prompt is not automatically a good prompt. Each instruction should reduce a specific uncertainty or make the output easier to evaluate.

## The exercise

Use the three fictional stories in [sample_user_stories.md](sample_user_stories.md): sign-in, card payment, and product search. The stories include explicit acceptance criteria and explicit omissions, so we can test whether the prompt distinguishes known behavior from unknown behavior.

### Prompt v1 — intentionally vague

```text
Write test cases for product search.
```

This has a feature name but no acceptance criteria, risk guidance, constraints, or output contract. Common problems to look for include invented search behavior, missing negative or boundary coverage, vague expected results, and irreusable output.

### Prompt v2 — structured

Use [qa-copilot/prompts/testcase_gen.md](../qa-copilot/prompts/testcase_gen.md). Copy the template, fill in context, the story, acceptance criteria, and an ID prefix, then compare its response with v1.

For prompt v2, the expected discipline is not “guess all possible behavior.” It should identify unknowns—for example, empty search input or result ordering—and ask questions rather than claim what the product does.

See [worked_prompt_comparison.md](worked_prompt_comparison.md) for a v1/v2 review example. [sample_login_v2_output.json](sample_login_v2_output.json) shows structured test cases in the existing Day 3 `TestCase` field format, plus priority-rationale, coverage, and ambiguity metadata. The priority rationale was deliberately separated from `TestCase` fields so the Day 3 data contract stays compatible.

For a payment-specific v2 example, inspect [sample_payment_v2_output.json](sample_payment_v2_output.json) and the [boundary walkthrough](worked_prompt_comparison.md#worked-example-card-payment-boundaries). It derives six amount values from the stated interval and lists unresolved rejection, currency, precision, and sandbox-card behavior as questions instead of inventing details.

The prepared three-story comparison and scorecard is in [comparison_results.md](comparison_results.md). It distinguishes assistant-generated teaching examples from external-model runs. [test_prompt_outputs.py](test_prompt_outputs.py) validates each sample JSON against the existing Day 3 `TestCase` model and checks rationale/coverage references.

## Worked example: derive cases from the payment amount rule

The sample payment criteria allow $1.00–$10,000.00 inclusive in $0.01 increments. This gives direct boundary candidates:

- $0.99: just below the lower boundary.
- $1.00: at the lower boundary.
- $1.01: just above the lower boundary.
- $9,999.99: just below the upper boundary.
- $10,000.00: at the upper boundary.
- $10,000.01: just above the upper boundary.

These are useful because they test the stated limits. The criteria do not define how malformed strings, other currencies, or amounts with more than two decimal places are handled, so those should be raised as questions unless another requirement defines them.

## Compare v1 and v2

For each story, save both prompt text and responses. Score each dimension from 0 to 2:

- **0:** absent or wrong.
- **1:** partly covered or needs substantial correction.
- **2:** accurate, traceable, and usable after normal review.

| Dimension | What to check | V1 score | V2 score |
|---|---|---:|---:|
| Traceability | Can each expected result be tied to a supplied criterion? |  |  |
| Coverage | Are important positive, negative, boundary, and risk cases included where supported? |  |  |
| Non-invention | Did the output avoid adding unspecified product behavior? |  |  |
| Ambiguity handling | Are assumptions/questions listed instead of hidden in expected results? |  |  |
| Test quality | Are preconditions, steps, and expected results concrete and observable? |  |  |
| Duplication | Are cases distinct rather than paraphrases? |  |  |
| Format | Does output follow the requested fields and allowed values? |  |  |
| **Total** | Maximum 14 per story |  |  |

A score is a review aid, not proof that the generated set is complete. Compare the output to your own cases and explain one change you made to the AI draft.

## Human review checklist

Before accepting a generated case:

- Confirm its expected result is explicitly required or clearly label it as a question.
- Check that the input and result are realistic and safe to use.
- Look for omitted acceptance criteria and important failure paths.
- Remove duplicates and cases that do not test distinct behavior.
- Check whether boundary values really come from a stated boundary.
- Verify priorities against impact and likelihood; explain the rationale.
- Validate the JSON structure and allowed `priority`/`type` values.
- Revise the case yourself; the model's output is a draft.

## Deliverable

Save the selected prompt as [qa-copilot/prompts/testcase_gen.md](../qa-copilot/prompts/testcase_gen.md). The workbook exercise expects a v1-versus-v2 comparison table and a saved prompt. Complete the scoring table above for all three stories, record at least one missed case and one hallucination/unsupported idea if present, and revise the prompt based on your review.

The prepared [comparison deliverable](comparison_results.md) uses fictional stories and explicitly labels the v1/v2 outputs as examples generated in this lesson, not separate runs from another model. The workbook specifically asks for **three real user stories**. To finish that part, replace these examples with three sanitized stories from actual work (remove names, credentials, customer data, and confidential details), then rerun the comparison and update the evidence. Never paste sensitive requirements or data into an AI service unless its use is approved.

## Verification state

- **Implemented:** structured prompt template, three practice stories, a three-story v1/v2 comparison and scorecard, three sample outputs, and automated TestCase-contract checks.
- **Verified:** all sample outputs parse and all test cases load into the repository's Day 3 `TestCase` model; rationale IDs and coverage references are checked by `test_prompt_outputs.py`. Actual external-model comparisons are not claimed.
- **Learned:** in progress until you can explain why the v2 constraints and ambiguity fields improve reviewability.
- **Presentable:** pending your independent walkthrough.
