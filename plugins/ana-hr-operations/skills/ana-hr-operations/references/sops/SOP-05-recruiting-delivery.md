# SOP-05 — Recruiting delivery and weekly client status

## Purpose

Launch and operate a structured search while keeping candidate data in the approved ATS, applying consistent evidence, and preserving human hiring accountability.

## Trigger

Run after job-description approval to launch a requisition, manage delivery, prepare a weekly update, or control a material role change.

## Entry criteria

- Kickoff and job-description validations pass.
- Scorecard, recruitment process, ATS, requisition owner, client decision-maker, and next update date are recorded.
- Ana explicitly approves recruiting launch.

## Procedure

1. Create the requisition in the approved ATS and store only its reference in the engagement record.
2. Confirm the sourcing brief, target evidence, approved channels, location/eligibility constraints, compensation facts, and outreach boundary.
3. Convert the scorecard into one structured screening rubric and interview plan used consistently for the same role.
4. Keep names, emails, CVs, interview notes, references, and decisions in the ATS. Use only aggregate stage counts and ATS references in the engagement record or client status asset.
5. Track aggregate stages: sourced, contacted, responded, screened, client review, interview, reference, offer, placed/closed. Counts must trace to the ATS snapshot time.
6. Prepare the weekly status from `assets/recruiting-weekly-status.md`: progress, evidence/process learning, risks, client decisions needed, changes, and next seven-day plan. Do not expose rejected-candidate details.
7. Present shortlisted candidates only through the approved ATS/client route and against the approved scorecard. AI may organize evidence but must not rank or decide.
8. Record client decisions, owners, dates, and any change request. A material role/scope change returns to `SOP-02`, `SOP-03`, or `SOP-04` as applicable.
9. Validate with `validate_engagement.py --stage recruiting` after launch and at any material process change.

## Exit criteria

- Recruiting validation passes and requisition status is current.
- ATS reference, scorecard reference, structured process, aggregate counts, next client update, and launch approval are recorded.
- Every candidate decision remains attributable to a named human decision-maker in the approved system.

## Evidence

- ATS requisition reference and timestamped aggregate counts.
- Weekly client status draft.
- Change log, validation output, and SOP receipt.

## Exceptions

- `LAUNCH_APPROVAL_PENDING`: Ana has not approved recruiting launch.
- `ATS_BLOCKED`: approved ATS or requisition reference is unavailable.
- `SCORECARD_BLOCKED`: job-relevant evidence or structured rubric is incomplete.
- `PIPELINE_STALE`: counts cannot be tied to a current ATS snapshot.
- `ROLE_CHANGE`: the client materially changes the outcome, criteria, timeline, or scope.
- `BIAS_BLOCKED`: a requested decision relies on protected traits or personality proxies.
- `DATA_INCIDENT`: candidate data appears outside the approved route; stop and follow company incident policy.
