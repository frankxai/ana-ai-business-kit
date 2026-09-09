# Team practice and reusable agency products

This extension connects a reviewed HR method to voluntary team practice, AI workflow adoption, and a reusable agency product. It adds two skills to the existing plugin. It does not add a second invoice engine, a clinical product, a community platform, or an automatic publication path.

## Route and responsibilities

| Stage | Existing or new route | Output and accountable decision |
| --- | --- | --- |
| Client need and scope | `ana-hr-operations` SOP-01/02 | Practitioner and client confirm one observable workflow and data boundary |
| Research | `ana-research-library` | Source statement, interpretation, limitations and reviewed reference |
| Voluntary practice | `team-practice-design` | Internal run sheet, participation choices, aggregate measurement and quality baseline |
| Repeatable delivery | `agency-productization` | Product brief, evidence receipts, adaptation/rights review, support and update limits |
| Offer and invoice | Existing SOP-04 and SOP-06 | Approved commercial facts and reconciled draft; no new billing engine |
| Client documents | `ana-template-studio` | Approved upstream stage receipt, exact-master copy and readback/visual check |
| Educational distribution | `ana-approved-content` | Separately approved sources and de-identified claims; no publish/send action |

A facilitator may apply the same method to a team working session, founder gathering, or host programme. Community/venue systems receive only the programme reference and approved logistics needs. Participant records, private reflections, billing records, employment decisions and property contracts never become one shared dataset.

## Initial product sequence

1. **Team practice kit:** one voluntary AI drafting or handoff practice, synthetic exercises, a quality rubric and facilitator run sheet. Measure baseline and pilot on the same task.
2. **Agency delivery kit:** repeat the approved practice with reviewed delivery evidence, local templates, a clear operator/client audience, versioned adaptation notes and bounded support.
3. **Maintained service:** offer onboarding, a capped adaptation service or updates only when the operator can state the maintained work, response boundary, update window and renewal responsibility.

This sequence is a product hypothesis, not a claim about Ana's existing services, credentials, clients, prices, or consent to co-launch. A collaboration proposal must give each collaborator explicit method/IP ownership, role, delivery limits, commercial review and name-use choices in a private agreement. The public base remains available under its existing license.

The human contribution may include facilitation, working agreements, attention to relationships, reflective discussion and team learning. Personal spiritual reflection is optional, participant-owned and separate from employer reporting. Clinical services require their own practitioner and scope and are outside these skills.

## Evidence standard

- [The COM-B original paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC3096582/) supplies a framework for thinking about capability, opportunity and motivation. It does not establish the efficacy of this kit or an AI adoption programme.
- [Edmondson's original team-learning study](https://www.hbs.edu/faculty/Pages/item.aspx?num=2959) offers research context for team learning and psychological safety. Do not infer guaranteed effects, individual psychological traits, or clinical claims from it.
- The [European Commission AI framework overview](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) identifies workplace emotion recognition among prohibited practices. These skills exclude employee emotion/personality inference and employment assessments by design; this is not a claim of general regulatory compliance.

Source URLs reviewed for this product proposal on 2026-09-09. Before using a claim in a client artifact, create/review its private `ana-research-library` entry. The synthetic fixtures use a labelled practice hypothesis rather than a fabricated approved research receipt.

## Success criteria

Targets below are proposed pilot criteria. They are not measured results, customer guarantees or prices. The owner must confirm them against the actual workflow before delivery.

| Measure | Definition and denominator | Proposed gate |
| --- | --- | --- |
| Operator activation | Operators completing one approved workflow / all eligible operators in the declared pilot window | At least 80%; publish both counts |
| First-pass quality | Completed cases passing the unchanged rubric / all completed cases | Preserve or improve the pre-product baseline |
| Time efficiency | Total preparation + delivery + rework + support hours / completed engagement | Target 20% improvement after two repeats while quality holds |
| Cost containment | Actual model/tool spend and operator hours against separately stated owner ceilings | Every engagement within its approved cap or explicitly rescoped |
| Repeatability | Distinct reviewed delivery receipts for the same workflow | At least two before calling the workflow repeat-delivered; this alone does not validate demand |
| Paid demand | Paid, accepted purchases / qualified proposals in a stated period | Set a pilot target before outreach; do not infer demand from downloads |
| Employer reporting | Consenting participants represented / minimum reporting group size | Suppress below five or a stricter owner floor; never include reflection or individual assessment |
| Support sustainability | Actual support hours / active licensed or supported organisations per support window | Within the stated support obligation; no unlimited access promise |

Contribution measurement belongs in the approved finance process: confirmed revenue less delivery, support, model/tools, travel/venue, payment fees, refund/chargeback and allocated upkeep costs. Public fixture ceilings are fictional rehearsal values. No real pricing is introduced by these skills.

## Rehearsal and validation

Run from the repository root:

```bash
npm test
python plugins/ana-hr-operations/skills/team-practice-design/scripts/validate_practice.py plugins/ana-hr-operations/skills/team-practice-design/assets/practice.example.json
python plugins/ana-hr-operations/skills/agency-productization/scripts/validate_product.py plugins/ana-hr-operations/skills/agency-productization/assets/product.example.json
```

The validators reject unknown structured fields, unsafe reporting settings, missing owners, invalid denominators, lowered quality floors, unbounded cost/support fields, exclusive-public-base rights and implied identity rights. They do not interpret arbitrary prose, authenticate consent or receipt provenance, prove anonymisation, calculate legal tax treatment, or authorize an external action.

Private reflection is never accepted as input to these records. A reporting consent count is a workflow control, not a determination that workplace consent is legally sufficient. Use approved data-processing arrangements and accountable review before live use.

The two existing ZIP audience manifests are unchanged. Review [agency adaptation](HR-AGENCY-ADAPTATION.md), [template routing](TEMPLATE-AND-CANVA-ROUTING.md) and [release/update](RELEASE-AND-UPDATE.md) for their respective operations. A Git branch containing the new skill source is not an installed plugin or a published release.
