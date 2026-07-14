# Install Ana HR Operations and keep company work private

The public repository is the maintained learning and plugin source. Your actual template links, internal policy, client records, candidate records, commercial information, and credentials stay in a separately controlled private company workspace.

## Before you start

You need:

- Codex in the ChatGPT desktop app or Codex CLI;
- a private company-approved Drive/ATS/finance workspace for live work;
- permission from your company to use the selected information in Codex;
- Ana's decision on who can install, update, and approve the plugin.

Do not add live client or candidate records to GitHub.

## Option A — install Frank's maintained public-safe version

Use this for the quickest start. It contains blank templates, validation, fictional practice material, and operating instructions only.

```powershell
codex plugin marketplace add frankxai/ana-ai-business-kit --ref main
codex plugin add ana-hr-operations@ana-business-kit
codex plugin list
```

Look for:

```text
ana-hr-operations@ana-business-kit  installed, enabled
```

Then close the current Codex task and start a new one. Plugin skills become available in new tasks.

## Option B — create Ana's private company overlay

Use this when Ana needs company-specific templates, policies, role prompts, or a change history that only the internal team can access.

**Do not use a public fork to hold private material.** Fork visibility and permissions follow the upstream/repository policy; GitHub documents that public forks do not inherit private permissions. Create a separately initialized private repository or private internal mirror instead. [GitHub's fork visibility guidance](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/about-permissions-and-visibility-of-forks) explains the distinction.

### Step 1: create a separate private repository

In Ana's GitHub organization, create a new private repository such as `ana-hr-private-overlay` (not a GitHub fork). Give access only to Ana, the named internal team, and any explicitly approved technical maintainer.

It may contain:

- a private `template-registry.private.json` with real Drive/Canva links and ownership;
- company policy, approved language, pricing sources, and internal operating notes;
- role-specific local prompts and version receipts;
- no candidate CVs, interview evidence, employment records, credentials, or bank details.

It must not contain:

- copied live client/candidate material;
- secrets or payment credentials;
- a mirror that claims the public kit is private;
- unreviewed code or connectors.

Keep an `UPSTREAM.md` that records the public kit release/tag tested, the private overlay version, owner, and validation date. Bring public changes in deliberately through a pull request or reviewed copy; do not auto-sync into live operations.

### Step 2: install the public plugin and use private sources in tasks

The plugin still installs from the maintained public repository. In a private Codex task, Ana or the responsible team member can give Codex the exact private template source needed for the current action. Do not paste that URL into GitHub.

For a private, locally developed plugin clone, use the Codex plugin update/reinstall procedure only after the source and marketplace are confirmed local. The public project does not require the team to clone or edit Git in daily use.

## Connect Google Drive and Canva for Ana's templates

The HR plugin can make a labeled local draft on its own. It needs the matching connector to work with an existing master:

1. In the ChatGPT desktop app, open **Plugins** from Codex.
2. Install **Google Drive** for Google Docs and Google Sheets work; connect Ana's approved account.
3. Install **Canva** only when a Canva offer, invoice, or presentation master will be used; connect Ana's approved Canva account.
4. Start a new Codex task after connecting.
5. Give only the exact approved master link, destination folder, document type, and copy approval in that private task.

Use the plugin screen for connector setup. Connector availability can differ between the desktop app and CLI. Gmail and Google Calendar are optional and remain approval-gated.

## Verify safely

1. Open **Plugins** from Codex.
2. Check the **Installed** row for **Ana HR Operations**.
3. Start a new task.
4. Type `@` and select **Ana HR Operations**, or ask for it by name.
5. Run this safe practice prompt:

> Use Ana HR Operations. Use fictional placeholders only. Explain the SOPs, the four team roles, the template route, and the approval gates. Do not create, share, send, schedule, price, invoice, or publish anything.

Expected flow: first call, kickoff, job description and/or offer, recruiting, invoice, approved handoff. See [Practice engagement](PRACTICE-ENGAGEMENT.md).

## Keep the plugin current

Once per month, or before a new teammate starts:

```powershell
codex plugin marketplace upgrade ana-business-kit
codex plugin list
```

Then run the fictional practice engagement, review the changelog/validation receipt, and only then use the update for a live engagement. The precise checklist is in [Release and update checks](RELEASE-AND-UPDATE.md).

## Migrate from the original `personal` release

The first release used the generic marketplace name `personal`. If `codex plugin marketplace list` shows that `personal` points to this Ana repository, migrate it once:

```powershell
codex plugin remove ana-hr-operations@personal
codex plugin marketplace remove personal
codex plugin marketplace add frankxai/ana-ai-business-kit --ref main
codex plugin add ana-hr-operations@ana-business-kit
codex plugin list
```

Do not remove a marketplace named `personal` when it points to a different repository.

## Troubleshooting

### `codex` is not recognized

Install or update Codex, then reopen the terminal. In the ChatGPT desktop app, plugin browsing is available from **Codex → Plugins**.

### The marketplace already exists

List configured sources:

```powershell
codex plugin marketplace list
```

If `ana-business-kit` already points to the correct repository, do not add it again. Run the plugin add command or upgrade it.

### The plugin is installed but Codex does not use it

Start a new task. Then type `@` and choose **Ana HR Operations** explicitly.

### Google Docs or Canva is blocked

Confirm the right connector, the correct approved account, exact master access, destination access, and copy approval. The safe fallback is a local draft marked `TEMPLATE_BLOCKED` (or `CANVA_RENDER_PENDING` after a copy awaiting visual review). Never substitute a generic template and claim it is Ana's master.
