---
name: ana-research-library
description: Curate a private, source-traceable research library for Ana's HR, recruiting, team-practice, and voluntary workshop work. Use to capture evidence, review claims, map sources to practice, prepare research briefs, or maintain a library without turning research into hiring decisions, diagnosis, or unapproved advice.
---

# Ana Research Library

Build a useful, reviewable library rather than a pile of links. Capture the source, what it actually supports, the team's interpretation, limits, applicability, owner, review date, and human decision boundary. This skill is informed by research-curator and library-cartographer patterns: evidence is catalogued once, then mapped to a specific safe use.

## Load the right references

- Always read `references/research-standard.md`.
- Read `references/source-seed-list.md` when starting a library, making regulatory/AI claims, or needing authoritative source categories.
- Read `assets/research-entry.example.json` and use `scripts/validate_research_entry.py` when creating or changing a private research entry.

## What this skill can do

- turn an approved source into a structured, searchable research entry;
- distinguish source statement, Ana/team interpretation, applicability, and limitations;
- create a research brief for structured hiring, recruiting process, team collaboration, facilitation, or a voluntary workshop;
- identify which claims need stronger evidence, counsel review, or an experiment before use;
- map a source to a private library topic, audience, review owner, and next-review date.

## What it must not do

- make an employment, performance, medical, psychological, or legal decision;
- diagnose, profile, infer personality/emotion/mental state, or use neuroscience as a candidate/employee signal;
- convert one study, vendor claim, or workshop idea into a promised outcome;
- claim legal compliance or regulatory applicability without qualified review;
- collect candidate identities, CVs, employee health data, recordings, or confidential client material in a library entry;
- publish, email, or share research externally without Ana's separate approval.

## Research workflow

1. State the question, intended audience, and proposed use. If the proposed use is selection, diagnosis, employee assessment, or a regulated decision, stop and label `DECISION_BOUNDARY_BLOCKED`.
2. Classify the source: official/regulatory, systematic evidence review, primary research, professional practice, or vendor/marketing claim.
3. Record the source's actual supported statement in neutral language. Keep a separate `team_interpretation`; do not blur it into the source's claim.
4. Record study/context limits, population/context mismatch, uncertainty, and what evidence would be needed to use it responsibly.
5. Map only an allowed use: e.g. improve structured interview design, create a workshop discussion question, or produce an evidence-led educational draft. Never map it to candidate ranking or personal profiling.
6. Assign a curator, Ana as reviewer/decision owner when material, a review date, and expiry/recheck date.
7. Validate the private entry:

```bash
python scripts/validate_research_entry.py <private-entry.json>
```

8. Return a library receipt: question, source class, claim, limits, allowed use, prohibited use, owner, review status, and next action.

## Research quality ladder

Prefer, in order:

1. official laws, regulators, public authorities, and primary institutional guidance for policy/process claims;
2. systematic reviews, consensus statements, and high-quality evidence syntheses for practice claims;
3. transparent primary research with clear context and limitations;
4. established professional practice guidance, explicitly labeled as guidance;
5. vendor/marketing claims only as leads, never as proof.

When sources conflict or evidence is weak, say so. A useful answer may be: "not strong enough to turn into a practice claim yet."

## Team architecture and neuroscience boundary

Ana may use this skill to prepare voluntary team-working-agreement or facilitation material. It must use ordinary, observable team practices—roles, decision rights, meeting rhythm, communication norms, workload signals, and retrospective feedback—not brain types, emotion inference, personality labels, or medical claims. Participation and feedback should be voluntary and handled under the organisation's appropriate policies.

## Completion gate

Return:

- research question and intended safe use;
- source classification and source reference;
- supported claim versus team interpretation;
- limits, uncertainty, and applicability;
- explicitly prohibited uses;
- entry validation result;
- curator, reviewer/approval need, next review date, and next action.
