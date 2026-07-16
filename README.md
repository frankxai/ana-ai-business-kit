# Ana AI Business Kit

Ana AI Business Kit turns Ana's established HR workflows and approved templates into a shared operating system for client delivery, recruiting, documents, research, and commercial administration. It carries the quality of Ana's method across engagements: capture the right facts once, make ownership visible, preserve the right template, and bring each decision to the right human at the right moment.

AI works backstage: it prepares, reconciles, and checks. Ana's team owns delivery. Each client's named decision-makers retain employment decisions; Ana retains authority over her practice's judgments, scope, pricing, invoices, publication, and external communication.

## What the system strengthens

| Work | Codex prepares and checks | Named human decides |
| --- | --- | --- |
| First call and kickoff | Structured capture, open decisions, owners, dates, and a readback | Ana confirms scope and data boundary |
| Role and recruiting process | Job-relevant scorecard, inclusive job description, structured process | Client and Ana make human employment decisions |
| Offer and invoice | Source-linked calculations, draft copy, template route, reconciliation | Ana approves price, wording, invoice facts, and destination |
| Documents and Canva | Copy-master route, content pack, readback, visual-check state | Ana approves final content and template fidelity |
| Research and team practice | Evidence library, applicability notes, workshop/research draft | Ana decides what is appropriate to use or teach |
| Content | Accurate, approval-gated draft using approved sources | Ana approves publication and any send |

The plugin includes four complementary skills:

| Skill | Job |
| --- | --- |
| `ana-hr-operations` | Consistent client delivery, recruiting operations, documents, commercial preparation, and handoffs |
| `ana-template-studio` | Validated content-pack-to-Google-Docs/Canva execution, candidate selection, readback, visual checks, and approval cards |
| `ana-research-library` | Evidence capture and a safe research library for HR, recruiting, team practice, and voluntary workshop preparation |
| `ana-approved-content` | Approval-gated, source-backed content drafts; it never publishes or sends |

## Pair the method with official Codex plugins

Ana HR Operations defines **how the team works**. OpenAI-curated plugins provide approved access to systems such as Google Drive, Canva, Gmail, Calendar, Slack, and GitHub. They are separate on purpose: a connector can retrieve or prepare information, while Ana's plugin applies the SOP, privacy boundary, stop state, and human approval.

