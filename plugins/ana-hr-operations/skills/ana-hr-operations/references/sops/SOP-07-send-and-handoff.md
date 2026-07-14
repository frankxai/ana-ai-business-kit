# SOP-07 — Approved send and administrative handoff

## Purpose

Prepare the exact document/email handoff, verify the latest artifact and recipient, and keep sending as a separate human-authorized action.

## Trigger

Run when Ana asks to prepare or perform a client-facing document, email, or calendar handoff.

## Entry criteria

- The exact artifact is approved and its latest document ID, revision, link, or file is known.
- Exact recipient and channel are named.
- Ana gives fresh active-turn send approval for this recipient, channel, artifact, and action.

## Procedure

1. Re-read the engagement record, artifact approval, and current send request; do not rely on prior chat approval.
2. Resolve the exact recipient and channel. Check for lookalike addresses, wrong client aliases, reply-all risk, or unintended CC/BCC recipients.
3. Re-open the latest artifact and verify title, client identity, role/service, dates, totals when relevant, links, attachment version, draft labels, template readback status, and named Canva/visual-check status where applicable.
4. Remove internal notes, unresolved placeholders, candidate data, hidden assumptions, and unsupported claims from the client-facing package.
5. Prepare a concise email/calendar/document handoff stating purpose, action requested, deadline, and attachment/link. Gmail may create a draft only when Ana asks.
6. Present a final send card: recipient, channel, subject/title, artifact, revision, amount when applicable, and remaining risks.
7. If Ana authorizes only preparation, stop with the draft. If she explicitly authorizes sending in the active turn and the connector supports it, perform only that exact action and capture the connector receipt.
8. Update the engagement status, sent/draft fact, timestamp, next owner, due date, and follow-up. Never claim sent from a prepared draft.

## Exit criteria

- Recipient, channel, artifact, revision, and approval match.
- The status distinguishes `PREPARED`, `DRAFT_CREATED`, and `SENT` with evidence.
- The next follow-up, owner, and due date are recorded.

## Evidence

- Final send card.
- Draft URL or connector send receipt, as applicable.
- Updated engagement status and SOP receipt.

## Exceptions

- `ARTIFACT_APPROVAL_PENDING`: final artifact is not approved.
- `RECIPIENT_BLOCKED`: exact recipient is missing or ambiguous.
- `REVISION_CONFLICT`: the selected artifact is not the latest approved revision.
- `CONTENT_BLOCKED`: placeholder, private data, unsupported claim, or wrong-client content remains.
- `SEND_APPROVAL_PENDING`: no fresh active-turn approval exists.
- `CONNECTOR_BLOCKED`: requested draft/send action is unavailable or unauthenticated.
