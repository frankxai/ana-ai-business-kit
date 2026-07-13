# SOP-01 — First client call (20–30 minutes)

## Purpose

Capture the minimum complete client brief once, distinguish facts from assumptions, and leave the call with confirmed owners and next steps.

## Trigger

Run for a new lead, a newly signed client, or a material new role that needs its own engagement record.

## Entry criteria

- Ana identifies the client organization, primary contact, and reason for the call.
- A private storage location outside the repository is available.
- No candidate-sensitive material is needed for this sales/discovery call.

## Procedure

1. **0–3 minutes — frame the call.** Confirm purpose, available time, confidentiality boundary, decision to be reached, and whether the need is recruiting, another HR service, or both.
2. **3–8 minutes — why now and success.** Capture the business context, trigger, urgency, and observable 30/60/90-day outcomes.
3. **8–13 minutes — role and scope.** Capture the role/service need, location, employment type, reporting line, responsibilities, exclusions, timeline, and constraints. Mark unknowns.
4. **13–18 minutes — stakeholders and process.** Identify decision-maker, daily contact, approvers, recruiting stages, evidence expected, review cadence, and dependencies.
5. **18–23 minutes — data and documents.** Identify the approved ATS/private systems, retention owner, template type, exact master URL if available, comparable document, and destination folder. Do not collect candidate data.
6. **23–27 minutes — commercial/admin inputs.** Capture budget range only when client-approved, offer deadline, price approver, currency, billing identity owner, tax-treatment owner, and payment-term owner. Do not calculate or recommend a price here.
7. **27–30 minutes — readback.** Read back facts, assumptions, open decisions, owners, dates, and the next artifact. Ask the client to correct the summary.
8. Create or update the private engagement record and the administration block.
9. Run `validate_engagement.py --stage first-call`.

## Exit criteria

- First-call validation passes.
- The client has confirmed the readback or corrections are visibly pending.
- One next action, owner, and due date are recorded.
- No price, kickoff, document, or send approval is inferred.

## Evidence

- Private engagement record with source attribution.
- Confirmed readback or `CLIENT_CONFIRMATION_PENDING`.
- Validation output and SOP receipt.

## Exceptions

- `IDENTITY_BLOCKED`: client organization or accountable contact is unclear.
- `SCOPE_BLOCKED`: the requested outcome cannot be stated without guessing.
- `DATA_BOUNDARY_BLOCKED`: the call introduces candidate/employee data without an approved system.
- `CLIENT_CONFIRMATION_PENDING`: readback has not been confirmed.
- `COMMERCIAL_INPUT_PENDING`: price, currency, tax, or billing ownership is unresolved.
