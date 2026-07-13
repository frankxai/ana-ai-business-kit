# Engagement record contract

Start by copying `assets/engagement.example.json` to a private client workspace. Replace all demo content. Never commit a live record.

## Main sections

- `engagement_id`: stable internal reference.
- `template`: exact Google Docs template and comparable-document URLs.
- `client`: legal, contact, and billing identity.
- `kickoff`: context, need, outcomes, timing, scope, decision-makers, cadence, and selection process.
- `role`: title, location, contract type, reporting line, mission, outcomes, responsibilities, evidence-based requirements, compensation, and process.
- `offer`: approved service, deliverables, exclusions, timeline, currency, subtotal, tax, total, terms, and validity.
- `invoice`: invoice identity, dates, lines, totals, terms, and an approved payment-details reference.
- `approvals`: named approver and timestamp for kickoff, job description, price, offer, invoice, and send.

## Data rules

- Keep candidate records outside this engagement record.
- Use minimum necessary personal data.
- Use a finance-system reference for payment details; do not store bank credentials or secrets here.
- Never treat an approval inferred from silence as valid.
- Record tax and pricing inputs as Ana-provided facts, not model recommendations.
