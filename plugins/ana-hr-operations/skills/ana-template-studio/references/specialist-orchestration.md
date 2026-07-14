# Specialist orchestration

## One coordinator, four specialist lanes

`$ana-hr-operations` remains the coordinator and synthesis owner. The “swarm” is a governed set of specialist passes, not independent authority.

| Lane | Skill/route | Input | Output | May not do |
| --- | --- | --- | --- | --- |
| Engagement control | `$ana-hr-operations` | Private record and selected SOP | Validated stage receipt | Infer approval or skip stage gates |
| Research and scorecard | `$ana-hr-operations` + `$ana-research-library` | Approved question/role facts | Evidence entry, scorecard, limitations | Decide or profile candidates/employees |
| Template Studio | `$ana-template-studio` | Validated stage receipt + content pack | Checked Docs/Canva artifact state | Change source facts, approve, share, send |
| Quality and approval | `$ana-hr-operations` | Artifact, validation, sources | Ana decision card and next action | Treat review as approval |

`$ana-approved-content` is an optional downstream lane for source-backed education/marketing only. It never publishes.

## Safe concurrency

- Before kickoff approval: sequential only.
- After kickoff approval: job-description/scorecard and service-offer content may run in parallel because both read the same immutable kickoff receipt.
- Before recruiting: job-description approval and recruiting-launch approval must be present.
- Before invoice: approved offer/milestone and all finance sources must be present; run sequentially.
- Candidate selection, Canva visual review, Ana approvals, and any external handoff are always sequential human gates.

## Fallback for a teammate

When orchestration is confusing or a connector fails:

1. Select one SOP in `$ana-hr-operations`.
2. Complete one copied Google Doc content pack.
3. Validate the stage.
4. Ask Ana one exact decision.
5. Resume the next step only after that decision.

No teammate needs GitHub knowledge for daily delivery. Codex loads the maintained plugin; Drive/ATS/Canva hold the private work.
