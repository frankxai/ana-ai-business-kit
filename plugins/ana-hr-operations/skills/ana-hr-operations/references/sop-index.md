# Ana HR SOP help system

Choose one SOP before acting. If a request spans stages, complete and receipt each SOP separately. Never skip an approval gate because a later artifact is urgent.

## Routing table

| User intent | SOP | Required reference | Stop condition |
| --- | --- | --- | --- |
| “What needs attention today?”, all clients, priorities, overdue work | `SOP-00` | `sops/SOP-00-multi-client-control.md` | Private source records unavailable or board would expose personal data |
| New client, discovery, first call, capture everything | `SOP-01` | `sops/SOP-01-first-client-call.md` | Client identity/need unavailable or sensitive candidate data appears |
| Kickoff, onboarding, confirm scope and process | `SOP-02` | `sops/SOP-02-client-kickoff.md` | First-call validation fails or decision-makers are unresolved |
| Scorecard, job description, role profile | `SOP-03` | `sops/SOP-03-job-description.md` | Kickoff is not approved or role evidence is incomplete |
| Proposal, offer, fee, price, commercial terms | `SOP-04` | `sops/SOP-04-offer-and-pricing.md` | Pricing source, currency, tax treatment, or approver is missing |
| Launch search, sourcing, screening, pipeline, weekly update | `SOP-05` | `sops/SOP-05-recruiting-delivery.md` | Job description or recruiting launch is not approved |
| Invoice, billing, milestone charge | `SOP-06` | `sops/SOP-06-invoice.md` | Approved offer/milestone, billing identity, or invoice numbering is missing |
| Final document, email draft, handoff, send | `SOP-07` | `sops/SOP-07-send-and-handoff.md` | Exact recipient, channel, latest artifact, or active-turn approval is missing |

## Branching sequence

```text
SOP-00 multi-client control (daily, across all stages)
                    |
SOP-01 first call -> SOP-02 kickoff
                         |             \
                         v              v
                  SOP-03 job       SOP-04 offer
                  description      and pricing
                         |              |
                         v              v
                  SOP-05 recruiting SOP-06 invoice
                         \              /
                          v            v
                         SOP-07 approved handoff
```

Job description and offer may proceed in parallel only after kickoff approval. Recruiting launch depends on job-description approval. Invoice depends on an approved offer or milestone. Every external handoff depends on the artifact approval plus a fresh send approval.

## Standard SOP receipt

Every SOP result must end with:

- `sop_id` and execution timestamp;
- engagement ID and client alias;
- source records read, with last-reviewed timestamps or revisions;
- entry criteria result;
- actions completed;
- validation command and result;
- approvals present and missing;
- artifacts created or changed, with draft/final status;
- exception code and blocked assumptions, if any;
- next action, owner, and due date;
- external action still requiring Ana.

Do not claim completion without this receipt. A draft, validation pass, approval, and external send are separate facts.
