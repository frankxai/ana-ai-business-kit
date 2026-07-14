# Release and update checks

Use this checklist monthly, before a new teammate begins, and before relying on a material plugin update for live work. Do not let a background agent auto-update a live process.

## Who does what

| Action | Owner |
| --- | --- |
| Decide an update is worth testing | Ana |
| Update the team guide/private overlay and run practice | Named operations owner |
| Review technical change/validation | Frank or another approved technical reviewer |
| Approve release into live work | Ana |

## Update procedure

1. **Check the installed source and version.** In Codex, run `codex plugin list`. Record the installed marketplace, plugin version, date, and person checking it in `00 Governance & Team Setup/Version and update receipts`.
2. **Read the change.** Compare the public kit release/PR or maintained summary with the private overlay's `UPSTREAM.md`. Do not silently merge public changes into private instructions.
3. **Upgrade deliberately.** If Ana decides to test it:

   ```powershell
   codex plugin marketplace upgrade ana-business-kit
   codex plugin list
   ```

4. **Start a new Codex task.** Existing tasks may not load the new skill content.
5. **Run the fictional practice engagement.** Complete the acceptance checklist in [Practice engagement](PRACTICE-ENGAGEMENT.md). No client data.
6. **Review differences.** Check team prompts, permission matrix, real-template registry compatibility, research/content guardrails, and approval states.
7. **Record decision.** Ana explicitly records `approved for live pilot`, `hold`, or `revert`, with date and reason.
8. **Use on one live pilot first.** Do not expand a change to every active client until the pilot review passes.

## Private overlay update rules

- The overlay is a separately initialized private repository, not a public fork.
- It stores only private configuration, template links, policies, and process notes—not live candidates, client records, credentials, or bank details.
- Changes are reviewed in a branch/pull request or equivalent before the operating guide is changed.
- Its `UPSTREAM.md` records: public kit commit/tag, private-overlay revision, owner, validation date, and results.
- If a public update conflicts with Ana's policy or real templates, keep the update in `hold` and use the last known approved version.

## Teammate readiness check

A teammate is current only when all are true:

- they use their own account and current plugin version;
- they have read the role prompt and permission boundary;
- they have run the fictional practice case successfully;
- they know where candidate, client, template, and finance data belong;
- they can explain `TEMPLATE_BLOCKED`, `CANVA_RENDER_PENDING`, and fresh Ana approval;
- Ana has added them to the private workspace with the minimum necessary access.