Use the [Codex plugin stack for Ana's team](docs/OFFICIAL-CODEX-PLUGIN-STACK.md) to choose the minimum plugins for each role, connect approved individual accounts, rehearse safely, and improve the shared method through reviewed changes.

## Begin with Ana's operating method

1. Ana starts with [her operating overview](START-HERE-ANA.md).
2. The team uses [its operating page](START-HERE-TEAM.md), [role and authority map](docs/TEAM-ADOPTION.md), and [ownership map](docs/WHO-READS-WHAT.md).
3. Keep live work inside the [controlled Drive architecture](docs/GOOGLE-WORKSPACE-AND-TEMPLATES.md), approved ATS, Canva, and finance systems.
4. Connect Ana's real masters privately through [template and Canva routing](docs/TEMPLATE-AND-CANVA-ROUTING.md).
5. Validate the complete route with the fictional [release rehearsal](docs/PRACTICE-ENGAGEMENT.md) before applying a new system version to live work.

## Existing templates stay in charge

Ana's existing kickoff, offer, invoice, and presentation masters are the design authority. The kit supplies quality gates, content mappings, and prompts—not a generic replacement template.

- Google Docs: exact master → copy only → small verified edits → connector readback → human content/template approval.
- Canva: exact master → copy only → approved content pack → Canva visual check → human approval. The status stays `CANVA_RENDER_PENDING` until visual review is recorded.
- Starter Canva route: generated candidates → user selection → editable design → named visual check. It is practice-only until Ana promotes an exact master.
- Google Sheets: controlled private workbook for aliases, task state, approvals, and fictional practice data; candidate identities remain in the ATS.

See [Template and Canva routing](docs/TEMPLATE-AND-CANVA-ROUTING.md), [Template Studio v1.2](docs/TEMPLATE-STUDIO-V1.2.md), and [Workspace architecture](docs/GOOGLE-WORKSPACE-AND-TEMPLATES.md).

## Technical activation

Technical setup follows the operating decisions above. Use [the install and private-overlay guide](docs/FORK-AND-INSTALL-CODEX.md) and [official plugin stack](docs/OFFICIAL-CODEX-PLUGIN-STACK.md), then install the maintained public plugin:

```powershell
codex plugin marketplace add frankxai/ana-ai-business-kit --ref main
codex plugin add ana-hr-operations@ana-business-kit
codex plugin list
```

Start a new Codex task after installation. Run a public-safe rehearsal first:

[Install from Ana's web guide](https://www.frankx.ai/allies/ana-cancino#install) · [Open Ana HR Operations in Codex](codex://plugins/ana-hr-operations@ana-business-kit) · [Browse OpenAI-curated plugins](codex://plugins/install/?marketplace=openai-curated)

The Codex link works after the marketplace has been added. If GitHub or the browser does not activate application links, open **Codex → Plugins** manually.

> Use Ana HR Operations. Start a private fictional engagement and guide me through the first call using SOP-01. Separate facts from assumptions. Do not create, send, schedule, price, invoice, or publish anything.

## What is safe to put in GitHub

Only public-safe instructions, blank templates, schemas, test fixtures, and fictional examples belong here. Real client records, template URLs, candidate material, internal policy, real pricing, invoices, and credentials do not.

For private customization, create a **separately initialized private company overlay repository** and controlled Drive workspace. Do not use a public fork as a private storage mechanism. Details and update flow are in [Fork, private overlay, and install](docs/FORK-AND-INSTALL-CODEX.md).

## Optional facilitation downloads

These legacy-compatible ZIPs support a separate facilitation workflow. They are not the primary path for Ana's ongoing HR operations; the installed Ana HR Operations plugin is.

| Item | Audience | Boundary |
| --- | --- | --- |
| **Ana HR Operations plugin** | Ana and the internal HR team | Main recurring workflow; never client/candidate data in repo |
| **Ana Operator Kit ZIP** | Ana/internal practitioners using the optional facilitation workflow | Practitioner-only; not client-sendable |
| **Client Session Kit ZIP** | A client after review | Client-safe preparation and aftercare material |

Create the two ZIPs locally only when ready to release:

```powershell
npm run package
```

The archives and SHA-256 checksums are created in `dist/` and are intentionally not committed.

## Repository map

```text
plugins/ana-hr-operations/       # installable plugin: HR operations + research + approved content skills
packages/ana-operator-kit/       # public-safe practitioner ZIP source; real work remains private
packages/ana-client-session-kit/ # client-safe ZIP source
docs/                            # team roles, Drive, Canva, release rehearsal, updates, adaptation guides
scripts/                         # validation and reproducible packaging
```

## Quality and privacy controls

- Do not rank or reject candidates from protected traits, personality proxies, neuroscience, emotion inference, or medical information.
- Use job-relevant, structured evidence and keep a named human accountable for the final decision.
- Never infer Ana's approval from silence.
- Require exact template source, destination, and copy approval before a final document route.
- Do not invent prices, tax treatment, credentials, claims, outcomes, testimonials, or client policy.
- Use ethical, transparent persuasion: accurate context, clear scope, a truthful next step, and no false urgency or guarantee.
- Confirm the company's data-processing, retention, access, and deletion rules before using live candidate or employee data with an AI service.

## For maintainers

```powershell
npm test
npm run package
```

`npm test` validates package manifests, plugin structure, SOPs, document gates, research entries, content approval gates, examples, and privacy/money controls.

## License and name use

The templates are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). “Ana”, Ana Cecilia Cancino's name, voice, and identity are not licensed for reuse, endorsement, or impersonation. Replace identity-specific text before adapting this kit for another practitioner or HR company. See [HR agency adaptation](docs/HR-AGENCY-ADAPTATION.md).
