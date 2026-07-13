---
name: ana-hr-operations
description: Run Ana's HR company operations from new-client discovery through kickoff, recruiting setup, job description or service offer, pricing approval, invoice draft, and human-approved send preparation. Use for recruiting clients, first-call capture, client onboarding, Google Docs template-preserving HR documents, job descriptions, proposals or offers, pricing calculations, invoice creation, and administration across many clients.
---

# Ana HR Operations

Operate one structured engagement per client and role. Capture facts once, execute the named SOP, validate every transition, and keep Ana as the approver for HR judgments, commercial terms, invoices, and external sends.

## Load the right references

- Always read `references/sop-index.md`, `references/workflow.md`, and `references/hr-quality-and-privacy.md`.
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

## Core workflow

1. Select exactly one SOP from `references/sop-index.md` and state its identifier.
2. Create or open the private engagement record from `assets/engagement.example.json`. Never commit a live record or candidate record.
3. Confirm the SOP entry criteria. If they do not pass, stop with the named exception code from that SOP.
4. Execute the SOP procedure and update facts, missing decisions, owners, due dates, blockers, approvals, and source references.
5. Route the next artifact:
   - use `job-description` for role definition and recruiting;
   - use `offer` for Ana's service scope and commercial terms;
   - run both in parallel only after kickoff is approved.
6. Validate the record before rendering or advancing:

```bash
python scripts/validate_engagement.py <private-record.json> --stage <first-call|kickoff|job-description|offer|recruiting|invoice|send>
```

7. Create a local human-review draft when useful:

```bash
python scripts/render_documents.py <private-record.json> --document <job-description|offer|invoice> --out <private-output.md>
```

8. For the final Google Doc, use the installed `$google-docs` skill. Require the exact approved template URL, copy the master, preserve connector-visible structure, write in small verified batches, and re-read before handoff.
9. Create an invoice only from an approved offer or milestone. Validate amounts and require invoice approval.
10. Prepare a send draft only after explicit send approval names the exact recipient and channel. Never send automatically.
11. End with the SOP receipt defined in `references/sop-index.md`.

## Existing plugin routing

- Use `$google-docs` for template reads, copies, edits, and connector verification.
- Use Google Calendar only when Ana asks to schedule or inspect a kickoff.
- Use Gmail only to create a draft after the send gate passes and Ana explicitly requests it.
- Keep local Markdown as the fallback when a connector or exact template is unavailable; label the result `TEMPLATE_BLOCKED` where appropriate.
- Keep candidate identities and evidence in the approved ATS. The engagement record may store only the ATS reference, aggregate pipeline counts, process status, and client decisions.

## Non-negotiable controls

- Do not invent price, tax, payment details, credentials, role facts, testimonials, candidate evidence, or client policy.
- Do not rank or reject candidates from protected traits or personality proxies. Use job-relevant structured evidence and keep the human decision-maker accountable.
- Do not put candidate data, CVs, recordings, IDs, health data, or bank details in this repository.
- Do not edit Ana's master Google Docs template; create a copy.
- Do not infer approval from silence. Record the named approver and timestamp.
- Do not send an offer, invoice, email, or calendar invitation without explicit active-turn authorization.

## Completion gate

Return:

- current engagement stage;
- artifacts created or updated;
- facts used and assumptions blocked;
- validation result;
- approvals present and missing;
- template fidelity/readback status;
- exact next human action.
- SOP identifier, entry-gate result, exception code if blocked, and evidence receipt.
