# Local agency planner contract

Schema: `agency-control/v1`. Python standard library only. This is a deterministic metadata/workflow planner, not a retrieval engine, permission service, agent host or calendar adapter.

## Invocation

Run from this skill directory with Python 3.12, the CI runtime:

```bash
python scripts/agency_control.py validate assets/agency-control.example.json
python scripts/agency_control.py plan assets/agency-control.example.json --out /tmp/agency-control-demo.md
```

`validate` checks structure and references. Valid input can still contain blocked work. `plan` prints the JSON plan and optionally creates a Markdown draft. Repeating export with identical content is accepted; an existing different file is preserved. The parent output directory must exist. For live records use an approved private location, never Git or a shared temporary directory.

## Input

| Record | Exact fields |
| --- | --- |
| Root | `schema_version`, `agency_alias`, `as_of`, `sources`, `tasks`, `meetings` |
| Source | `source_id`, `agency_alias`, `engagement_alias`, `kind`, `reference`, `version`, `owner_role`, `updated_at`, `review_due`, `access_state` |
| Task | `task_id`, `kind`, `engagement_alias`, `due_date`, `status`, `source_refs`, `depends_on`, `decision_question` |
| Task source reference | `source_id`, `version` |
| Meeting | `meeting_id`, `purpose`, `task_ids`, `planned_minutes`, `attendee_count`, `async_ready`, `requires_live` |

Identifiers are bounded opaque tokens. Dates are explicit ISO calendar dates; `as_of` is the supplied snapshot date, not proof of current source inspection. Source review deadlines cannot precede update dates. An update after `as_of` blocks planning from that source. Access declarations are `confirmed`, `unknown`, or `revoked`; live connector permission still requires independent verification.

Source `engagement_alias` must match the task for engagement-specific sources. The reserved `agency-wide` scope is permitted only for company-policy, service-catalog and talent-index sources. A shared talent pool still requires matching engagement context for candidate follow-up or an employment offer. A source from another engagement in the same agency is blocked.

The source domain is company-policy, service-catalog, engagement, talent-index, meeting-note, personal-reflection, or clinical. The last two are deliberately accepted as registry metadata so the planner can block employer use; their content is never supplied. Task and meeting enums are illustrated by the fictional example and maintained in the script. Unknown fields, duplicate JSON keys/IDs, malformed dates/booleans/numbers, unknown references and dependency cycles fail validation.

Every task needs at least one source. Pipeline work requires a talent index; candidate follow-up and employment-offer preparation require talent-index plus engagement context; service-offer preparation requires service-catalog plus engagement; invoice review, client handoff, status updates and meeting decisions require engagement context. Fresh but irrelevant sources cannot make a task ready.

## Planning states

- `BLOCKED`: a required source/domain is unavailable, outside the agency, forbidden, stale, from the future, unconfirmed/revoked, or on a different version.
- `WAITING_ON_DEPENDENCY`: current inputs exist, but prerequisite work is not completed under the snapshot checks.
- `COMPLETED`: supplied completion state with valid current inputs and dependency treatment; not proof that a real worker executed.
- `READY`: eligible for a proposed preparation handoff, subject to live source/identity checks.

Blocked tasks expose generic blocker codes without reproducing source references or decision text from those tasks. This local projection is not a security perimeter or a detector for personal information hidden in free text. Inputs themselves must already be appropriate for the operator's context.

`decision_question` is required for service-offer, employment-offer, invoice-review and meeting-decision work. These are proposed questions, not approval. Decision cards explicitly remain `DRAFT_QUESTION_PREPARATION_REQUIRED`; the helper has not verified an actual reviewable offer, invoice or decision artifact. Preparers and decision owners are separate: document operators prepare commercial/finance/handoff work, talent operators prepare employment-offer work, and the appropriate agency/client owner decides.

## Output and host handoff

JSON includes tasks, blocker/waiting state, overdue/due/upcoming markers, decision cards, proposed dispatch groups, handoff packets and meeting triage. Each packet contains scope, exact source versions, specialist, responsible human, requested outcome, allowed preparation actions and a return contract. A read/draft action ceiling does not itself authorize either action.

Groups contain at most three tasks for a specialist. `host_max_concurrent_workers: 3` is a proposed ceiling across the host, not enforced concurrency or proof any worker ran. The host must enforce that budget, verify source permissions/versions, execute a permitted task, read back the result and retain its receipt.

All output states retain `authenticated: false` and `external_actions_allowed: false`. No provider API, automated approval, employee assessment, external message or calendar mutation exists in this helper.

## Meetings and opportunity

Interviews, relationships, workshops, conflict, care and explicit live-required meetings stay `KEEP_LIVE`. Other meetings with blocked/unresolved pre-read tasks need `REPAIR_PRE_READ`. Eligible current tasks plus an explicit `async_ready` declaration allow an `ASYNC_CANDIDATE` or `ASYNC_DECISION_CANDIDATE` proposal. Completed/current inputs may support a pre-read; stale completed inputs cannot.

Pre-read readiness is explicitly `DECLARED_READY`, `READINESS_NOT_DECLARED`, or `REPAIR_REQUIRED`. No actual pre-read artifact is verified by this helper. Every recommendation requires organizer authorization before changing a real event. Opportunity sums the supplied scheduled duration and duration × attendee count for eligible meetings. Replacement async work is excluded, and `actual_saved_minutes` stays null. The fictional example is a test scenario, not an estimate of Ana's calendar.

See [asynchronous decisions](async-decisions.md) for actual measurement and [connected team](agent-team.md) for runtime responsibilities.
