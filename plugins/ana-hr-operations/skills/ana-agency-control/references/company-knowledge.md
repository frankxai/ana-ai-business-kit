# Company knowledge and talent-source contract

## One authority for each record

| Domain | Authoritative home | Shared knowledge may contain |
| --- | --- | --- |
| Company method, policies, approved reusable answers | Company-owned knowledge workspace; controlled Drive or existing vault | Reviewed content, version, owner, source, permitted use |
| Clients, buying needs, service opportunities | Existing CRM | Account alias, engagement alias, stage, owner, next action |
| Candidates and prospects for employment | Existing ATS; restricted current list only during an authorized migration | Requisition alias, aggregate counts, source-system reference |
| Role requirements and hiring evidence | Client-approved ATS/requisition record | Approved job criteria reference and unresolved process questions |
| Commercial service catalog | Owner-approved catalog with versioned terms | Approved service scope, exclusions, delivery units, pricing source reference |
| Meetings and decisions | Existing calendar plus reviewed decision/task records | Work decisions, commitments, owners, deadlines, source references |
| Invoicing and payments | Existing finance system | Draft/reconciliation receipt and provider reference |
| Personal reflection or clinical work | Separate restricted practice systems | No content or retrieval route in employer knowledge |

The existing Ana Business Vault is a reusable knowledge layer. It is not a candidate, CRM, signed-contract, or accounting database. Preserve that separation when adapting the public kit for another agency.

## Source registry

Register each permitted source before ingesting content: stable source ID; owning agency; domain; actual source-system reference kept privately; record owner; version; update date; review deadline; access classification; permitted audience/purpose; retention owner; superseding source; and deletion/revocation behavior.

The local planner accepts a smaller metadata projection: IDs, agency/engagement scope, kind, version, owner role, dates, and declared access. Its schema is not the full hosted security model. References in public fixtures are fictional tokens. They cannot be resolved without a private connector mapping.

Lifecycle: discovered → owner verified → permission scoped → indexed or linked → reviewed → superseded/revoked. Discovery alone is not permission to index. A stored transcript is not a reviewed company policy. A generated summary is not an approved decision.

Begin with document links and ordinary structured fields. Add full-text retrieval when a source is authorized and current. Add vector search only when measured retrieval failures justify it; embedding every file first increases duplicate facts and deletion work. Search must apply agency/resource permissions before retrieval and again before presenting a cited result.

An answer must expose its source and version, identify missing or conflicting facts, and distinguish policy from proposal. On price, employment terms, commitments, or client-specific rules, conflicting sources block a definitive answer until the accountable human selects the authority. Never blend two incompatible commercial offers into a new policy.

## Existing candidate lists

Treat spreadsheets, CRM exports, email references, and personal professional networks as distinct sources. Preserve origin, collection context, current owner, permission to use/contact, retention, and last verification. A person's appearance on a list does not imply availability, interest, consent, or suitability.

Use a source manifest first. Count rows and missing fields inside the authorized source; do not copy identifiable rows into Git or a broad company board. Where no ATS exists, an explicitly authorized restricted list can remain the temporary source while the agency selects a system. This is not permission to duplicate it across chat history, a vault, and several automation tools.

For an authorized migration, the operator maps source columns to the selected ATS, previews changes, reviews ambiguous duplicates, imports a small reversible batch, reads records back, and reconciles source/target counts. Use provider IDs for updates. Two people with the same name must not be merged automatically. Two identical exports must not create duplicate contacts. Keep the original until acceptance and retention policy permit disposal.

Safe agent jobs: prepare missing-field queues, reconcile authorized factual fields, surface explicit job-related evidence with source dates, flag stale availability, draft interview logistics, and prepare follow-up for human review. Final selection and outreach remain human governed. Do not infer personality, protected traits, emotion, health, spirituality, or unexpressed interest; do not scrape around a platform's access controls.

The company brief reports “three requisitions lack an owner” or “five follow-ups await review.” Candidate-level detail is retrieved only inside the restricted recruiting task for an authorized user. Aggregation is not automatic anonymization; avoid small-group disclosures across clients.

## Knowledge maintenance

The curator batches repeated questions into candidate FAQ entries with cited answers and an owner. Ana reviews reusable method changes; client-specific facts stay with their client owner. Give operational guidance an explicit review date. Revocation removes derived search material and queued context, not just the source link. Maintain provider tombstones and short-lived caches before introducing persistent retrieval.

Run three kinds of evaluation: questions with a known current answer; questions requiring abstention because a source is missing or stale; and cross-client questions that must disclose nothing. Source-citation accuracy and denied-access tests matter more than the number of documents indexed.
