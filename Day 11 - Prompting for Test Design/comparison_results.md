# Day 11 Deliverable: Prompt v1 vs. v2 Comparison

## Evidence status and method

This is a prepared, reviewable comparison using the three fictional stories in `sample_user_stories.md`. V1 and v2 examples below are generated for this lesson by GitHub Copilot in this conversation; they are **not** claimed to be outputs from an external model or independent runs in ChatGPT/Claude. If you run the prompts in another model, preserve its raw response and update the table with the actual results.

For a fair comparison, the story and acceptance criteria stay fixed; only the prompt instructions change.

- **V1:** `Write test cases for <feature>.`
- **V2:** use `qa-copilot/prompts/testcase_gen.md`, with product context, story, acceptance criteria, techniques, constraints, a JSON contract, and requests for assumptions, questions, coverage mapping, and priority rationales.

Scores use the Day 11 rubric: **0** = missing/wrong, **1** = partial or needs major correction, **2** = accurate and usable after normal human review. Dimension order is **traceability / coverage / non-invention / ambiguity / test quality / duplication / format**. The totals are review judgments for these illustrative examples, not objective measures of model quality.

## Comparison summary

| Story | V1 illustrative result and review | V1 scores / 14 | V2 evidence and reviewer note | V2 scores / 14 |
|---|---|---:|---|---:|
| Sign-in | “Valid login; invalid password; lock account after five failures; password reset.” Misses empty email/password and the requirement to compare the same generic message for unknown email vs. wrong password. Invents lockout and password reset. | `0/1/0/0/0/1/0` = **2** | [`sample_login_v2_output.json`](sample_login_v2_output.json) maps five cases to AC1–AC3 and raises unspecified password, email, and lockout details. Cases LOGIN-004/005 are separate because AC3 explicitly requires two inputs to produce the same message. | `2/2/2/2/2/2/2` = **14** |
| Card payment | “Test valid card, invalid card, Visa, min/max amount, declined card, receipt, and lockout after three failures.” Vague expected results, no values around the stated amount edges, no mapping to the five criteria, and invented Visa-only and lockout behavior. | `1/1/0/0/0/1/0` = **3** | [`sample_payment_v2_output.json`](sample_payment_v2_output.json) has six boundary values, approval/decline outcomes, and masking. It flags sandbox instruments and currency/precision behavior as questions. **Reviewer caveat:** the two outside-range cases treat the eligible range as excluding values beyond it; confirm explicit rejection behavior before asserting a particular UI error. | `2/2/1/2/2/2/2` = **13** |
| Product search | “Search for a product; show no results; empty query shows all; fuzzy typo matching; order alphabetically; search descriptions.” Covers the broad topic but omits the explicit case-insensitive rule and invents empty-query, fuzzy, description, and sort behavior. | `1/1/0/0/0/1/0` = **3** | [`sample_search_v2_output.json`](sample_search_v2_output.json) covers name matching, case-insensitive results, and the exact no-results message. It asks about empty queries, whitespace, result ordering, and the meaning of “contains.” **Reviewer caveat:** the criterion says names “contain” the keyword while the story’s omissions list matching mechanics as unspecified; clarify literal substring vs. whole token. | `2/2/1/2/2/2/2` = **13** |

## Manual baseline coverage

Before accepting a generated set, a reviewer should be able to identify at least these requirement-derived cases:

- **Sign-in:** success to dashboard; empty email; empty password; unknown email; wrong password; compare both invalid-credential outcomes for the same generic message.
- **Payment:** USD eligibility; six amount boundary points from `$0.99` through `$10,000.01`; successful authorization with order reference/final amount; declined authorization creates no order and displays the required message; card number/security code masking and absence from confirmation.
- **Search:** matching product name; same match under different keyword casing; no matching product yields the exact specified message.

The baseline is derived only from the stated criteria. Unspecified behavior stays a question, not an expected result.

## Main findings

1. **Prompt v1 is underspecified.** It invites generic cases, omits traceability and concrete expected results, and can introduce unsupported features.
2. **V2 improves reviewability.** Acceptance criteria plus a coverage map make omissions easier to see; constraints and `open_questions` expose uncertainty rather than disguising it.
3. **Output format is a contract.** Test cases retain the Day 3 fields. Review-only metadata (`priority_rationales`, `assumptions`, `open_questions`, `coverage_notes`) stays outside the `TestCase` records.
4. **Structured prompting does not remove review.** Payment and search each have a wording ambiguity that a human must resolve before treating edge-case behavior as authoritative.
5. **Do not over-read scores.** A 14/14 score means the example meets this rubric as reviewed; it does not prove completeness, correctness, security, or production suitability.

## Artifacts

- Saved prompt: `qa-copilot/prompts/testcase_gen.md`
- Three stories and criteria: `sample_user_stories.md`
- Structured v2 examples: `sample_login_v2_output.json`, `sample_payment_v2_output.json`, and `sample_search_v2_output.json`
- Automated contract checks: `test_prompt_outputs.py`

This completes the comparison-table and saved-prompt artifacts as a prepared example. Learner walkthrough/presentation remains separate from repository implementation and verification.
