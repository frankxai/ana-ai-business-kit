# Engagement record contract

Start by copying `assets/engagement.example.json` to a private client workspace. Replace all demo content. Never commit a live record.

## Main sections

- `engagement_id`: stable internal reference.
- `administration`: privacy-safe client alias, record owner, current/next action, next owner, due date, review timestamp, risk, and blockers.
- `template`: exact Google Docs template and comparable-document URLs.
- `client`: legal, contact, and billing identity.
- `privacy`: approved client/candidate systems, retention owner, deletion rule, and incident contact.
- `kickoff`: context, need, outcomes, timing, scope, decision-makers, cadence, and selection process.
- `role`: title, location, contract type, reporting line, mission, outcomes, responsibilities, evidence-based requirements, compensation, and process.
- `recruiting`: ATS/requisition reference, scorecard reference, structured process, aggregate stage counts, change requests, and next client update. Never candidate identities or evidence.
- `offer`: approved service, deliverables, exclusions, timeline, currency, subtotal, tax, total, terms, and validity.
- `invoice`: invoice identity, dates, lines, totals, terms, and an approved payment-details reference.
- `handoff`: exact artifact type, private reference, and approved revision selected for `SOP-07`.
- `approvals`: named approver and timestamp for kickoff, job description, recruiting launch, price, offer, invoice, and send.

## Data rules

- Keep candidate records outside this engagement record.
- Use minimum necessary personal data.
- Use a finance-system reference for payment details; do not store bank credentials or secrets here.
- Never treat an approval inferred from silence as valid.
- Record tax and pricing inputs as Ana-provided facts, not model recommendations.
- Use aliases on cross-client boards and retain legal/billing identity only in each private engagement record.
- Candidate names, emails, CV/resume content, interview recordings, IDs, health data, protected-trait inferences, and bank-account fields are forbidden in this record.
