# Team adoption and template operations

## Four role model

| Role | Owns | May not approve |
| --- | --- | --- |
| Ana — manager | Quality review, exception decisions, scope, hiring accountability, price, invoice, publish, send | Nothing is auto-approved |
| Engagement coordinator | First-call/kickoff capture, board, owners, dates, document route | Scope, price, invoice, send |
| Research and recruiting operator | Job-relevant scorecard/process, aggregate ATS status, research entry | Candidate decision, profiling, client-facing claims |
| Document and client-experience operator | Content pack, copied template, visual-check card, delivery draft | Master edit, commercial approval, publish/send |

## Manager controls

Treat prompts such as `manager morning control`, `approval review`, and `quality and exceptions review` as read-only decision-support routes. They can create a decision card but never record approval until Ana actively supplies the specific approval in the current task.

The manager board uses client aliases only and contains: stage, next action, owner, due date, blocker, source-review timestamp, template status, and missing approval. It never contains candidate identity, interview evidence, billing address, or payment details.

## Template route contract

Record only private references in a live engagement record. A document route requires:

- `template_id`, platform (`google-docs` or `canva`), exact master reference, and destination;
- named copy approval from Ana;
- content-pack source facts and unresolved fields;
- copied artifact reference/revision;
- connector readback (`google-docs`) or named visual check (`canva`);
- Ana content/template approval and a separate handoff/send gate when relevant.

Use these truthful states:

- `TEMPLATE_BLOCKED`: an exact source, destination, access, or copy approval is missing;
- `DRAFT_CONTENT_READY`: facts are ready but no copy is claimed;
- `COPY_CREATED`: copied artifact exists; review pending;
- `GOOGLE_DOCS_READBACK_COMPLETE`: connector-visible structure re-read; layout may still require visual inspection;
- `CANVA_RENDER_PENDING`: a Canva copy needs named human visual inspection;
- `READY_FOR_HANDOFF_REVIEW`: artifact is reviewed; a fresh send/share gate remains.

## Platform routing

- **Google Docs:** exact master → copy → small verified edits → re-read → report visual-inspection status.
- **Canva:** exact master → copy → approved content pack → named human checks actual visual result. No generic reconstruction, export, client share, or send without the appropriate approval.
- **Google Sheets:** private control workbook may contain aliases, workflow state, source references, and approvals. Candidate identities/evidence remain in the ATS.

## Skill handoffs

- Use `$ana-research-library` for a source-backed research entry, evidence mapping, team-practice question, or research brief.
- Use `$ana-approved-content` only after a factual source/approved library entry exists; it creates an approval-gated draft and never publishes/sends.

Neither specialised skill changes hiring accountability, template protections, finance controls, or external-action gates.
