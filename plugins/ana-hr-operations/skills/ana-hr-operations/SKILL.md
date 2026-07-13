---
name: ana-hr-operations
description: Run Ana's HR company operations from new-client discovery through kickoff, recruiting setup, job description or service offer, pricing approval, invoice draft, and human-approved send preparation. Use for recruiting clients, first-call capture, client onboarding, Google Docs template-preserving HR documents, job descriptions, proposals or offers, pricing calculations, invoice creation, and administration across many clients.
---

# Ana HR Operations

Operate one structured engagement per client. Capture facts once, validate every transition, and keep Ana as the approver for HR judgments, commercial terms, invoices, and external sends.

## Load the right references

- Always read `references/workflow.md` and `references/hr-quality-and-privacy.md`.
- Read `references/record-contract.md` when creating or changing an engagement record.
- Read `references/google-docs-template.md` for any Google Docs template, copy, write, or verification task.
- Read `references/pricing-and-invoice.md` before creating an offer, price calculation, invoice, or send draft.

## Core workflow

1. Create a private engagement record from `assets/engagement.example.json`. Never commit a live record.
2. Run the 20–30 minute first-call capture from `assets/client-kickoff.md`. Record facts, missing decisions, owners, and due dates.
3. Confirm kickoff scope, stakeholders, cadence, structured selection process, data handling, template source, and billing inputs.
4. Route the next artifact:
   - use `job-description` for role definition and recruiting;
   - use `offer` for Ana's service scope and commercial terms;
   - run both in parallel only after kickoff is approved.
5. Validate the record before rendering or advancing:

```bash
python scripts/validate_engagement.py <private-record.json> --stage <first-call|kickoff|job-description|offer|invoice|send>
```

6. Create a local human-review draft when useful:

```bash
python scripts/render_documents.py <private-record.json> --document <job-description|offer|invoice> --out <private-output.md>
```

7. For the final Google Doc, use the installed `$google-docs` skill. Require the exact approved template URL, copy the master, preserve connector-visible structure, write in small verified batches, and re-read before handoff.
8. Create an invoice only from an approved offer or milestone. Validate amounts and require invoice approval.
9. Prepare a send draft only after explicit send approval names the exact recipient and channel. Never send automatically.

## Existing plugin routing

- Use `$google-docs` for template reads, copies, edits, and connector verification.
- Use Google Calendar only when Ana asks to schedule or inspect a kickoff.
- Use Gmail only to create a draft after the send gate passes and Ana explicitly requests it.
- Keep local Markdown as the fallback when a connector or exact template is unavailable; label the result `TEMPLATE_BLOCKED` where appropriate.

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
