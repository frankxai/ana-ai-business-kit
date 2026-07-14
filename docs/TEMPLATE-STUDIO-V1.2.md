# Template Studio v1.2

Template Studio joins Ana's SOPs, private engagement records, Google Docs, Canva, and approvals into one inspectable artifact pipeline. Daily users do not need GitHub knowledge.

## The operating loop

```text
private engagement record
  -> ana-hr-operations selects and validates one SOP
  -> approved fact/content pack
  -> ana-template-studio creates one template job
  -> Google Docs copy/readback OR Canva candidate/copy/visual check
  -> Ana decision card
  -> ana-hr-operations advances or holds the engagement
  -> SOP-07 only after fresh recipient/channel/artifact/send approval
```

## What each system owns

| System | Owns | Does not own |
| --- | --- | --- |
| Codex plugin | SOPs, prompts, validation, handoff contracts, quality gates | Live client/candidate records or master URLs |
| Google Drive | Private engagement folders, starter/real Docs masters, copied artifacts, control workbook | Candidate system of record |
| Canva | Exact visual masters, generated review candidates, editable copies | Source facts, commercial authority, send authority |
| Approved ATS | Candidate identities, evidence, decisions, retention | Offer/invoice/template content |
| Ana | Practice judgment, scope, price, invoice, content, visual, publish and send approvals | Nothing is auto-approved |

## Guided mode

Use for normal team adoption and every money-sensitive route. The teammate completes one SOP, one content pack, one template job, one validation, and one decision card. The plugin explains the why beneath the step and names the stop condition.

## Orchestrated specialist mode

`$ana-hr-operations` remains the coordinator. It routes research to `$ana-research-library`, document execution to `$ana-template-studio`, and source-backed educational drafts to `$ana-approved-content`. Job-description and offer preparation may run in parallel only after kickoff approval. All approvals, candidate selection, Canva visual review, invoice reconciliation, and handoff are sequential.

## Replacing starters with Ana's masters

1. Ana supplies the exact private Google Doc/Canva master and nearest approved example.
2. The template owner records its private registry ID, artifact type, platform, owner, permissions, required fields, and visual-check owner.
3. The team rehearses on a copy with fictional data.
4. Ana checks structure, wording, calculations, and visuals.
5. The registry route changes from `starter-practice` to `exact-master`; prompts and SOPs do not change.
6. The practice starter remains clearly labeled and is never used for a client.

## Current private starter pack

The existing non-retreat Ana Team Operating System Drive contains five short practice masters: first call/kickoff, role scorecard/job description, service-offer content, invoice content, and approval/handoff. Exact links stay in the private registry and are intentionally absent from Git.

The current Canva account does not expose fillable brand-template generation without a paid-plan capability. Normal generated candidates remain available, but the user must select a candidate before Codex creates an editable design. This is recorded as a capability fact, not hidden behind a generic failure.
