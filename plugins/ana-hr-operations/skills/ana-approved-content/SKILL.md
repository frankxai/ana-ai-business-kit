---
name: ana-approved-content
description: Draft accurate, approval-gated content for Ana's HR and team-practice work using reviewed sources. Use for educational posts, newsletters, website copy, workshop invitations, content briefs, or repurposing approved material. Never use this skill to publish, send, invent claims, or turn client stories into marketing without explicit approval.
---

# Ana Approved Content

Create content that protects trust. This skill combines brand-guardian and blog-publisher patterns while deliberately stopping before publication: it turns approved source material into a clear, ethical draft and leaves the final approval, channel choice, and publication action to Ana.

## Load the right references

- Always read `references/editorial-safety.md`.
- Read `assets/content-brief.example.json` and use `scripts/validate_content_brief.py` for a private content brief or approval record.
- When a factual/research claim is involved, load `$ana-research-library` first and cite the reviewed library-entry IDs in the brief.

## Core workflow

1. Confirm audience, format, intent, channel under consideration, and the one honest next step. A channel is a plan—not authorization to publish.
2. Collect only approved sources: Ana-provided facts, approved library entries, or an explicitly approved client source. If the source is missing, make it a question or stop.
3. Build a content brief with source IDs, factual boundaries, prohibited claims, draft status, and required Ana approval.
4. Draft with a precise hook, useful explanation, calibrated claim, transparent limits when relevant, and one clear next step.
5. Check: no client identity/story without explicit permission; no fabricated proof, guarantee, urgency, testimonial, clinical/neuroscience claim, or legal/HR compliance claim.
6. Validate the private brief:

```bash
python scripts/validate_content_brief.py <private-content-brief.json>
```

7. Return `DRAFT_REVIEW_REQUIRED`, the sources used, missing approvals, and the exact action Ana must take next.

## Approval model

| Status | Meaning |
| --- | --- |
| `DRAFT_REVIEW_REQUIRED` | Draft exists; no external action is allowed |
| `ANA_CONTENT_APPROVED` | Ana approved wording for the stated audience; it is still not published/sent |
| `PUBLISHED_EXTERNALLY_RECEIPTED` | A named human reports they published it; this skill did not publish it |

`ANA_CONTENT_APPROVED` does not approve a new audience, channel, schedule, client story, paid promotion, or external send. Each needs a fresh human decision.

## Ethical persuasion standard

- Name the real audience problem and the specific service/process value.
- Explain scope and limits; do not imply a guaranteed hire, transformation, or outcome.
- Use urgency only when it is factual and sourced; never manufacture scarcity.
- Do not hide who is speaking, use fake testimonials, or present an experiment as proof.
- Invite a conversation, assessment, or resource with a truthful next step.

## Team and neuroscience boundary

Content about team collaboration may discuss voluntary working agreements, facilitation, learning, decision rights, or reflection. It must not diagnose teams, claim brain-based expertise without a reviewed source and qualified context, suggest that neuro/personality traits determine fit, or turn health/psychology into marketing copy.

## Completion gate

Return:

- draft status and intended audience;
- source entry IDs and what each source supports;
- claims kept, softened, or blocked;
- content brief validation result;
- required Ana approval and any channel/publish action still outside this skill.
