# Google Workspace and template architecture

This is the exact starting folder and permission design for Ana's Drive. Create it in an Ana-controlled shared drive or company-owned Drive account. Use a real client alias rather than a full client name in cross-client views.

```text
Ana HR Operations — Private
├── 00 Governance & Team Setup
│   ├── Team roles and permission matrix
│   ├── Private template registry (real links)
│   ├── Approval and change log
│   └── Version and update receipts
├── 01 Master Templates — View Only
│   ├── Google Docs — Kickoff
│   ├── Google Docs — Job Description
│   ├── Google Docs — Offer
│   ├── Google Docs — Invoice
│   ├── Canva — Offer
│   ├── Canva — Invoice
│   └── Canva — Presentation
├── 02 Active Engagements
│   └── ENG-[CLIENT-ALIAS]-[ROLE-ALIAS]
│       ├── 00 Administration and approvals
│       ├── 01 Kickoff
│       ├── 02 Role and recruiting delivery
│       ├── 03 Commercial drafts
│       ├── 04 Client-ready drafts
│       └── 05 Handoff receipts
├── 03 Approved Deliverables
│   └── ENG-[CLIENT-ALIAS]-[ROLE-ALIAS]
├── 04 Research Library
│   ├── Source register
│   ├── Reviewed claims
│   └── Workshop and team-practice research
├── 05 Content Studio — Approval Required
│   ├── Drafts
│   ├── Ana-approved source pack
│   └── Published receipt archive
└── 90 Archive — Restricted
```

## Permission model

| Folder | Ana | Team | Client | Principle |
| --- | --- | --- | --- | --- |
| `00 Governance & Team Setup` | Owner/editor | Comment or view according to role | No access | Central rules, real template links, change receipts |
| `01 Master Templates — View Only` | Owner/editor | View only | No access | Masters are never edited in place |
| `02 Active Engagements` | Editor | Only the engagement team, editor according to task | No access by default | Work happens in a copied artifact and private record |
| `03 Approved Deliverables` | Editor | View or comment | Client gets only a deliberate share of an approved item | Nothing enters here without Ana approval |
| `04 Research Library` | Editor | Research operator edits; others comment/view | No access unless a source is explicitly client-shareable | Sources and applicability, not confidential material |
| `05 Content Studio` | Editor/approver | Draft/edit based on role | No access | Drafts are not publishing authorization |
| `90 Archive` | Owner | View only if required | No access | Retention and access follow Ana/company policy |

Candidate CVs, interview recordings, detailed interview evidence, background checks, medical information, and identity data remain in the approved ATS/HR system, not in this Drive architecture. Bank/payment credentials remain in the approved finance system.

## Template registry: the bridge from process to design

Create the real registry inside `00 Governance & Team Setup`. Start from the public-safe [example registry](../plugins/ana-hr-operations/skills/ana-hr-operations/assets/template-registry.example.json), replace the placeholder references privately, and keep the real registry out of GitHub.

Every row/entry needs:

- `template_id`, document type, and platform (`google-docs` or `canva`);
- real master link or ID (private only), owner, and approved audience;
- copy destination and expected naming format;
- content fields the template accepts;
- whether visual inspection is required and who records it;
- last reviewed date, version, and replacement/superseded status.

## Template lifecycle

1. **Select:** the coordinator identifies the exact approved template from the private registry.
2. **Authorize:** Ana confirms the document type, destination, and permission to copy.
3. **Copy:** Codex or the operator creates a copy; it never edits the master.
4. **Prepare:** use approved engagement facts and a document-specific content pack.
5. **Verify:** Google Docs gets connector readback; Canva gets an in-Canva human visual check.
6. **Approve:** Ana approves content and template fidelity separately where needed.
7. **Handoff:** client sharing/sending remains a fresh `SOP-07` gate.
8. **Archive:** save the approval/handoff receipt with the copied artifact.

## Naming convention

Use names that make stage and review state visible:

```text
[CLIENT-ALIAS] — [ROLE/SERVICE] — [DOCUMENT TYPE] — DRAFT v01
[CLIENT-ALIAS] — [ROLE/SERVICE] — [DOCUMENT TYPE] — ANA APPROVED v02
```

Avoid client names in a broad cross-client board. Use the legal client name only inside the restricted engagement folder where the company policy permits it.

## Tool routing

| Task | Correct tool/connector | Required evidence |
| --- | --- | --- |
| Kickoff, job description, offer, or invoice master in Google Docs | Google Drive / `$google-docs` | Exact master, copy ID/URL, connector readback, draft status |
| Offer, invoice, or presentation master in Canva | Canva connector or human Canva workflow | Exact master, copied design, approved content pack, visual-check card |
| Control workbook and practice tracker | Google Sheets / `$google-sheets` | Private folder location, formula/data-validation review, owner |
| Client email | Gmail only after `SOP-07` | Exact recipient, current artifact revision, fresh Ana authorization |
| Kickoff scheduling | Calendar only after explicit request | Exact attendee/time, fresh Ana authorization |

No tool may search Drive or Canva broadly for an unspecified master. Missing exact source or copy permission is `TEMPLATE_BLOCKED`.
