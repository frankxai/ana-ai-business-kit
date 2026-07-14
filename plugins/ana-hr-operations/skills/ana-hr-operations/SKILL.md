---
name: ana-hr-operations
description: "Extend Ana's established, human-approved HR delivery method across new-client discovery, kickoff, recruiting setup, job descriptions, service offers, pricing approval, invoice drafts, template-preserving Google Docs or Canva work, and approved handoff preparation. Use for recruiting clients, first-call capture, client onboarding, document quality, operating control, and administration across many clients."
---

# Ana HR Operations

Operate one structured engagement per client and role. Capture facts once, execute the named SOP, validate every transition, and keep Ana as the approver for HR judgments, commercial terms, invoices, and external sends.

## Load the right references

- Always read `references/sop-index.md`, `references/workflow.md`, `references/hr-quality-and-privacy.md`, and `references/team-adoption-and-template-ops.md`.
- Read `references/record-contract.md` when creating or changing an engagement record.
- Read `references/google-docs-template.md` for any Google Docs template, copy, write, or verification task.
- Read `references/pricing-and-invoice.md` before creating an offer, price calculation, invoice, or send draft.
- Read the exact SOP selected by `references/sop-index.md` before taking stage actions. Do not improvise a different stage sequence.

## SOP routing

- Use `SOP-00` for the daily multi-client board, workload triage, blockers, approvals, and next actions.
- Use `SOP-01` for a new lead or the 20–30 minute first client call.
- Use `SOP-02` to convert the discovery record into an approved kickoff.
- Use `SOP-03` for the role scorecard and job description.
- Use `SOP-04` for the 20–30 minute service offer and pricing approval.
- Use `SOP-05` for requisition launch, structured recruiting delivery, weekly status, and change control.
- Use `SOP-06` to draft and reconcile an invoice.
- Use `SOP-07` for a Google Doc, email, or administrative handoff after explicit send approval.

## Team and manager routing

- Use the four-role contract in `references/team-adoption-and-template-ops.md`; individual team members prepare within their role, while Ana retains the manager/approval routes.
- Use `manager morning control`, `approval review`, or `quality and exceptions review` as read-only manager controls. Present a decision card; do not treat the request itself as approval.
- Use `$ana-research-library` for source capture, HR/recruiting research, team-practice research, or voluntary workshop research. It never turns research into a hiring or diagnostic signal.
- Use `$ana-approved-content` only to draft source-backed educational/marketing content that remains approval-gated and unpublished.
- Use `$ana-template-studio` after a stage validates and a kickoff, job description, offer, invoice, presentation, or handoff artifact must be created or checked in Google Docs or Canva.

## Operating modes

- Use **guided mode by default**: one SOP, one artifact, one validation, and one human decision at a time. Explain what is happening underneath and stop at each named gate.
- Use **orchestrated specialist mode** only when the user asks for the team, swarm, end-to-end execution, or parallel preparation. This skill remains the single coordinator and synthesis owner. Route research to `$ana-research-library`, template execution to `$ana-template-studio`, and approval-gated education/marketing to `$ana-approved-content`.
- After kickoff approval, job-description/scorecard work and offer-content preparation may run in parallel from the same immutable kickoff receipt. Candidate selection, price/invoice reconciliation, Ana approvals, visual checks, and external handoffs remain sequential human gates.
- If a connector or specialist route fails, return to guided mode at the last validated stage. Do not improvise past the missing evidence.

## Core workflow

1. Select exactly one SOP from `references/sop-index.md` and state its identifier.
2. Create or open the private engagement record from `assets/engagement.example.json`. Never commit a live record or candidate record.
3. Confirm the SOP entry criteria. If they do not pass, stop with the named exception code from that SOP.
4. Execute the SOP procedure and update facts, missing decisions, owners, due dates, blockers, approvals, and source references.
5. Route the next artifact:
   - use `job-description` for role definition and recruiting;
   - use `offer` for Ana's service scope and commercial terms;
   - use `kickoff`, `offer`, `invoice`, or `presentation` content packs only after their exact template route is known;
   - run job description and offer in parallel only after kickoff is approved.
6. Validate the record before rendering or advancing:

```bash
python scripts/validate_engagement.py <private-record.json> --stage <first-call|kickoff|job-description|offer|recruiting|invoice|send>
```

7. Create a local human-review draft when useful:

```bash
python scripts/render_documents.py <private-record.json> --document <kickoff|job-description|offer|invoice> --out <private-output.md>
```

8. Route the validated stage receipt to `$ana-template-studio`. It creates one template job and selects the exact-master, starter-practice, generated-candidate, or local-fallback route.
9. For a Google Docs final, use the installed `$google-docs` skill through Template Studio. Require the exact approved template URL, copy the master, preserve connector-visible structure, write in small verified batches, and re-read before handoff. Report whether visual layout was actually inspected.
10. For a Canva offer, invoice, or presentation, prefer the exact approved master. When Ana explicitly asks to establish a starter and the account cannot access brand templates, Template Studio may generate practice candidates, but it must show every candidate and wait for user selection before creating an editable design. Use `CANVA_RENDER_PENDING` until the named visual check is recorded. Never edit a master or call a generated candidate Ana's approved design.
11. Create an invoice only from an approved offer or milestone. Validate amounts and require invoice approval.
12. Prepare a send draft only after explicit send approval names the exact recipient and channel. Never send automatically.
13. End with the SOP receipt defined in `references/sop-index.md`.

## Existing plugin routing

- Use `$google-docs` for Google Docs template reads, copies, edits, and connector verification.
- Use Canva only for an exact Canva master after a private content pack and copy approval; visual review remains a named human action.
- For a new practice-only Canva starter, use `$ana-template-studio` and its generated-candidate selection gate. This does not replace the future exact-master route.
- Use `$google-sheets` only for the private alias-only control workbook and practice tracker, never as the candidate system of record.
- Use Google Calendar only when Ana asks to schedule or inspect a kickoff.
- Use Gmail only to create a draft after the send gate passes and Ana explicitly requests it.
- Keep local Markdown as the fallback when a connector or exact template is unavailable; label the result `TEMPLATE_BLOCKED` where appropriate.
- Keep candidate identities and evidence in the approved ATS. The engagement record may store only the ATS reference, aggregate pipeline counts, process status, and client decisions.

## Non-negotiable controls

- Do not invent price, tax, payment details, credentials, role facts, testimonials, candidate evidence, or client policy.
- Do not rank or reject candidates from protected traits or personality proxies. Use job-relevant structured evidence and keep the human decision-maker accountable.
- Do not put candidate data, CVs, recordings, IDs, health data, or bank details in this repository.
- Do not edit Ana's master Google Docs template; create a copy.
- Do not edit Ana's Canva master; create a copy and require a named visual check before client use.
- Do not infer approval from silence. Record the named approver and timestamp.
- Do not use neuroscience, psychology, personality, emotion, or health information to profile, rank, or select a candidate or employee.
- Do not send an offer, invoice, email, or calendar invitation without explicit active-turn authorization.

## Completion gate

Return:

- current engagement stage;
- artifacts created or updated;
- facts used and assumptions blocked;
- validation result;
- approvals present and missing;
- template fidelity/readback status;
- template platform, copy/visual-check status, and any `TEMPLATE_BLOCKED` or `CANVA_RENDER_PENDING` condition;
- exact next human action.
- SOP identifier, entry-gate result, exception code if blocked, and evidence receipt.
