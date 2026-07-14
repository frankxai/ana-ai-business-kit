# Engagement record contract

Start by copying `assets/engagement.example.json` to a private client workspace. Replace all demo content. Never commit a live record.

## Main sections

- `engagement_id`: stable internal reference.
- `administration`: privacy-safe client alias, record owner, current/next action, next owner, due date, review timestamp, risk, and blockers.
- `template`: private template-registry reference, exact master/comparable references, document routes, platform, copy status, and visual-check requirement. Never place a live URL in this public repository.
- `team`: the named manager/approver, engagement coordinator, research/recruiting operator, and document/client-experience operator. Team roles prepare work; only the named Ana manager approval makes a controlled transition.
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
- Do not add personality profiles, neuroscience/health inferences, emotion inference, or candidate/employee assessments to the record.
- A document route must name its platform, master/template ID, copy/visual-check status, and human approval needed. `TEMPLATE_BLOCKED` and `CANVA_RENDER_PENDING` are truthful stop states, not errors to hide.
