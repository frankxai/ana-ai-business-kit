# Ana AI Business Kit

`v1.1` is a public-safe, four-person adoption product for a human-led HR practice. It turns Ana's existing high-quality Google Docs and Canva templates into a controlled workflow for client discovery, kickoffs, job descriptions, offers, invoices, recruiting delivery, research, and approval-gated content.

It is not an autonomous hiring system. AI prepares and checks work; accountable client humans make employment decisions, while Ana remains accountable for her practice's scope, recommendations, pricing, invoices, publication, and every external send.

## Start here

1. Read [Start Here for Ana](START-HERE-ANA.md).
2. Give the team [Start Here for the Team](START-HERE-TEAM.md) and [Who reads what](docs/WHO-READS-WHAT.md).
3. Set up [the four-person team](docs/TEAM-ADOPTION.md) and [controlled Drive architecture](docs/GOOGLE-WORKSPACE-AND-TEMPLATES.md).
4. Follow [the install and private-overlay guide](docs/FORK-AND-INSTALL-CODEX.md).
5. Run the fictional [practice engagement](docs/PRACTICE-ENGAGEMENT.md) before live work.
6. Use [template and Canva routing](docs/TEMPLATE-AND-CANVA-ROUTING.md) to connect Ana's actual masters privately.

The maintained public install is:

```powershell
codex plugin marketplace add frankxai/ana-ai-business-kit --ref main
codex plugin add ana-hr-operations@ana-business-kit
codex plugin list
```

Start a new Codex task after installation. Ask:

> Use Ana HR Operations. Start a private practice engagement and guide me through SOP-01. Separate facts from assumptions. Do not create, send, schedule, price, invoice, or publish anything.

## The operating system

| Work | Codex prepares and checks | Named human decides |
| --- | --- | --- |
| First call and kickoff | Structured capture, open decisions, owners, dates, and a readback | Ana confirms scope and data boundary |
| Role and recruiting process | Job-relevant scorecard, inclusive job description, structured process | Client and Ana make human employment decisions |
| Offer and invoice | Source-linked calculations, draft copy, template route, reconciliation | Ana approves price, wording, invoice facts, and destination |
| Documents and Canva | Copy-master route, content pack, readback, visual-check state | Ana approves final content and template fidelity |
| Research and team practice | Evidence library, applicability notes, workshop/research draft | Ana decides what is appropriate to use or teach |
| Content | Accurate, approval-gated draft using approved sources | Ana approves publication and any send |

The plugin includes three complementary skills:

| Skill | Job |
| --- | --- |
| `ana-hr-operations` | SOP-led HR client delivery, documents, pricing, invoice drafts, and handoffs |
| `ana-research-library` | Evidence capture and a safe research library for HR, recruiting, team practice, and voluntary workshop preparation |
| `ana-approved-content` | Approval-gated, source-backed content drafts; it never publishes or sends |

## Existing templates stay in charge

Ana's existing kickoff, offer, invoice, and presentation masters are the design authority. The kit supplies quality gates, content mappings, and prompts—not a generic replacement template.

- Google Docs: exact master → copy only → small verified edits → connector readback → human content/template approval.
- Canva: exact master → copy only → approved content pack → Canva visual check → human approval. The status stays `CANVA_RENDER_PENDING` until visual review is recorded.
- Google Sheets: controlled private workbook for aliases, task state, approvals, and fictional practice data; candidate identities remain in the ATS.

See [Template and Canva routing](docs/TEMPLATE-AND-CANVA-ROUTING.md) and [Workspace architecture](docs/GOOGLE-WORKSPACE-AND-TEMPLATES.md).

## What is safe to put in GitHub

Only public-safe instructions, blank templates, schemas, test fixtures, and fictional examples belong here. Real client records, template URLs, candidate material, internal policy, real pricing, invoices, and credentials do not.

For private customization, create a **separately initialized private company overlay repository** and controlled Drive workspace. Do not use a public fork as a private storage mechanism. Details and update flow are in [Fork, private overlay, and install](docs/FORK-AND-INSTALL-CODEX.md).

## Two optional ZIPs

The optional ZIPs solve a different sharing problem:

| Item | Audience | Boundary |
| --- | --- | --- |
| **Ana HR Operations plugin** | Ana and the internal HR team | Main recurring workflow; never client/candidate data in repo |
| **Ana Operator Kit ZIP** | Ana/internal practitioners | Practitioner-only; not client-sendable |
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
docs/                            # team adoption, Drive, Canva, practice, updates, adaptation guides
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
