# Engagement workflow

Use one engagement record per client and role. Never use chat history as the system of record.

## State sequence

1. `first-call` — capture the 20–30 minute discovery call.
2. `kickoff` — confirm scope, stakeholders, cadence, selection process, privacy, and next document.
3. `job-description` — create the role scorecard and job description when recruiting a role.
4. `offer` — create the service offer from Ana-approved scope and pricing.
5. `invoice` — create an invoice draft from the approved offer or completed milestone.
6. `send` — prepare the final email and attachment only after invoice and send approvals exist.

Job description and offer can run in parallel after kickoff. Invoice depends on an approved offer. Send depends on an approved invoice.

## First-call output

Capture facts, open decisions, owner, due date, and the next artifact. Mark assumptions separately. Do not invent missing price, tax, payment, legal, role, or candidate facts. End the call with a short readback for the client to confirm.

## Kickoff output

Confirm:

- business outcome and role outcome;
- scope and exclusions;
- decision-makers and daily contact;
- document owners and approval deadlines;
- structured selection stages and job-relevant evidence;
- candidate-data handling and deletion expectations;
- communication cadence;
- Ana's approved Google Docs template and nearest comparable completed document;
- pricing source, currency, billing identity, tax treatment, and payment terms.

## Administration rule

At every transition, write a short status block:

- current stage;
- complete facts;
- missing decisions;
- approvals obtained;
- next owner and due date;
- external action still requiring Ana.

Use `scripts/validate_engagement.py` before advancing a stage.
