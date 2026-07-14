# Research library standard

## Entry contract

Every private entry follows `ana-research-entry/v1` and includes:

- question, topic, intended audience, and proposed safe use;
- source title, publisher/author, URL or approved private reference, source class, and publication/access date;
- `source_supported_claim` written narrowly;
- separate `team_interpretation`, limitations, applicability, and prohibited uses;
- evidence strength label and whether qualified review is needed;
- curator, named reviewer, review status/date, and next-review date;
- confirmation that no personal/candidate/employee data is included.

Use an absolute `https://` URL for a public source. When the source location must remain in the approved private registry, use only a non-sensitive reference ID in the form `PRIVATE-SOURCE-NAME-001`; never put a private URL, access token, person name, or client identifier in that value.

## Claim writing rules

- Say what the source supports, not what the team hopes it means.
- Use calibrated language: "may support", "is guidance for", "was observed in [context]", or "requires local validation" when appropriate.
- State population, context, method, or implementation limits that could change applicability.
- Do not turn an association into causation, a workshop into therapy, a framework into law, or a vendor claim into evidence.
- Link every external claim to at least one entry ID; a claim without a reviewed source remains a draft question.

## Sensitive/regulated boundary

For recruiting and employment work, research may improve process design, structured evidence, access, and communication. It must not be used to:

- determine candidate suitability from protected traits, personality, emotion, health, neurotype, or inferred psychology;
- automate or materially determine an employment decision;
- diagnose, assess wellbeing, or represent clinical/neuroscience expertise;
- provide legal, tax, immigration, employment-law, or regulatory advice.

If a source concerns employment AI, data protection, legal constraints, or high-risk systems, record it as a research flag and route implementation decisions to Ana and qualified counsel/appropriate expert.

## Review statuses

| Status | Meaning |
| --- | --- |
| `CAPTURED` | Source recorded; no practice use approved |
| `CURATOR_REVIEWED` | Entry is complete enough for Ana review |
| `ANA_APPROVED_FOR_INTERNAL_REFERENCE` | Ana approved the stated limited internal reference use |
| `EXPIRED_OR_SUPERSEDED` | Do not rely on it until re-reviewed |

No status approves publishing, client advice, or an employment decision.
