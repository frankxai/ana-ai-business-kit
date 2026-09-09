# Agency pilot operating runbook

Status: ready for an internal fictional rehearsal; live and commercial gates remain open. All targets are proposed. This runbook turns the [product requirements](HR-EXCELLENCE-PRD.md) and [scorecard](EXCELLENCE-SCORECARD.md) into an operator's evidence trail.

## First cohort

Use one agency, one coordinator, one invoice reviewer, one existing finance system, and one repeatable engagement type. A second agency must use its own identity, policy, template registry, records, and local ledger. The shared plugin must require no code changes. This tests setup portability; it does not establish hosted tenant isolation.

Ana owns method and service quality. Her named delegate may prepare the review queue. Frank owns source quality and technical support. These are proposed operating responsibilities; record actual accepted assignments privately before the pilot starts.

## Start conditions

| Gate | Evidence to record privately | If absent |
| --- | --- | --- |
| Product scope | One buyer, outcome, engagement type, exclusions, and responsible operator | Scope pending |
| Method and identity | Owner-approved wording, allowed source uses, reviewed biography | No claims in Ana's voice |
| Client authority | Approved purpose, systems, access, and retention for the specific engagement | Fictional records only |
| Templates | Exact master links, copy permissions, required content and visual checks | Local review draft only |
| Finance | Commercial source, event basis, jurisdiction-approved treatment, numbering process, reviewer | No issue/send |
| Release | Source revision, required tests, installation receipt, rollback version | Do not expand beyond rehearsal |

No source approval, client authorization, payment, or consent is created by filling a template or running a validator.

## Rehearsal A — invoice to review receipt

Follow the [local billing review guide](../plugins/ana-hr-operations/skills/ana-hr-operations/references/billing-review.md) with its fictional source and event. The coordinator and reviewer use separate role aliases, even when one person rehearses both roles.

1. Register the fictional event against the exact source file. Try a changed source; it must fail.
2. Prepare and export the invoice draft. Compare identity, items, terms, total, event basis, and destination with the source.
3. Record a local review acknowledgment for that exact revision. The result must still say `authenticated: false` and `external_send_allowed: false`.
4. Repeat the same preparation request. It must return the same revision and reserve no second invoice.
5. Change payment terms or recipient, prepare again, and attempt to use the old review receipt. It must fail. Restoring older content must require a fresh revision and review.
6. Edit the exported artifact. The check must fail. Export the persisted artifact to a new path to recover.
7. Attempt to use the invoice number for a different event. It must fail in that ledger.
8. Stop at local review. Record failures and recovery steps. No finance provider record or customer message should exist from this exercise.

The exercise passes only when the operator explains why a local acknowledgment cannot authorize a provider issue/send. A second ledger cannot prevent duplicates in the first; the finance provider remains authoritative.

## Rehearsal B — team working agreements

Use the [fictional handoff exercise](../plugins/ana-hr-operations/skills/ana-team-practice/assets/handoff-rehearsal.md) and the team-practice example. The facilitator prepares a session; a second practitioner reviews the agenda, participant choices, language, exercise, and follow-through owners.

Success evidence: the team can state one observable handoff problem; the session produces a behavior, role owner, due date, and review point; a participant can choose a work-example-only or observer route. Keep personal reflection outside sponsor reporting. This is a rehearsal of usable facilitation, not evidence of therapeutic or neuroscience outcomes.

## Live proof, once authorized

Start with three engagements and manual entry into the existing finance system after its normal human approval. The ledger can hold preparation evidence in an approved private location; it has no authenticated identity, encryption, or tamper-resistant audit boundary. Its use with real billing material requires the agency's existing access and retention controls. Do not copy the local acknowledgment into a provider as authenticated authorization.

Capture ten comparable baseline drafts before making a speed claim. Match task type and complexity. Capture every pilot attempt, including failure, rework, and abandoned drafts. At least twenty reviewed pilot drafts are needed before assessing the proposed 90% first-pass threshold. Keep paid pilot acceptance and payment evidence separate from technical rehearsal results.

## Measurement workbook

Copy the blank [draft observation CSV](templates/pilot-draft-observations.csv) to an approved private workbook. The public template contains no observations. Use one row per attempt, never overwrite failed attempts, and retain a stable artifact ID across revisions.

| Columns | Meaning |
| --- | --- |
| observation_id, artifact_id, attempt_number | Unique observation, stable draft identity, sequential attempt |
| agency_alias, engagement_alias | Opaque aliases; identities remain in approved systems |
| phase, task_type, complexity_band, comparison_id | `baseline` or `pilot`; match comparable work using a comparison ID |
| outcome | `completed`, `failed`, `pending`, or `abandoned` |
| preparation_minutes, review_minutes, rework_minutes | Active work only; blank means unknown, zero means measured zero |
| reviewed, financially_correct, material_corrections | `true`/`false` or blank for unknown; correction count is a nonnegative integer when measured |
| due_date, accepted_at | Approved due date and accepted handoff date, ISO dates |
| approval_receipt_reference, source_revision | Private evidence reference and exact source version; neither proves authentication |
| failure_category | Arithmetic, source, template, stale review, missing input, or other specified cause |

For each metric retain numerator, denominator, missing count, and observation window. Report `not_measured`, `insufficient_sample`, `pass`, `fail`, or `paused`.

- **Preparation time:** sum preparation and rework minutes over all attempts for each completed artifact. Compare medians of matched baseline and pilot artifacts; report review time separately and also show total human time. Use at least ten matched pairs across three engagements. Unmatched and unfinished artifacts remain visible as counts; they cannot silently disappear from the report.
- **First-pass acceptance:** artifacts accepted on attempt one with zero material corrections / reviewed pilot artifacts, including failed first attempts. Do not count corrected revisions as new successes. Missing review/correction data prevents a pass.
- **Financial correctness:** financially correct reviewed invoice drafts / reviewed invoice drafts. Keep any erroneous reviewed revision in the denominator. Any material error pauses the affected billing route regardless of aggregate score.
- **On-time handoff:** artifacts accepted by their due date / artifacts due in the window. Overdue pending items remain in the denominator; future items do not. Report missing due dates separately.
- **Approval coverage:** consequential actions with a verified current approval in the authoritative process / all such actions. A local ledger acknowledgment alone is insufficient evidence. Unsent rehearsals have no consequential actions and must report `not_measured`, not 100%.

For paid validation, contribution margin, weekly support, and team follow-through, keep the [scorecard's](EXCELLENCE-SCORECARD.md) separate private evidence sources. Do not infer them from this invoice CSV.

## Daily and weekly review

The coordinator records the next action, owner, due date, blocker, and evidence reference for each engagement. Review consequential decisions in one batch where practical; urgent exceptions go to the designated accountable owner.

At the weekly review, show actual counts before percentages. Decide whether to continue the same scope, repair a specific defect, or pause it. Finance or privacy failures cannot be averaged away by good speed or satisfaction scores. Keep founder support time visible even when no invoice is raised for it.

## Exit evidence

The pilot closeout contains: exact plugin revision and installation receipt; fictional rehearsal results; authorized engagement counts; baseline and pilot observations; exceptions and fixes; owner/reviewer decisions; actual support cost; and a continue/change/stop recommendation. A paid product requires a separate method, rights, fulfillment, and seller review. A hosted service additionally requires authenticated approvals, tenant isolation, provider reconciliation, and operational recovery tests.
