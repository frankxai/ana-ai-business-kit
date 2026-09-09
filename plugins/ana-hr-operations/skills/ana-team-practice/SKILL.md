---
name: ana-team-practice
description: Prepare voluntary, non-clinical team working agreements and 30-day follow-through plans from approved team-level facts. Use for role clarity, communication norms, handoffs, and team AI adoption; never use for employee assessment, therapy, or hiring decisions.
---

# Ana Team Practice

Turn a team coordination problem into a facilitated practice, an observable working agreement, and a review date. Ana owns the method and final judgment; a named facilitator owns delivery. Do not invent Ana's signature exercises, qualifications, experiences, or approval.

Read [the session workflow](references/session-workflow.md). Use [the fictional brief](assets/team-practice.example.json) as a schema example, replacing it with approved team-level facts in the private workspace.

Use [the fictional handoff rehearsal](assets/handoff-rehearsal.md) for a concrete exercise and checklist. Confirm checkpoint owners and reconcile agreement review dates with the standard days 7/14/30 checkpoints before delivery.

1. Identify observable friction and the desired working behavior. Use role aliases. Keep employee identities, personal stories, health information, and individual feedback outside this brief.
2. Name the facilitator role, reviewer, voluntary participation notice, and neutral alternative. A manager's approval does not substitute for a participant's ability to decline disclosure.
3. Draft a time-boxed agenda and proposed agreements, owners, and review dates. Evidence-informed facilitation requires source URLs and limitations; route substantive research through `ana-research-library`.
4. Keep spiritual reflection in a separate, individually chosen personal-practice context. Corporate work covers observable collaboration and never collects beliefs or therapeutic disclosures.
5. Validate and render an internal draft:

```bash
python scripts/team_practice.py <private-brief.json> --out <private-draft.md>
```

6. Review free text manually. The helper checks structure and declared boundaries; it cannot establish truth, consent, anonymity, or professional suitability. Passing validation is not approval.
7. Route to `ana-template-studio` for an approved Docs/Canva master. Keep the operator brief internal. Move only human-approved participant material into the existing client-session package or controlled client workspace. Sending requires the separate send gate.

Return the draft, assumptions, evidence limits, proposed agreements, responsible roles, review dates, validation result, and `HUMAN_REVIEW_REQUIRED`. Never record approval, send, schedule, collect participant responses, or write to employer systems.
