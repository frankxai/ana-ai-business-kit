# SOP-02 — Client kickoff and engagement activation

## Purpose

Convert discovery into an approved operating agreement covering scope, recruiting process, responsibilities, communication, data handling, documents, and commercial dependencies.

## Trigger

Run after the first-call record is confirmed and before producing a final job description, offer, or live recruiting work.

## Entry criteria

- `first-call` validation passes.
- Client decision-maker and Ana's internal owner are named.
- Open discovery assumptions are either resolved or explicitly assigned.

## Procedure

1. Re-read the first-call record and list every unresolved assumption before the kickoff.
2. Confirm business outcome, role/service outcome, scope, exclusions, timeline, dependencies, and change-control route.
3. Confirm accountable decision-maker, daily contact, document approvers, commercial approver, and expected turnaround times.
4. Confirm the structured recruiting stages, scorecard owner, job-relevant evidence, interview responsibilities, shortlist decision, and final human decision-maker.
5. Confirm approved systems, access boundary, retention owner, deletion rule, and data-incident contact. Keep candidate identities out of the engagement record.
6. Confirm meeting/update cadence, channels, escalation route, next client update, and response expectations.
7. Confirm required artifacts, template-registry ID, platform (Google Docs or Canva), exact approved master, comparable approved example, destination folder, copy owner, and permission to create copies. Mark `TEMPLATE_BLOCKED` when incomplete. For Canva, require a named visual check after copy creation.
8. Confirm pricing source owner, currency, tax-treatment owner, billing identity, invoice route, and payment terms without giving tax/legal advice.
9. Produce a kickoff readback with decisions, open items, owners, team roles, template route/status, and dates.
10. Record Ana's explicit kickoff approval and timestamp; then run `validate_engagement.py --stage kickoff`.

## Exit criteria

- Kickoff validation passes and Ana's approval is recorded.
- Scope, exclusions, process, privacy, cadence, document route, and commercial owners are explicit.
- The next route is `SOP-03`, `SOP-04`, or both.

## Evidence

- Approved kickoff record or draft marked with missing approvals.
- Decision log and change-control owner.
- Validation output and SOP receipt.

## Exceptions

- `DISCOVERY_BLOCKED`: first-call validation fails.
- `DECISION_OWNER_BLOCKED`: client decision-maker or document approver is unclear.
- `PROCESS_BLOCKED`: selection stages or job-relevant criteria are unresolved.
- `PRIVACY_BLOCKED`: approved systems, retention, or deletion ownership is missing.
- `TEMPLATE_BLOCKED`: exact source, destination, or copy approval is missing.
- `KICKOFF_APPROVAL_PENDING`: Ana has not approved activation.
