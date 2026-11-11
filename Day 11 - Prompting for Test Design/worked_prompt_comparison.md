# Worked comparison: prompt v1 vs prompt v2

This is a teaching example authored for this exercise, not a claim that an external model was run. Use the same sign-in story from `sample_user_stories.md` for both prompts so the prompt quality—not a change in requirements—is what we compare.

## Prompt v1

```text
Write test cases for sign-in.
```

### Illustrative v1 draft

1. Test successful login.
2. Test invalid password.
3. Test locked account.
4. Test password reset.
5. Test login rate limiting.

### Review

- It misses the explicitly required empty-email and empty-password behavior.
- It does not specify useful steps, preconditions, or observable expected results.
- It invents locked-account, password-reset, and rate-limit behavior not present in the story.
- It does not check the requirement that unknown email and wrong password use the same generic message.
- It has no traceability, priority rationale, or requested data format.

These items make v1 a weak draft, not because it is short by itself, but because it lacks requirements and review constraints.

## Prompt v2

Use `qa-copilot/prompts/testcase_gen.md` with Story A from `sample_user_stories.md`, acceptance criteria AC1–AC3, product context “a web account sign-in page,” and ID prefix `LOGIN`.

### Illustrative v2 result

See `sample_login_v2_output.json`. It covers the three supplied criteria, maps tests to each criterion, and lists missing details as questions instead of asserting lockout or password rules. Priority reasons are separate review metadata, not extra fields in each Day 3 `TestCase`.

### Prompt refinement found during review

The first prompt draft requested a reason for every priority but did not define an output field for that reason. That made the requirement impossible to follow while still obeying the exact JSON contract. The prompt was revised to add a top-level `priority_rationales` list keyed by test-case ID. The canonical Day 3 `TestCase` objects remain unchanged. Since the sample has no measured likelihood information, its rationales explicitly say likelihood is unassessed rather than making it up.

## Scorecard example

Scores are illustrative reviewer judgments for this sample:

| Dimension | V1 | V2 | Reason |
|---|---:|---:|---|
| Traceability | 0 | 2 | V2 maps each case to a supplied criterion. |
| Coverage | 1 | 2 | V2 covers success, required fields, and both invalid-credential variants. |
| Non-invention | 0 | 2 | V1 adds lockout/reset/rate limiting; V2 records unknowns. |
| Ambiguity handling | 0 | 2 | V2 makes open questions explicit. |
| Test quality | 0 | 2 | Revised v2 includes preconditions, actionable steps, observable outcomes, and separate priority rationale metadata. |
| Duplication | 1 | 2 | V2 keeps credential variants separate because AC3 requires comparison of the same generic message. |
| Format | 0 | 2 | V2 follows the JSON wrapper and `TestCase` field contract. |
| **Total / 14** | **2** | **14** | The initial v2 draft would score 13 because it omitted the requested rationale; the revised v2 example adds it. Re-score against your own product knowledge. |

## Important reviewer note

Even a fully scored v2 example is not automatically correct or complete. Confirm that the test data is valid for the product, the expected behavior is authorized by requirements, and no security rule is missing. In the payment story, use only fictional placeholders; never use real payment data.

## Worked example: card-payment boundaries

The detailed v2-style sample is in `sample_payment_v2_output.json`. For the stated inclusive interval `$1.00` to `$10,000.00` in one-cent steps, the boundary set is:

| Position | Value | Reason |
|---|---:|---|
| Below lower limit | `$0.99` | Check just outside the minimum. |
| At lower limit | `$1.00` | Check the inclusive minimum. |
| Just inside lower limit | `$1.01` | Check the next permitted cent. |
| Just inside upper limit | `$9,999.99` | Check the permitted cent before the maximum. |
| At upper limit | `$10,000.00` | Check the inclusive maximum. |
| Above upper limit | `$10,000.01` | Check just outside the maximum. |

The sample also separates other acceptance criteria into authorization-success, authorization-decline, and sensitive-data masking cases. It asks which sandbox instruments produce approved/declined results instead of inventing card numbers.

**Requirement wording nuance:** “amounts in this interval are eligible for submission” defines the eligible set, but the story does not explicitly state the handling of out-of-range values, non-USD currency, or precision beyond cents. The boundary examples treat the outside values as not eligible based on the stated interval and flag the exact rejection behavior for confirmation. A reviewer should resolve that question with the product owner before using a rejection message or UI behavior as an expected result.
