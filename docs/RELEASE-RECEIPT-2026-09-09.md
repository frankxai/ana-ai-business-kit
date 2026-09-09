# Development candidate receipt — 9 September 2026

Primary studio: software-studio. Canonical source: ana-ai-business-kit. Base: 5ee80906a8079a797eb7c737401f5c9a74f4185e. Plugin candidate: 0.3.0-rc.1. Legacy download package version: 1.1.0.

## Delivered

- Invoice validator/renderer correctness fixes with malformed-input, decimal, fractional quantity, rounding, and payment-term regressions.
- Team-practice skill, validated JSON brief, internal draft renderer, 10 behavioral tests, fictional handoff exercise, checklist, and follow-through roles.
- Audit with primary-source research, engineering PRD, and defined success metrics with all business baselines unmeasured.
- Portable Python packaging and a read-only GitHub Actions test/package workflow using pinned action revisions.

## Local verification

- The pre-change npm test baseline passed.
- The updated npm test passes all existing checks plus the 10 new team-practice tests.
- Skill structure validation passes for ana-team-practice.
- Independent forward-use produced a draft successfully. Review found missing exercise assets and checkpoint ownership; the candidate now supplies them. Validation-only mode now explicitly reports that no file was written.
- The previous package command failed because PowerShell was absent. The new Python packaging command succeeds; both archives were checked against manifest entry lists, source bytes, and SHA-256 checksum files.
- Changed source passes git diff --check.

GitHub CI is a separate result from local verification. Consult the PR's exact head checks before merge. No fresh Codex installation or cross-host installation was performed.

## Limits and release state

This is a reviewable source candidate, not a commercial or live accounting release. No prices, external sends, invoices, customer records, checkout products, or production websites were changed. Ana's method/identity and commercial approvals are not recorded by this work.

Input validators enforce documented structure and declared boundaries, not the authenticity of human approvals or absence of personal information in free text. The invoice helper has a bounded two-decimal currency set and one supplied tax rate. The team session is an unvalidated facilitation scaffold, with no clinical or neuroscience outcome claim.

Connected accounting, authenticated approvals, source-linked billable events, duplicate prevention, tenant isolation, and payment reconciliation remain proposed work. Rollback is a reviewed source revert and restoration of the previously validated plugin version. Existing editorial-contract PR #8 is separate.

Runtime/API spend for the delivered local helpers: no external calls. Model/tool session costs were not exposed, so no total cost is asserted.
