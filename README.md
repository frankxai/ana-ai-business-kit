# Ana AI Business Kit

Ana's private HR operating system for moving a new client from the first client call to a reviewed kickoff, job description, service offer, price, and invoice draft.

AI prepares and checks the work. Ana remains the decision-maker and approves every price, invoice, hiring judgment, and external message.

## Ana, start here

1. Read [Start Here for Ana](START-HERE-ANA.md).
2. Follow [Fork and install in Codex](docs/FORK-AND-INSTALL-CODEX.md).
3. Connect Ana's real template with [Google Docs setup](docs/GOOGLE-DOCS-SETUP.md).
4. Run one client through [the first-client walkthrough](docs/FIRST-CLIENT-FLOW.md).

The shortest install is:

```powershell
codex plugin marketplace add frankxai/ana-ai-business-kit --ref main
codex plugin add ana-hr-operations@ana-business-kit
codex plugin list
```

Start a new Codex task after installation. Ask:

> Use Ana HR Operations. Start a new client engagement and guide me through the 20–30 minute first-call capture. Do not send, schedule, price, or invoice anything without my explicit approval.

## What the system handles

| Stage | Codex prepares | Ana decides |
| --- | --- | --- |
| First call | Structured notes, missing questions, owners, and dates | What is accurate and appropriate to retain |
| Kickoff | Scope, stakeholders, cadence, selection process, privacy, and next actions | Final scope and accountable people |
| Job description | Role outcome, responsibilities, evidence, and structured criteria | Hiring requirements and final wording |
| Service offer | Deliverables, exclusions, timing, and commercial summary | Scope, price, currency, tax, and payment terms |
| Invoice | A mathematically checked draft linked to an approved offer or milestone | Invoice number, billing facts, approval, and whether to send |
| Handoff | A status summary and optional email draft | Exact recipient, channel, and send approval |

The plugin does not make candidate decisions, invent prices, edit Ana's master template, or send anything automatically.

## Built-in SOP help system

The plugin selects and receipts one named procedure instead of improvising:

| SOP | Procedure |
| --- | --- |
| `SOP-00` | Daily multi-client control board and approval queue |
| `SOP-01` | Time-boxed 20–30 minute first client call |
| `SOP-02` | Client kickoff and engagement activation |
| `SOP-03` | Role scorecard and inclusive job description |
| `SOP-04` | Time-boxed service offer and pricing approval |
| `SOP-05` | Recruiting launch, delivery, weekly status, and change control |
| `SOP-06` | Invoice draft and financial reconciliation |
| `SOP-07` | Approved document, email, or administrative handoff |

Each SOP defines entry criteria, numbered actions, exit criteria, required evidence, and exception codes. See the [SOP routing index](plugins/ana-hr-operations/skills/ana-hr-operations/references/sop-index.md).

## One plugin and two optional ZIPs

These are three different tools, not three versions of the same thing.

| Item | Who uses it | When it is useful |
| --- | --- | --- |
| **Ana HR Operations Codex plugin** | Ana and her internal HR team | The main recurring workflow for recruiting clients, documents, pricing, invoices, and administration |
| **Ana Operator Kit ZIP** | Ana privately | A lightweight offline workspace for offers, reflective sessions, workshops, and approved aftercare |
| **Client Session Kit ZIP** | A client | A clean preparation and aftercare packet that needs no AI account |

So: keep the two ZIP downloads because they have different audiences, but Ana only needs to install the Codex plugin for her HR operations. A client never receives the plugin, private operator prompts, engagement records, or candidate data.

Create the two ZIPs locally with:

```powershell
npm run package
```

The archives and SHA-256 checksums are created in `dist/` and are intentionally not committed.

## What Ana needs before the first live client

- Codex in the ChatGPT desktop app or Codex CLI.
- The plugin installed and visible as `ana-hr-operations@ana-business-kit`.
- The Google Drive plugin connected if she wants the final document in her real Google Docs template.
- The exact master-template URL, a comparable finished document when available, a destination folder, and permission to create a copy.
- A private, company-approved location outside this repository for engagement records and candidate material.

Google Drive is optional for the first local draft. If it is not connected, the plugin creates a clearly labeled Markdown draft and reports `TEMPLATE_BLOCKED` instead of pretending the Google Doc is finished.

## Privacy and control

- Never commit client names, contact details, CVs, recordings, interview notes, IDs, health data, bank details, or real engagement records.
- Give Codex only the minimum information needed for the current task.
- Use job-relevant evidence. Do not rank or reject candidates from protected traits or personality proxies.
- Never infer Ana's approval from silence.
- Require explicit approval before changing price, finalizing an invoice, emailing, scheduling, or sending a document.
- Confirm the company's data-processing and retention requirements before using any live candidate or employee data with an AI service.

## Repository map

```text
plugins/ana-hr-operations/   # installable Codex plugin, SOPs, gates, and templates
packages/ana-operator-kit/   # private operator ZIP source
packages/ana-client-session-kit/ # client-safe ZIP source
docs/                        # Ana's install and operating guides
scripts/                     # validation and reproducible packaging
```

## For maintainers

```powershell
npm test
npm run package
```

`npm test` checks the two package manifests, plugin marketplace, required guides, workflow resources, money/send gates, and example engagement record. See [plugin internals](plugins/ana-hr-operations/skills/ana-hr-operations/SKILL.md) for the operating contract.

## License and name use

The templates are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). “Ana”, Ana Cecilia Cancino's name, voice, and identity are not licensed for reuse, endorsement, or impersonation. Replace identity-specific text before adapting this kit for another practitioner or HR company.
