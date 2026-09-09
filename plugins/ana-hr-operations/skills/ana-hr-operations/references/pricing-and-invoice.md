# Pricing and invoice controls

Money paths fail closed.

## Offer pricing

Use only an Ana-approved price list, written quote, or explicit instruction. Capture currency, line items, quantity, unit price, discounts, subtotal, tax rate, tax amount, total, payment terms, and validity. If tax treatment is unclear, stop and request the approved value; do not provide tax or legal advice.

Require separate approvals for price and offer wording.

When the offer uses Ana's Canva master, create a source-linked content pack before editing a copied design. A named human must visually check the copy; `CANVA_RENDER_PENDING` is a stop state, not a final offer.

## Invoice creation

Create an invoice only from an approved offer or explicitly approved milestone. Reconcile:

- client legal and billing identity;
- engagement reference;
- invoice number from the approved numbering process;
- issue and due dates;
- line-item subtotal;
- currency and tax arithmetic;
- total and payment terms;
- payment instructions from an approved finance-system reference.

The plugin may produce a draft Google Doc or Markdown invoice. It must not create a payment, alter accounting records, or invent bank details.

When the invoice uses Ana's Canva master, the copied design is still an invoice draft until Ana reviews the billing identity, number, totals, payment reference, and named visual check. The visual template never contains raw bank credentials.

## Draft arithmetic contract

The local validator supports EUR, USD, GBP, CAD, AUD, NZD, CHF, SEK, NOK, and DKK with two decimal places. This is an explicit scope for the Markdown draft engine, not a list of all valid currencies. Currencies with other minor-unit precision, such as JPY or KWD, require an explicit adapter and corresponding tests before use; never relabel or round them to fit.

- Money inputs must be finite and non-negative and have at most two decimal places. Additional trailing zeros are harmless; nonzero sub-cent input is rejected rather than silently changed. Negative amounts, credits, and refunds require a separate reviewed credit-note workflow.
- Quantities and supplied percentage rates retain their fractional precision. Decimal strings are supported and preferred for exact interchange; the CLI also reads JSON decimal numbers directly as decimals.
- Inputs support up to 28 significant digits, 28 integer places, and 28 fractional places. This bounded range keeps multiplication exact within the explicit 64-digit arithmetic context and rejects pathological exponents rather than silently rounding them.
- Round each quantity × unit-price line once to cents using **ROUND_HALF_UP**, then sum the rounded line amounts. Calculate tax once from that subtotal and the supplied percentage rate, using the same rounding. Total must equal subtotal plus rounded tax exactly. The rule is deterministic regardless of the calling process's decimal context; it is an engineering convention that must match the approved accounting configuration.
- Invoice currency must match the approved offer. Invoice drafts display the invoice's own currency and payment terms; differing terms still require the recorded human approval.
- Malformed records and unsupported numbers stop validation before a draft is written. This validates shape and arithmetic; the supplied approver names and timestamps are not an authenticated approval system.

This is a single-tax-rate draft workflow. It does not establish applicable taxes, tax jurisdictions, invoice-number uniqueness, payment settlement, mixed tax treatment, credit notes, discounts as negative lines, or verified approval identity. Those require the approved finance system and human review.

## Send gate

Before preparing a sendable email, require `approvals.invoice` and `approvals.send` with named approver, timestamp, channel, and exact recipient. Re-read the attachment and totals immediately before handoff.

The Gmail plugin may create a draft only when Ana explicitly asks. Sending remains a separate, explicit human action in the active turn.
