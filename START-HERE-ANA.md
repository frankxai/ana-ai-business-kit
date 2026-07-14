# Start here, Ana

This is your four-person HR operating kit. It helps your team move a client from first conversation to a high-quality, human-approved kickoff, job description, offer, invoice draft, recruiting update, and handoff—without putting client or candidate information in GitHub.

AI prepares, checks, and explains. You remain the accountable manager for your practice: client decision-makers make employment decisions, while you approve your team's recommendations, scope, pricing, invoices, publication, and external communication.

## The simple model

| Layer | What it does | Where it lives |
| --- | --- | --- |
| **SOP** | Tells the team the right order, quality gate, and stop condition. | This plugin |
| **Private engagement record** | Holds the live facts, owner, approvals, and next action for one client and role. | Ana's approved private workspace |
| **Master template** | Holds the exact design for kickoff, offer, invoice, or presentation. | Controlled Google Drive or Canva |
| **Approval record** | Shows who approved what, when, and what is still blocked. | Private engagement record + control workbook |
| **Final artifact** | A copied, checked draft or approved client document. | Client engagement folder |

The point is not to make the team technical. They work from Google Drive and Codex. GitHub is the maintained operating manual and update source; Ana or an explicitly approved technical maintainer keeps the private company overlay.

Give each teammate [Start Here for the Team](START-HERE-TEAM.md). The role-by-role reading and ownership map is in [Who reads what](docs/WHO-READS-WHAT.md).

## First 45 minutes

1. Read [Team adoption](docs/TEAM-ADOPTION.md) together and choose the four role owners.
2. Create the private Drive structure exactly as described in [Workspace and template architecture](docs/GOOGLE-WORKSPACE-AND-TEMPLATES.md). Do not move live client or candidate data into this repo.
3. Put the approved kickoff, offer, invoice, and presentation masters in **01 Master Templates**. Make each one view-only for the wider team; copies are edited in the relevant engagement folder.
4. Complete a private template registry using [the example registry](plugins/ana-hr-operations/skills/ana-hr-operations/assets/template-registry.example.json). Keep real links in the private overlay only.
5. Install the HR plugin using [the corrected install guide](docs/FORK-AND-INSTALL-CODEX.md), then start a **new Codex task**.
6. Run the fictional [practice engagement](docs/PRACTICE-ENGAGEMENT.md) before using a live client. It deliberately uses made-up names and no candidate data.

## Daily rhythm

### Ana — manager control

Use these as plain-language prompts in a new Codex task. They are manager controls, not autonomous slash commands.

> Use Ana HR Operations. Run manager morning control for our private engagement records. Show only client aliases, current stage, owner, due date, blocker, approval needed, template status, and the next action. Do not create, send, price, invoice, publish, or change records.

> Use Ana HR Operations. Run the approval review. For each request, show the exact artifact, source facts, unresolved assumptions, template/readback status, named recipient if relevant, and the single approval I am being asked to give. Do not treat this review as approval.

> Use Ana HR Operations. Run a quality and exceptions review. Flag stale records, missing owners, missing template routes, money mismatches, sensitive-data risk, unsupported claims, and anything that needs my decision.

Only after you actively say "I approve [specific decision]" with the relevant facts should Codex record an approval. Silence, a thumbs-up in an old thread, or a general preference is not approval.

### Team members

Each person uses a fresh task and their role prompt from [Team starter prompts](docs/TEAM-STARTER-PROMPTS.md). The coordinator owns the next action; the research operator owns source quality; the document operator owns template fidelity. Nobody makes an employment decision, commercial commitment, or external send through the system.

## Your existing great templates

Your real kickoff, offer, invoice, and Canva presentation templates are the source of visual quality. This kit never replaces them with generic AI styling.

- **Google Docs templates:** Codex reads the exact master, makes a copy, changes only the copy in small verified batches, re-reads it, and reports whether visual page inspection happened.
- **Canva offer, invoice, and presentation templates:** the team provides the exact approved Canva master inside a private task; creates a copy; prepares a content pack from approved facts; then performs a human visual check in Canva. Codex must report `CANVA_RENDER_PENDING` until that check is complete.
- **No exact template link, no final document:** the correct result is `TEMPLATE_BLOCKED`, not an invented document. The full route is in [Template and Canva routing](docs/TEMPLATE-AND-CANVA-ROUTING.md).

## One first live engagement

When the practice engagement passes, use this prompt with the real client facts only in Ana's approved private workspace:

> Use Ana HR Operations. Create or open the private engagement record for one client and one role. Select SOP-01 and guide me through the first-call capture one section at a time. Separate facts, assumptions, owners, due dates, template route, and approvals. Keep candidate information in the approved ATS. Do not send, schedule, set price, create an invoice, or publish anything.

Then use the system in this order:

> first client call → confirmed kickoff → job description and/or service offer → approved price → invoice draft → approved handoff

## What lives where

| Information | Correct home |
| --- | --- |
| Plugin instructions, blank schemas, fictional practice material | This public-safe repository |
| Real template links, company policy, internal notes | Separate private company overlay |
| Master Google Docs and Canva templates | Controlled Drive/Canva master folder |
| Live engagement record and client files | Private client engagement folder |
| CVs, interview evidence, candidate identity, employment data | Approved ATS/HR system only |
| Finance credentials and bank details | Approved finance system only |
| Daily cross-client view | Private control workbook, aliases only |

## What Codex is doing underneath

For every request it should:

1. select one named SOP instead of improvising;
2. check its entry criteria and stop with an exception code if something is missing;
3. use the right connector: Google Docs for Docs, Canva for visual masters, Google Sheets for the control workbook, and Gmail/Calendar only after a fresh approval gate;
4. create or validate a private record; run its validation; and preserve the source of each important fact;
5. produce a receipt: what changed, what is still blocked, approvals present/missing, template status, and next owner.

That gives your team consistency without asking them to learn Markdown, Git, or a technical agent framework in daily work.

## Updates and support

Use [Release and update checks](docs/RELEASE-AND-UPDATE.md) once per month or before a new teammate starts. Changes should be trialled on the fictional practice engagement first. Keep real policy and template changes in the private overlay, never in a public fork.

The optional Operator and Client Session ZIPs remain separate from the HR plugin. See the repository README for their audience boundary.
