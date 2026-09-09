---
name: team-practice-design
description: Design a voluntary, nonclinical team practice or AI adoption pilot with observable workflow outcomes, private participant reflection, and aggregate reporting. Use for an HR agency workshop, founder gathering, or team working agreement; never for employee assessment or therapy.
---

# Team Practice Design

Design one bounded change to how a team works: an approved AI drafting task, a clearer handoff, a decision review, or a meeting practice. The accountable practitioner chooses the method. Separate supported source claims, practice hypotheses, and measured results.

## Workflow

1. Start from an approved engagement scope or a clearly labelled synthetic rehearsal. Name the workflow, facilitator, sponsor, decision owner, review date, eligible population, and voluntary participants. A venue booking never authorizes participation or reporting.
2. Choose one observable work outcome and its quality check. Use the same task definition, measurement window, unit, and quality rubric for baseline and pilot. Record raw numerator/denominator counts; report adoption against the eligible population, not only attendees. Set operator-hour and tool-spend ceilings from the owner, not invented market assumptions.
3. Use [the practice contract](references/practice-contract.md) to define participation choices and the reporting boundary. Personal reflection stays with the participant outside AI context, the employer report, Git, and shared programme records. Collect no health, religion, trauma, personality, or emotion data.
4. For a research claim, route the source through `$ana-research-library` and attach its entry reference, evidence class, supported claim, and limitation. A useful framework is not proof that this programme works. Facilitator-designed reflection prompts are labelled practice hypotheses, not neuroscience or treatment.
5. Adapt [the practice plan](assets/practice-plan.md) and [synthetic record](assets/practice.example.json) privately. Validate from this skill directory:

```bash
python scripts/validate_practice.py <private-practice.json>
```

6. Return a draft run sheet, a participant-facing choice notice, an aggregate measurement plan, evidence limitations, validation findings, and the next named owner. Validation never authorizes delivery, collection, employer sharing, or an external send.

## Integration

- `$ana-hr-operations` remains the engagement coordinator; use SOP-02 for scope, SOP-04 for an approved offer, and SOP-06 for invoice reconciliation. Do not add billing logic here.
- `$ana-template-studio` receives an approved engagement-stage receipt before producing a client document. Until then use a private Markdown draft; a validated practice record is not a substitute stage receipt.
- `$agency-productization` can package a repeat delivered practice after outcomes and usage rights have been reviewed.
- `$ana-approved-content` receives only approved, de-identified outcome summaries and independently approved teaching material. Never repurpose private reflection, workshop audio, or client stories into content by default.
- A community or venue workflow may receive only programme ID, approved capacity/date needs, owner, accessibility/logistics requirements, and scope. Agreements, occupancy, deposits, and participant identities remain in their designated private systems.

## Boundaries that change decisions

Keep voluntary reflection and spiritual practices optional and separate from employer objectives. A secular equivalent must be equally available with no penalty. Do not imply psychotherapy, mental-health treatment, diagnosis, brain rewiring, clinical outcomes, professional credentials, employee fit, emotion recognition, or personality inference. Separate any proposed clinical service into an appropriately qualified practitioner's own scope; this skill cannot design it.

Use task-level quality and time evidence, never employee rankings. Small-group aggregates can still identify people: the default reporting floor is five consenting participants, with stricter suppression when context exposes identity. The threshold is a product safeguard, not a legal anonymity guarantee. Participant choice is not itself a determination of lawful workplace data processing.

## Completion receipt

Return `DRAFT_REVIEW_REQUIRED`, scope, facilitator and sponsor, evidence class/limits, raw outcome denominators and quality baseline, reporting/suppression decision, resource ceilings, unresolved inputs, and next review owner/date. Missing owner facts remain blockers; do not invent approval, pricing, venue readiness, or results.
