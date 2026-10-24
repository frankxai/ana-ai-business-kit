# Connected specialist team

One coordinator owns the work graph and the consolidated owner brief. Specialists receive a bounded job and the minimum authorized source context. They return artifacts and evidence to the coordinator. No specialist can delegate itself authority.

| Specialist | Preparation responsibility | Human accountability | Completion evidence |
| --- | --- | --- | --- |
| Knowledge curator | Current source registry, conflicting/stale facts, reusable FAQ drafts | Coordinator; agency owner approves method changes | Cited answer or explicit unknown, source/version, review owner |
| Talent operations | Requisition readiness, authorized factual retrieval, missing evidence, follow-up and interview preparation | Talent operator; client owns hiring decisions | ATS reference, job-related evidence source, next owner/date |
| Commercial | New service opportunity, approved scope and service-offer pack | Document operator; agency owner approves terms | CRM/engagement source, catalog version, open commercial decisions |
| Meeting coordinator | Pre-read, status digest, decision question, owner/date, async replacement proposal | Coordinator; meeting organizer owns calendar changes | Reviewed work-only decisions and proposed tasks |
| Finance | Billable-event reconciliation and exact invoice revision | Document/finance operator; named human finance approver | Existing billing validation and review receipt |
| Document quality | Master-copy preparation, source fidelity, artifact/readback checks | Document operator; named reviewer approves client output | Artifact revision and explicit content/visual-check status |

The planner's specialist names describe roles, not six persistent employees or running services. A person can hold multiple human remits. A separate review step remains explicit even when an agency is small.

## Handoff packet

Each dispatch specifies task ID, agency/engagement scope, purpose, specialist, responsible human, exact source versions, requested output, dependencies, allowed preparation actions, and approval boundary. Record a task budget and deadline in the host runtime. Default to one pass and one targeted repair; escalate unresolved source or authority conflicts.

Read/draft preparation can run concurrently when inputs are independent. Default ceiling: three simultaneous preparation workers across the agency, not three for each client. This is a starting resource budget, not a performance benchmark. Use one worker when the job is small. Dependent work waits for a verified artifact receipt; a model's “done” message is insufficient.

The local planner returns ready dispatch groups only after its declared dependencies are completed. It does not make future dependencies complete or run the groups. The host must resolve source references, enforce permissions, execute workers, read back artifacts, and update the authoritative task record.

## Tool and state boundary

Phase one uses existing company-approved connectors in an initiated host session. Bind every actual action to the current user and resource. Connector availability in Frank's workspace does not establish access to Ana's company or any client. A shared owner token must not be distributed to all agents.

An always-on runtime needs authenticated work items, resource scopes, durable task state, idempotency, event deduplication, a transactional outbox for mutations, provider readback, and a retry/reconciliation queue. Keep credentials outside prompts. Limit tool names and destinations in executable policy; a prompt-only allowlist is insufficient.

Use the ATS/CRM/task system's provider IDs as authoritative references. Domain events such as requisition updated, source superseded, review requested, and handoff accepted drive preparation. Do not poll every folder and send repeated updates simply because a schedule fired.

## Worker return contract

Return task ID, status (`draft_ready`, `blocked`, or `failed`), source versions actually read, artifact reference and digest where available, unresolved facts, requested human decision, runtime/provider receipt, and measured time/cost when exposed. Never fill unknown cost or completion with zero. Record failures and canceled work.

The coordinator rejects results with a different agency, engagement, source version, destination, or unapproved scope. Re-check permission immediately before a consequential action. A quality worker may flag defects; it cannot impersonate a human approver or authorize an external send.

## Operational stop conditions

Stop the affected task when source permission changes, an input version is superseded, arithmetic fails, provider state is ambiguous, or the worker exhausts its budget. Preserve the task and evidence; do not create a new ID to evade retry controls. No hiring decision, signed term, invoice issue, external message, or calendar cancellation may emerge solely from specialist consensus.
