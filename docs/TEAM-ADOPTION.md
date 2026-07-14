# Four-person team adoption

This is the operating product for Ana and a four-person team. It is designed so the team can work mainly from Google Drive and Codex; GitHub is for maintained instructions and updates, not daily client work.

## The four seats

| Seat | Primary outcome | Can prepare | Cannot decide or do alone |
| --- | --- | --- | --- |
| **Ana — manager and approver** | Quality, client trust, scope, risk, and commercial control | Manager board, approval review, escalation, final artifact review | Delegate final hiring decision, price, invoice, publication, or external send to AI |
| **Engagement coordinator** | Every client has a next action, owner, date, and clean kickoff | First-call capture, board updates, meeting preparation, follow-up draft | Approve scope, price, invoice, or send; edit master templates |
| **Research and recruiting operator** | Job-relevant research, scorecard/process readiness, and traceable sources | Research library entries, role evidence, aggregate pipeline updates, weekly status draft | Make a candidate decision, retain candidate data outside the ATS, turn neuroscience/personality into a selection signal |
| **Document and client-experience operator** | Template fidelity and clean client experience | Content pack, copied Google Doc/Canva draft, visual-check card, client-facing draft | Edit a master, publish, send, approve a commercial number, or claim a visual check that did not happen |

One person may temporarily cover two seats, but the approval separation still applies: the person who prepared a commercial/client-facing item does not silently self-approve it.

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

## First month adoption

### Day 0 — set the guardrails (45–60 minutes)

1. Assign the four seats and backup owners.
2. Create the Drive folder structure in [Workspace and template architecture](GOOGLE-WORKSPACE-AND-TEMPLATES.md).
3. Set up the private template registry and identify the real kickoff, offer, invoice, and Canva presentation masters.
4. Confirm where candidate data, client data, and finance information actually live.
5. Install the plugin on the team members' individual Codex accounts; do not paste credentials into any prompt.

### Week 1 — practice, not production

1. Run [the fictional practice engagement](PRACTICE-ENGAGEMENT.md) together.
2. Each role uses its prompt from [Team starter prompts](TEAM-STARTER-PROMPTS.md).
3. Ana runs the manager morning control and approval review.
4. Record only learnings about the process in the private overlay—no client data.

### Week 2 — one live pilot

1. Pick one appropriate, low-complexity engagement with a clear client data boundary.
2. Use one private engagement record and the existing template masters.
3. Keep candidate identities and interview evidence in the ATS.
4. Stop at every approval gate. A slow, well-receipted first run is a successful run.

### Weeks 3–4 — stabilize

1. Review bottlenecks, unclear ownership, template issues, and repeated questions.
2. Update the private template registry, prompts, and team guide—not the public repository with client-specific content.
3. Run a second practice case if the template or approval process changed materially.
4. Decide whether to expand to a second client only after Ana signs off on the pilot review.

## Ana-only manager controls

These are explicit prompts, not automated commands. Use them in a fresh task with private records accessible only through approved systems.

| Control | Prompt outcome | Always stops before |
| --- | --- | --- |
| **Morning control** | Alias-only board: stage, owner, due date, blocker, approval need, template state | Creating tasks, changing records, messaging clients |
| **Approval review** | Exact artifact, source facts, assumptions, calculations, recipient, and requested decision | Recording approval without Ana's words |
| **Exception review** | Stale work, sensitive-data risk, template block, money mismatch, client ambiguity | Fixing or sending anything automatically |
| **Weekly quality review** | Trends in completeness, evidence quality, reusable process improvements | Candidate ranking, performance diagnosis, or policy/legal conclusions |

Use the prompts in [Start Here](../START-HERE-ANA.md). A manager control produces a decision card; it does not itself grant approval.

## Definition of adoption success

The team is ready for normal use when it can demonstrate, on a fictional case:

- one correct owner and next action for every engagement;
- a copied—not edited—master template route for kickoff, offer, invoice, and presentation;
- `TEMPLATE_BLOCKED` or `CANVA_RENDER_PENDING` when the required source/check is missing;
- clear evidence sources and no unsupported claims;
- no candidate or finance data in GitHub or the cross-client board;
- a named Ana approval before price, invoice, publication, or external handoff;
- a concise receipt after every SOP.
