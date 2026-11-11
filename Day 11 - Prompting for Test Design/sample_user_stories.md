# Day 11 Practice Stories

These are fictional exercises written for prompt practice. They are not requirements for a real product. The search story intentionally leaves details open so the prompt can demonstrate ambiguity detection.

## Story A — Sign-in

**User story**  
As a registered user, I want to sign in with my email and password so that I can access my account.

**Acceptance criteria**

1. A registered user who submits the correct email and password is signed in and taken to the account dashboard.
2. Submitting the form with either email or password empty does not sign in the user and identifies the required field.
3. An unrecognized email or incorrect password does not sign in the user and displays the same generic message: “Email or password is incorrect.”

**Not specified**

- Email normalization or case sensitivity.
- Password length or character rules.
- Account lockout, rate limits, CAPTCHA, MFA, or session duration.
- Exact required-field text or accessibility behavior.

## Story B — Card payment

**User story**  
As a customer checking out, I want to pay by card so that I can place my order.

**Acceptance criteria**

1. The accepted currency is USD.
2. A payment amount from $1.00 through $10,000.00 inclusive, in increments of $0.01, is eligible for submission.
3. A successful authorization displays an order-confirmation page with the order reference and final amount.
4. A declined authorization does not create an order and displays a payment-declined message.
5. The card number and security code are masked after entry and are not displayed on the confirmation page.

**Not specified**

- Accepted card brands, test-card numbers, expiry-date rules, and security-code length.
- Whether the amount is typed by the user or calculated from the cart.
- Retry behavior, idempotency, timeout handling, refunds, and payment-provider behavior.

Use fictional placeholders only. Do not enter real card data.

## Story C — Product search

**User story**  
As a shopper, I want to search the product catalog by keyword so that I can find relevant products.

**Acceptance criteria**

1. Submitting a non-empty keyword shows products whose names contain that keyword.
2. Matching is case-insensitive.
3. When no product matches, the page displays “No products found.”

**Not specified**

- Whether matching is substring, prefix, token, or fuzzy matching.
- Minimum/maximum query length, whitespace behavior, or punctuation handling.
- Search across descriptions, categories, or product identifiers.
- Result ordering, pagination, filters, and behavior for an empty query.

## Practice rule

Ask the prompt to generate cases from the supplied criteria and report ambiguity separately. Review every proposed expected result against the criteria above; do not treat an AI suggestion as a new requirement.
