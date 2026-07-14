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

## Send gate

Before preparing a sendable email, require `approvals.invoice` and `approvals.send` with named approver, timestamp, channel, and exact recipient. Re-read the attachment and totals immediately before handoff.

The Gmail plugin may create a draft only when Ana explicitly asks. Sending remains a separate, explicit human action in the active turn.
