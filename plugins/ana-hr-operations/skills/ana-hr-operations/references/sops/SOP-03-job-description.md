# SOP-03 — Role scorecard and job description

## Purpose

Create an inclusive, evidence-based role scorecard and job description in Ana's approved structure without inventing requirements or using personality proxies.

## Trigger

Run when recruiting scope is approved and a new or materially changed role needs definition.

## Entry criteria

- Kickoff approval exists and `kickoff` validation passes.
- Role owner and job-description approver are named.
- Business outcome, reporting line, location, employment type, timeline, and selection process are known or visibly blocked.

## Procedure

1. Separate the role mission, 30/60/90-day outcomes, responsibilities, must-haves, trainable capabilities, and optional advantages.
2. Translate vague traits such as “culture fit,” “dynamic,” or “senior presence” into observable job-relevant evidence or remove them.
3. Challenge every must-have: retain it only when the role owner can explain why it is necessary and how it will be assessed consistently.
4. Create the scorecard and structured interview evidence before polishing the public job-description copy.
5. Draft title, mission, outcomes, responsibilities, requirements, location/work pattern, employment type, compensation text from approved facts, and recruitment stages.
6. Check for protected-trait inference, unnecessary credential inflation, unexplained gaps, fabricated market claims, and inconsistent criteria.
7. Create a content pack from approved role facts. For Google Docs, execute the copy/readback route in `google-docs-template.md`; for Canva, use a copied master and named visual check; otherwise create a visibly labeled local draft.
8. Compare the draft with the kickoff and scorecard. Resolve or list every contradiction.
9. Record Ana's job-description approval and timestamp; run `validate_engagement.py --stage job-description`.

## Exit criteria

- Job-description validation passes.
- Scorecard reference and final draft reference are recorded.
- Requirements are job-relevant and the same evidence can be applied consistently across candidates.
- Publication/send remains a separate `SOP-07` action.

## Evidence

- Scorecard reference.
- Draft job description and template readback status.
- Quality review, approval, validation output, and SOP receipt.

## Exceptions

- `ROLE_FACTS_BLOCKED`: mission, reporting line, location, or employment facts are missing.
- `CRITERIA_BLOCKED`: must-haves cannot be tied to observable evidence.
- `BIAS_BLOCKED`: protected-trait or personality-proxy language remains.
- `TEMPLATE_BLOCKED`: approved template route is incomplete.
- `JD_APPROVAL_PENDING`: Ana has not approved the job description.
