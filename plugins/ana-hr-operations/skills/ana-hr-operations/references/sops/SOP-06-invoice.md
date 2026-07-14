# SOP-06 — Invoice draft and reconciliation

## Purpose

Create a correct invoice draft only from an approved offer or milestone, reconcile billing facts, and stop before any accounting or payment mutation.

## Trigger

Run when an approved deposit, milestone, retainer, success fee, or completed service is ready to bill.

## Entry criteria

- Approved offer or explicitly approved milestone exists.
- Client legal/billing identity, invoice-number source, issue date, due rule, currency, tax treatment, payment terms, and finance reference are available.
- Ana names the invoice approver.

## Procedure

1. Identify the approved commercial source and billable event. Reject work not covered by that source.
2. Reconcile client legal name, billing name/address/email, engagement reference, and purchase-order/reference requirements.
3. Obtain the invoice number from the approved numbering process; never invent or reuse a number.
4. Build each line from quantity, unit price, amount, description, and approved currency.
5. Verify every line amount, subtotal, discount when applicable, tax basis/rate/amount, total, deposit/credit, and balance due.
6. Calculate due date from the approved payment terms and confirm it is not before issue date.
7. Use only a finance-system reference for payment instructions; do not store or reproduce unverified bank details.
8. Build a source-linked invoice content pack, render a visibly labeled invoice draft, and compare it with the offer/milestone and billing source. If Ana's Canva invoice master is used, copy it and require a named visual check; never include raw bank credentials.
9. Run `validate_engagement.py --stage invoice` and record Ana's invoice approval only after she reviews the final facts and total.

## Exit criteria

- Invoice validation and reconciliation pass.
- Invoice approval, approver, and timestamp are recorded.
- The invoice remains unsent and no accounting/payment record was changed.

## Evidence

- Approved commercial source and invoice-number reference.
- Arithmetic/reconciliation output.
- Draft invoice, approval, validation output, and SOP receipt.

## Exceptions

- `BILLING_EVENT_BLOCKED`: no approved offer or milestone supports the invoice.
- `BILLING_IDENTITY_BLOCKED`: legal or billing facts are incomplete.
- `NUMBERING_BLOCKED`: approved invoice number is unavailable.
- `TAX_BLOCKED`: approved tax treatment is unclear.
- `MONEY_MISMATCH`: line, subtotal, tax, total, or currency fails reconciliation.
- `PAYMENT_REFERENCE_BLOCKED`: approved finance reference is unavailable.
- `INVOICE_APPROVAL_PENDING`: Ana has not approved the final invoice draft.
