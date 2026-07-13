# SOP-04 — Service offer and pricing (20–30 minutes)

## Purpose

Produce a concise service offer from an approved kickoff, verify every commercial input, and obtain separate price and wording approvals.

## Trigger

Run after kickoff approval when the client needs a recruiting/service proposal or revised commercial scope.

## Entry criteria

- Kickoff approval and scope exist.
- Ana supplies an approved price list, written quote, or explicit pricing instruction.
- Currency, tax-treatment owner, payment-term owner, offer approver, and delivery deadline are known.

## Procedure

1. **0–5 minutes — confirm scope.** Reconcile requested outcome, inclusions, exclusions, dependencies, client responsibilities, and change-control boundary with the kickoff.
2. **5–10 minutes — define deliverables.** State tangible deliverables, milestones, timing, acceptance/review points, and what is not included.
3. **10–15 minutes — load approved commercial inputs.** Capture each line item, quantity, unit price, discount, currency, tax rate/treatment, validity, and payment terms with its source. Do not recommend or invent a number.
4. **15–20 minutes — calculate.** Verify quantity × unit price, line totals, subtotal, explicit discount, tax basis/amount, total, deposits or milestones, and currency consistency.
5. **20–25 minutes — draft the offer.** Use plain language, named outcomes, scope, exclusions, timeline, dependencies, commercial terms, validity, and signature/acceptance route.
6. **25–30 minutes — quality and approvals.** Compare with kickoff, pricing source, and template; list missing facts; record separate `approvals.price` and `approvals.offer` only after Ana explicitly approves each.
7. Run `validate_engagement.py --stage offer`; use the Google Docs copy/readback route if the final draft belongs in Ana's template.

## Exit criteria

- Offer validation and arithmetic pass.
- Price source and separate price/offer approvals are recorded.
- Scope and exclusions match the approved kickoff.
- The offer is draft until `SOP-07` send approval.

## Evidence

- Price-source reference and arithmetic breakdown.
- Draft offer and template readback status.
- Two approvals, validation output, and SOP receipt.

## Exceptions

- `SCOPE_CONFLICT`: offer scope differs from kickoff without approved change control.
- `PRICE_SOURCE_BLOCKED`: no Ana-approved price source exists.
- `TAX_BLOCKED`: tax treatment is unclear or would require advice.
- `MONEY_MISMATCH`: line, subtotal, tax, discount, or total arithmetic fails.
- `PRICE_APPROVAL_PENDING`: price is not explicitly approved.
- `OFFER_APPROVAL_PENDING`: wording/scope is not explicitly approved.
