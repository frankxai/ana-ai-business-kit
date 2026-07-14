# Template and Canva routing

Ana's real templates are a quality asset. This workflow protects them and makes the underlying method repeatable without exposing their links or styling in a public repository.

## Route by artifact

| Artifact | Source of truth | Primary owner | Required gate before client use |
| --- | --- | --- | --- |
| Kickoff | Approved Google Docs master | Engagement coordinator | Ana approves scope and copied-document fidelity |
| Job description | Approved Google Docs master | Research/recruiting operator | Ana approves facts, job-relevant criteria, and template route |
| Service offer | Approved Google Docs or Canva master | Document/client-experience operator | Ana approves scope, price, tax/terms, content, and visual fidelity |
| Invoice | Approved Google Docs or Canva master + finance source | Document/client-experience operator | Ana approves billing facts, total, payment-reference route, and visual fidelity |
| Client presentation | Approved Canva master | Document/client-experience operator | Ana approves claims, visual check, audience, and handoff |

## Google Docs prompt

Use this only in a private task after the exact master and destination are known:

> Use Ana HR Operations and Google Docs. Select `[document type]` from our private template registry. The exact approved master is `[private link]`; the destination is `[private folder]`; the title is `[title]`. Ana has approved making a copy. Create a copy, never edit the master, map only the approved engagement facts into the existing structure, write in small verified batches, re-read the copy, and report the document URL, revision/readback, unresolved placeholders, and whether rendered page layout was visually inspected. Keep the result labeled draft. Do not share or send it.

If any bracketed source is missing, return `TEMPLATE_BLOCKED`.

## Canva prompt

Use this only with an exact Canva master in a private task:

> Use Ana HR Operations and Canva. Select the `[offer / invoice / presentation]` master from our private template registry. The exact approved master is `[private link]`. Ana has approved copying it for `[client alias]`. First build a concise content pack from approved facts, source each commercial value, and list unresolved items. Create or prepare a copy only; never edit the master. Preserve the existing visual system and replace only approved fields. Mark the result `CANVA_RENDER_PENDING` until a named human opens the copy in Canva and records a visual check for hierarchy, line breaks, tables, dates, totals, links, and placeholders. Do not share, export to a client, publish, or send it.

## Content packs before visual work

Every template action begins with a short structured content pack:

```text
artifact: offer
engagement: ENG-[alias]
template_id: offer-canva-master-v[version]
approved facts: [source references]
numbers: [source reference and arithmetic status]
required sections: [template sections]
unknowns: [explicit blockers]
Ana approval needed: [content / price / invoice / visual / send]
```

The content pack reduces accidental design changes and lets the operator verify the words and numbers before touching the visual template.

## Non-negotiable visual checks

For Canva and for high-stakes Google Docs exports, a named human checks:

- client alias/legal identity in the appropriate location;
- document title, role/service, dates, and version;
- all monetary values, currency, tax treatment label, invoice number, and due date where relevant;
- line breaks, tables, pagination/overflow, links, logos, and unresolved placeholders;
- wording is sourced, accurate, inclusive, and free of unsupported outcomes or false urgency;
- no candidate data, internal notes, finance credentials, or wrong-client material.

Record `visual_checked_by`, `visual_checked_at`, and any correction in the private approval record. Plain connector text readback does not prove visual fidelity.

## Status vocabulary

| Status | Meaning |
| --- | --- |
| `TEMPLATE_BLOCKED` | Exact master, destination, access, or copy approval is missing |
| `DRAFT_CONTENT_READY` | Facts are assembled but no template copy is claimed |
| `COPY_CREATED` | A copy exists; content/visual review still needed |
| `GOOGLE_DOCS_READBACK_COMPLETE` | Connector structure was re-read; visual layout may still be unverified |
| `CANVA_RENDER_PENDING` | Canva copy exists or is ready, but a human visual check is not recorded |
| `ANA_CONTENT_APPROVED` | Ana approved the document content; does not grant sharing/sending permission |
| `READY_FOR_HANDOFF_REVIEW` | Artifact and destination are ready for `SOP-07`; it is not yet sent |
