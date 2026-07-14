# Template job contract

One template job connects one validated HR stage to one document artifact. It is an execution record, not a client or candidate record.

## Required fields

- `schema`: `ana-template-job/v1`.
- `demo_only`: `true` in public examples; live jobs stay private.
- `job_id`, `engagement_id`, `client_alias`, `artifact_type`, `mode`, `platform`, and `status`.
- `upstream`: SOP ID, engagement stage, validation result, and receipt reference.
- `route`: one of `exact-master`, `starter-practice`, `generated-candidate`, or `local-fallback`.
- `source`: approved content-pack, template, comparable artifact, destination, and last fact-review references.
- `content`: approved fact references, required sections, unresolved fields, and commercial source references when relevant.
- `artifact`: master-never-edit flag, copy/candidate references, revision, and downstream stage.
- `verification`: Docs readback, rendered-layout inspection, Canva candidate selection, and Canva visual-check state.
- `approvals`: copy, content, commercial, invoice, visual, and send states as applicable.
- `next`: exact action, owner, due date, and external action still requiring Ana.

## Status sequence

Use only truthful states:

```text
TEMPLATE_BLOCKED
  -> DRAFT_CONTENT_READY
  -> CANVA_CANDIDATE_SELECTION_PENDING (generated Canva route only)
  -> CANVA_CANDIDATE_SELECTED (generated Canva route only)
  -> COPY_CREATED
  -> GOOGLE_DOCS_READBACK_COMPLETE or CANVA_RENDER_PENDING
  -> REVIEW_COMPLETE
  -> ANA_CONTENT_APPROVED
  -> READY_FOR_HANDOFF_REVIEW
```

The exact-master Canva route skips candidate states. A local fallback stays `TEMPLATE_BLOCKED` even when its Markdown content is useful. `READY_FOR_HANDOFF_REVIEW` is not shared or sent.

## Handoff invariant

The upstream stage is immutable evidence. Template Studio may report a conflict back to `$ana-hr-operations`, but it may not silently change kickoff scope, role facts, pricing, billing facts, approvals, or hiring criteria.

The downstream handoff contains only:

- artifact reference and revision;
- current status;
- validation/readback/visual-check evidence;
- unresolved fields and exception code;
- exact approval or action still required.
