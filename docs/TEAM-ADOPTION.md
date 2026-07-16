# Team operating roles and authority

This role map turns Ana's established way of working into visible ownership, decision rights, and clean handoffs. It defines four operating remits, not a required headcount: an experienced operator may own more than one remit, while approval separation and named accountability remain intact.

Daily delivery stays in Google Drive, the approved ATS, Canva, and Codex. GitHub maintains public-safe operating instructions and updates; it is not the team's live client workspace.

The [official Codex plugin stack](OFFICIAL-CODEX-PLUGIN-STACK.md) maps each operating remit to the minimum connectors it needs and provides the safe rehearsal prompts. Do not grant the whole team every connector by default.

## Four operating remits

| Operating remit | Primary outcome | Can prepare | Cannot decide or do alone |
| --- | --- | --- | --- |
| **Ana — manager and approver** | Quality, client trust, scope, risk, and commercial control | Manager board, approval review, escalation, final artifact review | Delegate final hiring decision, price, invoice, publication, or external send to AI |
| **Engagement coordinator** | Every client has a next action, owner, date, and clean kickoff | First-call capture, board updates, meeting preparation, follow-up draft | Approve scope, price, invoice, or send; edit master templates |
| **Research and recruiting operator** | Job-relevant research, scorecard/process readiness, and traceable sources | Research library entries, role evidence, aggregate pipeline updates, weekly status draft | Make a candidate decision, retain candidate data outside the ATS, turn neuroscience/personality into a selection signal |
| **Document and client-experience operator** | Template fidelity and clean client experience | Content pack, copied Google Doc/Canva draft, visual-check card, client-facing draft | Edit a master, publish, send, approve a commercial number, or claim a visual check that did not happen |

One person may own more than one remit, but approval separation still applies: the person who prepared a commercial or client-facing item does not silently self-approve it.

## Permission matrix

Use named individual accounts. Do not share a Google, Canva, GitHub, Codex, ATS, or finance login.

| Resource / action | Ana | Coordinator | Research & recruiting | Document & client experience | Client | Frank / technical maintainer |
| --- | --- | --- | --- | --- | --- |
| `00 Governance & Team Setup` | Owner | Comment | Comment | Comment | No access | No live access unless Ana grants a specific technical review |
| `01 Master Templates` | Owner/editor | View | View | View | No access | No live access |
| `02 Active Engagements/[alias]` | Editor | Editor | Limited by task/ATS policy | Editor for copied artifacts only | No access by default | No access |
| ATS candidate data | Accountable access | Only if client policy grants it | Only if client policy grants it | No access by default | Per client process | No access |
| Finance profile / bank details | Owner or finance delegate | No access | No access | No access | No access | No access |
| Template registry with real links | Owner/editor | View if needed | View if needed | View if needed | No access | No access |
| Private company overlay repository | Owner/admin | Read if needed | Read if needed | Read if needed | No access | Maintainer only if Ana explicitly invites |
| Approve scope, price, invoice, release, publish, or send | **Yes — named approval** | No | No | No | Client approves only their own designated decisions | No |

This is a starting access design, not legal or security advice. Align it with the client's data-processing terms, local employment law, and Ana's actual systems before live use.

## Activation and assurance sequence

### Establish the control layer

1. Assign a named owner and backup for each operating remit.
2. Create the Drive folder structure in [Workspace and template architecture](GOOGLE-WORKSPACE-AND-TEMPLATES.md).
3. Set up the private template registry and identify the real kickoff, offer, invoice, and Canva presentation masters.
4. Confirm where candidate data, client data, and finance information actually live.
5. Install the plugin on the team members' individual Codex accounts; do not paste credentials into any prompt.

### Validate the route with a fictional release rehearsal

1. Run [the fictional release rehearsal](PRACTICE-ENGAGEMENT.md) across the complete route.
2. Each operator uses the relevant prompt from [Team starter prompts](TEAM-STARTER-PROMPTS.md).
3. Ana reviews the manager control, approval review, and decision boundaries.
4. Record only approved operating decisions and process improvements in the private overlay—no client data.

### Activate one bounded live engagement

1. Select one appropriate, bounded engagement with a clear client data boundary.
2. Use one private engagement record and the existing template masters.
3. Keep candidate identities and interview evidence in the ATS.
4. Stop at every approval gate. A deliberate, well-receipted first run is a successful run.

### Stabilize and extend

1. Review bottlenecks, unclear ownership, template issues, and repeated questions.
2. Classify each improvement as reusable/public-safe or company-specific/private using the [shared improvement loop](OFFICIAL-CODEX-PLUGIN-STACK.md#improve-the-method-without-losing-control).
3. Update the private template registry, prompts, and team guide—not the public repository with client-specific content.
4. Run a second practice case if the template, connector, permission, or approval process changed materially.
5. Decide whether to expand to a second client only after Ana signs off on the pilot review.

## Ana-only manager controls

These are explicit prompts, not automated commands. Use them in a fresh task with private records accessible only through approved systems.

| Control | Prompt outcome | Always stops before |
| --- | --- | --- |
| **Morning control** | Alias-only board: stage, owner, due date, blocker, approval need, template state | Creating tasks, changing records, messaging clients |
| **Approval review** | Exact artifact, source facts, assumptions, calculations, recipient, and requested decision | Recording approval without Ana's words |
| **Exception review** | Stale work, sensitive-data risk, template block, money mismatch, client ambiguity | Fixing or sending anything automatically |
| **Weekly quality review** | Trends in completeness, evidence quality, reusable process improvements | Candidate ranking, performance diagnosis, or policy/legal conclusions |

Use the prompts in [Start Here](../START-HERE-ANA.md). A manager control produces a decision card; it does not itself grant approval.

## Operating readiness standard

Before a workflow version is used with live client material, the fictional release evidence should show:

- one correct owner and next action for every engagement;
- a copied—not edited—master template route for kickoff, offer, invoice, and presentation;
- `TEMPLATE_BLOCKED` or `CANVA_RENDER_PENDING` when the required source/check is missing;
- clear evidence sources and no unsupported claims;
- no candidate or finance data in GitHub or the cross-client board;
- a named Ana approval before price, invoice, publication, or external handoff;
- a concise receipt after every SOP.
