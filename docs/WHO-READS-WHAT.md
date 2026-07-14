# Operating map: what each person reads and owns

## Recommended operating model

Use a **Drive-first, GitHub-maintained** model:

- Ana and her team use Google Drive, the approved ATS, Canva, and Codex for ordinary work.
- The installed plugin guides the SOP, validations, stop states, and receipts.
- GitHub holds public-safe instructions, schemas, tests, and fictional examples. Team members may read it in a browser; they do not need a local clone.
- Ana or the approved technical maintainer reviews repository updates and mirrors the relevant operating summary into Drive.
- A separate private company overlay holds real template references and internal policy. It is not a public fork and never holds live candidate records.

This separation respects how expert operators already work: client delivery stays in familiar, controlled business systems, while versioned quality controls remain reviewable and auditable. GitHub maintenance is a specific technical responsibility, not a requirement for every operator.

## Reading path by role

| Person | Read first | Use weekly | Maintains |
| --- | --- | --- | --- |
| Ana | `START-HERE-ANA.md` and the private Drive operating manual | Manager board, approval queue, exception review | Approval decisions, access, templates, live-pilot decision |
| Engagement coordinator | `START-HERE-TEAM.md`, `TEAM-ADOPTION.md`, `TEAM-STARTER-PROMPTS.md` | SOP-00/01/02, Drive engagement folders, control workbook | Owners, due dates, kickoff facts, template route |
| Research/recruiting operator | Team start + research skill instructions | SOP-03/05, ATS, research library | Scorecard/process, aggregate pipeline, evidence entries |
| Document/client-experience operator | Team start + template/Canva routing | SOP-04/06/07, copied Docs/Canva artifacts, content review | Content pack, readback/visual-check receipt, draft handoff |
| Frank / technical maintainer | README, release/update guide, plugin resources/tests | Version check and fictional practice test | Public kit, draft PR, validation evidence; no client data |

## Canonical source by subject

| Subject | Canonical source | Drive mirror/use |
| --- | --- | --- |
| SOP sequence and exception codes | Plugin `references/sop-index.md` + `references/sops/` | Operating manual summary; Codex selects exact plugin SOP |
| Operating roles and permissions | `docs/TEAM-ADOPTION.md` | Governance folder copy, adapted privately |
| Folder/template permissions | `docs/GOOGLE-WORKSPACE-AND-TEMPLATES.md` | Actual controlled Drive folders and permissions |
| Starter prompts | `docs/TEAM-STARTER-PROMPTS.md` | Team onboarding Doc or bookmarks |
| Practice acceptance | `docs/PRACTICE-ENGAGEMENT.md` | Fictional practice folder/workbook |
| Real template IDs/links | Private template registry only | Governance folder; never public GitHub |
| Update status | `docs/RELEASE-AND-UPDATE.md` + reviewed Git history | Version/update receipt in Governance folder |

## SOP synchronization rule

The full procedure is canonical in the installed plugin. The Drive manual may summarize it for readability, but it must not silently redefine entry criteria, approvals, or exceptions. When a plugin SOP changes:

1. update and validate the GitHub/plugin source;
2. run the fictional practice engagement;
3. update the Drive operating-manual summary and version receipt;
4. have Ana approve the live pilot;
5. roll out to the team in a new Codex task.

If the Drive summary and plugin disagree, stop and use the last Ana-approved version until the mismatch is reviewed.
