# Excellence scorecard

All baseline and current values are **unmeasured** at 9 September 2026. Targets below are proposed release criteria, not advertised outcomes. Start with ten comparable completed drafts and at least three engagements. Retain denominators and task complexity; do not present a tiny pilot as causal proof.

North-star measure: completed, human-approved engagement milestones per delivery hour, with quality, privacy, and client satisfaction as guardrails. Track billable value separately; generated document count is not customer value.

| Metric | Definition and source | Proposed threshold | Owner |
| --- | --- | --- | --- |
| Draft preparation time | Median active preparation minutes per comparable invoice; private timer/receipt | At least 50% below baseline | Operations lead |
| Financial correctness | Reconciled drafts / reviewed drafts; finance checklist | 100% on pilot; any material error pauses connected billing | Finance owner |
| First-pass acceptance | Drafts needing no material revision / reviewed drafts | At least 90% after 20 drafts | Practice lead |
| Approval coverage | Consequential actions with current valid receipt / such actions | 100%; initially manual, later authenticated | Ana/delegate |
| On-time handoff | Accepted handoffs by due date / due handoffs | At least 95% over 30 days | Coordinator |
| Template fidelity | Outputs passing content readback + visual review / reviewed outputs | 100% before client delivery | Document lead |
| Agency activation | Agencies finishing a fictional end-to-end rehearsal / onboarded agencies | At least 80% within 7 days | Enablement lead |
| Owner burden | Ana/Frank support minutes per active agency each week | At most 30 after onboarding; exceptions tracked | Product owner |
| Team follow-through | Agreed process actions completed / actions due by day 30 | At least 80%; no individual psychometric score | Facilitator |
| Paid validation | Agencies purchasing and completing scoped pilot | Two before broader launch; three for shared MCP demand gate | Commercial owner |
| Digital contribution margin | (Ex-tax revenue − refunds − fees − hosting/inference − allocated variable delivery/support) / ex-tax revenue | At least 70% over first 30 orders | Commercial owner |
| Partner independence | Sessions delivered to standard without Ana present / licensed sessions | At least 80% after initial facilitator enablement | Method lead |
| Boundary incidents | Unauthorized send, cross-client access, individual profiling, exposed private content | Zero; any confirmed event pauses affected capability | Technical + practice owners |

Do not mix self-serve digital margins with labor-intensive installation margins. Report both founder time and contractor cost. No aggregate emotion score, diagnosis, brain type, or belief score belongs on this dashboard.

## Minimal event receipt — proposed hosted contract

Record `event_id`, `tenant_alias`, `engagement_alias`, `workflow`, `stage`, `artifact_revision`, `status`, `started_at`, `finished_at`, `active_minutes`, `review_minutes`, `material_corrections`, `cost_currency`, `variable_cost`, `policy_version`, `approval_receipt_ref`, and `failure_category`. Keep actual identities and sensitive source material in their approved systems. Unknown values remain null; failed attempts remain in the denominator.

Use `not_measured`, `insufficient_sample`, `pass`, `fail`, or `paused` explicitly. A software test pass does not satisfy a business metric. Process adoption is observable evidence; it does not demonstrate clinical benefit or a causal neuroscience effect.

## Cadence

The coordinator maintains the daily exception queue. Ana or her delegate reviews material decisions in one weekly batch. Monthly, the product owner reviews adoption, margin, support burden, and which unproven feature to stop. Customer follow-up and metrics collection require agreed purpose, access, and retention.
