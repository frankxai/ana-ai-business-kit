# Google Docs and Canva runbook

## Route decision

| Condition | Route | Result |
| --- | --- | --- |
| Exact approved Google Doc exists | `exact-master` | Copy, populate, read back, keep draft |
| Exact approved Canva master exists | `exact-master` | Copy, populate, named visual check |
| Team is rehearsing with the private starter master | `starter-practice` | Copy only; practice label remains visible |
| No Canva master exists and Ana wants a starter design | `generated-candidate` | Generate candidates, wait for selection, create editable copy, visual check |
| Exact source/access/approval is missing for live work | `local-fallback` | Labeled Markdown content draft plus `TEMPLATE_BLOCKED` |

## Google Docs route

1. Require artifact type, exact master, destination, title, template-registry ID, comparable example when available, and Ana's copy approval.
2. Use `$google-docs` to read the source and create a copy. Never edit the master.
3. Re-read the copy and record its document ID, revision, tab, section order, heading/list/table/link structure, and unresolved placeholders.
4. Map only source-linked fields. Write the smallest verified batches with current indexes/revision control.
5. Re-read after substantial writes and compare with the source.
6. Report `GOOGLE_DOCS_READBACK_COMPLETE`. Report rendered layout as uninspected unless an actual page/PDF view was checked.
7. Keep the copy draft until Ana approves its content and template fidelity.

## Canva exact-master route

1. Require exact design/brand-template reference, template-registry ID, approved content pack, Ana's copy approval, and named visual-check owner.
2. Copy the design or create it from the selected brand template. Never edit the master.
3. Replace only approved fields. Do not invent a missing image, logo, claim, price, tax value, or payment detail.
4. Open/check the real design for hierarchy, overflow, line breaks, dates, tables, links, totals, placeholders, and wrong-client content.
5. Record `visual_checked_by`, `visual_checked_at`, findings, and corrections. Until then use `CANVA_RENDER_PENDING`.

## Canva generated-candidate route

1. Use only for a starter/practice design or when Ana explicitly asks to establish a new master.
2. If fillable brand templates are available, search them and let the user choose before autofill. If the account cannot access that capability, record `BRAND_TEMPLATE_CAPABILITY_BLOCKED` and use normal design generation.
3. For an offer presentation, prepare generation with the approved slide outline and user-selected visual reference.
4. For an invoice, generate document candidates from the approved placeholder schema with no real billing or bank data.
5. Show every candidate. Record `CANVA_CANDIDATE_SELECTION_PENDING` and stop.
6. After the user chooses, create the editable design from the exact job/candidate IDs. Candidate choice is not content or visual approval.
7. Record `CANVA_RENDER_PENDING` until the named human checks the editable design.

## Ready prompts

### Guided Google Docs copy

> Use $ana-template-studio in guided mode for `[artifact]`. Upstream SOP `[SOP]` passed. The exact master is `[private link]`, destination is `[private folder]`, title is `[title]`, and Ana approved making a copy. Validate the template job, copy the master, map only approved facts, write in small verified batches, re-read, and stop with a fidelity card. Do not share or send.

### Generated Canva starter

> Use $ana-template-studio in guided mode for a practice-only `[offer presentation / invoice]`. Validate the content pack, generate review candidates with placeholders only, show every candidate, and stop for selection. Do not create an editable design until I choose one; do not call it Ana's approved master.

### Exact Canva master

> Use $ana-template-studio with the exact approved Canva master `[private reference]` and approved content pack `[private reference]`. Ana approved a copy for `[client alias]`. Copy only, replace approved fields, preserve the visual system, and stop at `CANVA_RENDER_PENDING` for `[visual-check owner]`. Do not share, export to a client, or send.
