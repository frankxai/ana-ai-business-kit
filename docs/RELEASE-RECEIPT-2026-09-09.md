# Development candidate receipt — 9 September 2026

Primary studio: software-studio. Canonical source: ana-ai-business-kit. Base: 5ee80906a8079a797eb7c737401f5c9a74f4185e. Plugin candidate: 0.3.0-rc.3. Legacy download package version: 1.1.0.

## Delivered

- Invoice validator/renderer correctness fixes with malformed-input, decimal, fractional quantity, rounding, and payment-term regressions.
- Local SQLite billing preparation ledger with immutable event/source records, exact full-event reconciliation, duplicate reservation prevention, revision-bound manual acknowledgment, recoverable exports, and 21 behavioral tests.
- Team-practice skill, validated JSON brief, internal draft renderer, 10 behavioral tests, fictional handoff exercise, checklist, and follow-through roles.
- Audit with primary-source research, engineering PRD, and defined success metrics with all business baselines unmeasured.
- Pilot operator runbook, fictional billing source/event, failure exercises, and a blank measurement CSV with denominators and missing-data rules.
- Sixth skill, ana-agency-control: company source/engagement scope checks, dependency planning, bounded specialist handoffs, distinct preparation/approval roles, draft decision questions, and protected live-meeting rules; 31 behavioral tests.
- Current native connector/MCP research, agency-control PRD, knowledge/team/async contracts, and a blank coordination measurement CSV.
- Portable Python packaging and a read-only GitHub Actions test/package workflow using pinned action revisions.

## Local verification

- The pre-change npm test baseline passed.
- The updated npm test passes all existing checks plus 10 team-practice tests, 21 local billing tests and 31 agency-control tests, including concurrent retries, source/amount mismatch, stale/reverted revisions, forged JSON approver declarations, edited artifacts, malformed CLI input, and export recovery.
- Skill structure validation passes for ana-team-practice.
- Independent forward-use produced a draft successfully. Review found missing exercise assets and checkpoint ownership; the candidate now supplies them. Validation-only mode now explicitly reports that no file was written.
- The previous package command failed because PowerShell was absent. The new Python packaging command succeeds; both archives were checked against manifest entry lists, source bytes, and SHA-256 checksum files.
- Independent command-line forward-use completed for two fictional agency identities using separate ledgers and records without modifying shared code. Both exercised init, event registration, preparation, export, consistency check, manual acknowledgment, retry, changed terms, and stale-receipt rejection. This is technical portability evidence; actual installed operator adoption is unmeasured.
- Independent code review corrected an initial conflation of accounting destination and payment-instructions profile; both now bind separately to the receipt.
- New database and export files use owner-only permissions on the tested POSIX runtime. These defaults do not supply encryption or protect against an authorized file editor.
- Independent agency-control forward-use completed a fictional work/decision/meeting brief. It found missing packet deadline/dependency fields and worker-return contract drift; these were corrected. Decision questions now explicitly require preparation, and pre-read readiness is declared rather than artifact-verified.
- Agency-control tests cover same-agency wrong-engagement sources, cross-agency/forbidden/stale/revoked sources, missing task source domains, dependency cycles/blockers, separate service/employment decisions, malformed CLI input, protected meetings, and modeled-versus-actual time.
- Changed source passes git diff --check.

GitHub CI is a separate result from local verification. Consult the PR's exact head checks before merge. No fresh Codex installation or cross-host installation was performed.

## Limits and release state

This is a reviewable source candidate, not a commercial or live accounting release. No prices, external sends, invoices, customer records, checkout products, or production websites were changed. Ana's method/identity and commercial approvals are not recorded by this work.

Input validators enforce documented structure and declared boundaries, not the authenticity of human approvals or absence of personal information in free text. The invoice helper has a bounded two-decimal currency set and one supplied tax rate. The team session is an unvalidated facilitation scaffold, with no clinical or neuroscience outcome claim.

The ledger implements source digest matching, local full-event reservations, and exact-revision manual acknowledgments. Connected accounting, authenticated source acceptance/approvals, cumulative contract budgets, cross-ledger/provider duplicate prevention, tenant isolation, and payment reconciliation remain proposed work. The ledger does not monitor external file changes or provide a tamper-resistant audit service. Rollback is a reviewed source revert and restoration of the previously validated plugin version. Existing editorial-contract PR #8 is separate.

Runtime/API spend for the delivered local helpers: no external calls. Model/tool session costs were not exposed, so no total cost is asserted.

## Company knowledge and connected team limits

The agency helper validates supplied metadata and emits proposed work packets. It does not import candidate lists, search live sources, authenticate actors, launch workers, verify pre-read artifacts, create tasks, or cancel meetings. The actual company ATS/CRM/workspace/calendar and live data were not inspected. The existing private vault contains reusable guidance and client placeholders, not the company candidate corpus.

Private Ana PR #10 adds a navigable company knowledge map, twelve source-linked starter answers, candidate-list intake manifest, service-catalog structure, decision protocol, activation slots, and connected-team architecture. These are reviewed source drafts, not accepted company policy or a configured live service. Meeting reduction and all business outcomes remain unmeasured.
