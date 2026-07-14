# SOP-00 — Multi-client control board

## Purpose

Give Ana one privacy-safe view of priorities, blockers, approvals, and due dates across many clients without copying candidate or client-sensitive content into the board.

## Trigger

Run at the start and end of the working day, before a weekly planning block, or when Ana asks what needs attention.

## Entry criteria

- Private engagement records are accessible from an approved workspace.
- Each engagement has a stable ID and client alias.
- Candidate identities remain in the approved ATS and are not loaded into the board.

## Procedure

1. Read only the minimum status fields from each active engagement: alias, stage, last review, next action, owner, due date, blockers, risk, template status, and missing approval.
2. Reject stale or ambiguous records instead of inferring status from chat history.
3. Validate the current stage when a record claims it is ready to advance.
4. Classify each row: `RED` overdue/privacy/money/send block, `AMBER` due within two working days or awaiting approval, `GREEN` on track, `PAUSED` explicitly held.
5. Sort by red risk, overdue date, client commitment, then earliest due date. Do not rank clients by commercial value unless Ana explicitly supplies that policy.
6. Render `assets/daily-operations-board.md` using aliases only.
7. Create a decision queue for Ana: approvals, client questions, internal follow-ups, template/connector-blocked work, and exceptions. Present it as a decision card; never treat the board review as approval.
8. Record the board timestamp and source-record timestamps. Do not write board summaries back into stale source records without review.

## Exit criteria

- Every active engagement has one next action, owner, and due date or is explicitly paused.
- Every red/amber item names its blocker and required decision.
- Every item has an assigned team role or is explicitly owned by Ana.
- The board contains no candidate names, emails, CV content, interview evidence, billing address, or bank information.

## Evidence

- Generated daily board.
- Count of active, red, amber, green, and paused engagements.
- List of source records not reviewed and exception codes raised.
- SOP receipt.

## Exceptions

- `RECORD_MISSING`: engagement source cannot be found.
- `RECORD_STALE`: last-reviewed timestamp is missing or no longer trustworthy.
- `STATUS_CONFLICT`: record fields and claimed stage disagree.
- `PRIVACY_BLOCKED`: the requested board would expose personal or confidential content.
- `APPROVAL_BLOCKED`: a next action depends on Ana or client approval.
