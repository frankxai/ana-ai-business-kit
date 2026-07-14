---
name: ana-template-studio
description: "Create and verify Ana's Google Docs and Canva kickoff, job-description, offer, invoice, presentation, and handoff artifacts from approved engagement facts. Use when a template must be selected, copied, populated, checked, replaced with Ana's future master, or routed through Canva candidate selection without editing a master or bypassing Ana's approvals."
---

# Ana Template Studio

Turn a validated engagement stage into one controlled template job. Preserve the master, expose every unresolved field, verify the connector-visible result, and stop at the next named human decision.

## Load the right references

- Always read `references/template-job-contract.md` and `references/docs-canva-runbook.md`.
- Read `references/specialist-orchestration.md` when the user asks for the team, agent swarm, orchestration, parallel work, or end-to-end execution.
- Use `assets/template-job.example.json` as the public-safe shape. Copy it only into a private workspace for live use.
- Run `scripts/validate_template_job.py` before a template job advances.

## Choose the operating mode

- **Guided mode is the default.** Work on one artifact, explain the next step in plain language, run one gate, and stop for the named owner or Ana. Use this for a teammate learning the process or any money-sensitive artifact.
- **Orchestrated specialist mode** keeps `$ana-hr-operations` as the single coordinator and uses this skill only for the document lane. Parallelize a job description and offer only after kickoff approval. Never parallelize or infer approvals, invoice reconciliation, candidate selection, visual review, sharing, or sending.

## Workflow

1. Receive one stage receipt from `$ana-hr-operations`: engagement ID, alias, SOP, validation result, approved fact references, unresolved decisions, artifact type, owner, and next gate.
2. Create a private template-job record from `assets/template-job.example.json`.
3. Select exactly one route:
   - `exact-master`: Ana's approved Google Docs or Canva master exists;
   - `starter-practice`: the clearly labeled private practice master is used for rehearsal only;
   - `generated-candidate`: no approved Canva master exists, so generate review candidates and wait for user selection;
   - `local-fallback`: create only a labeled Markdown content draft and return `TEMPLATE_BLOCKED`.
4. Build the content pack from approved facts. Keep every unknown as an unresolved field. For offers and invoices, include source references and arithmetic status; never propose a price, tax treatment, invoice number, or bank detail.
5. Validate the job:

```bash
python scripts/validate_template_job.py <private-template-job.json>
```

6. Execute only the selected platform route from `references/docs-canva-runbook.md`.
7. Re-read the artifact. Google Docs requires connector readback; Canva requires candidate selection when generated, editable-copy creation, and a named in-Canva visual check.
8. Present an approval card naming the artifact, revision, source facts, unresolved fields, validation result, template status, visual/readback status, and the exact decision requested.
9. Return control to `$ana-hr-operations`. This skill never sends, shares, publishes, schedules, creates accounting entries, or records an approval from silence.

## Route contracts

### Google Docs

Use the installed `$google-docs` skill. Read the exact master, create a copy in the approved destination, map approved fields in small verified batches, re-read, and report whether rendered page layout was visually inspected. Never edit the master.

### Canva exact master

Use the Canva connector with the exact approved master or design ID. Create a copy, apply the approved content pack, and preserve the existing visual system. Keep `CANVA_RENDER_PENDING` until a named human opens and checks the actual design.

### Canva generated candidate

Use generation only for a clearly labeled starter/practice route when no approved master exists. Show every candidate, wait for the user to choose one, then create the editable design from that candidate. Candidate generation is not master approval. Keep the result `CANVA_RENDER_PENDING` until the named visual check is recorded.

## Non-negotiable controls

- Never put real client, candidate, employee, billing, tax, payment, or bank data in this public skill or its example.
- Never search broadly for an unspecified live template.
- Never edit a Google Docs or Canva master.
- Never claim visual fidelity from connector text readback or a candidate thumbnail.
- Never invent a client fact, biography, qualification, claim, price, currency, tax rule, invoice number, testimonial, urgency, or result.
- Never use psychology, neuroscience, personality, emotion, health, or protected-trait inference for hiring or employee assessment.
- Never convert review into approval or approval into permission to send.

## Completion gate

Return:

- operating mode and route;
- upstream SOP and validation receipt;
- template job ID and artifact type;
- artifact/candidate references created;
- content sources and unresolved fields;
- Google Docs readback or Canva selection/visual-check status;
- approvals present and missing;
- template status and exception code;
- exact next owner and action.
