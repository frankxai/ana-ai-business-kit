# Fork and install Ana HR Operations in Codex

The simplest route takes about five minutes. The commands are the same in Windows PowerShell, macOS Terminal, and most Linux terminals.

## Before you start

You need:

- Codex in the ChatGPT desktop app or the Codex CLI;
- a GitHub account only if you want your own fork;
- permission from your company to use the selected client information in Codex.

Do not add client or candidate records to the fork.

## Option A — install Frank's maintained version

Use this when Ana wants the quickest start and does not need to change the plugin yet.

```powershell
codex plugin marketplace add frankxai/ana-ai-business-kit --ref main
codex plugin add ana-hr-operations@ana-business-kit
codex plugin list
```

In the final output, find:

```text
ana-hr-operations@ana-business-kit  installed, enabled
```

Then close the current Codex task and start a new one. Plugin skills become available to new tasks after installation.

## Option B — fork it into Ana's GitHub first

Use this when Ana wants her own copy, private change process, or future custom templates and policies.

### Step 1: create the fork

1. Sign in to GitHub.
2. Open [frankxai/ana-ai-business-kit](https://github.com/frankxai/ana-ai-business-kit).
3. Select **Fork**.
4. Choose Ana's account or company organization.
5. Keep the repository name `ana-ai-business-kit` and create the fork.

GitHub's direct fork page is [Create a new fork](https://github.com/frankxai/ana-ai-business-kit/fork).

### Step 2: install from the fork

Replace `YOUR-GITHUB-USERNAME` with the owner shown in the fork's URL.

```powershell
codex plugin marketplace add YOUR-GITHUB-USERNAME/ana-ai-business-kit --ref main
codex plugin add ana-hr-operations@ana-business-kit
codex plugin list
```

No local clone is required for installation. To edit the repository later:

```powershell
git clone https://github.com/YOUR-GITHUB-USERNAME/ana-ai-business-kit.git
cd ana-ai-business-kit
npm test
```

Keep the fork public only if it contains blank templates and public-safe instructions. Use a private repository and company-approved access controls for internal policies. Live client and candidate data should remain outside either kind of fork.

## Connect Google Drive for Ana's templates

The HR plugin can make a local draft on its own. To read and copy Ana's real Google Docs template:

1. In the ChatGPT desktop app, open **Plugins** from Codex.
2. Open the **OpenAI** section and find **Google Drive**.
3. Select the plus button to install it.
4. Connect Ana's approved Google account when prompted.
5. Start another new Codex task after connecting.

Use the plugin screen for this connector setup. Do not rely on a `codex plugin add google-drive@...` command: connector availability is supplied through the Codex plugin directory and can differ from user-configured CLI marketplaces.

Gmail and Google Calendar are optional. Install them only when Ana wants draft-email or scheduling support. The HR plugin still requires active approval before any external send or calendar change.

## Verify in the Codex app

1. Open **Plugins** from Codex.
2. Check the **Installed** row for **Ana HR Operations**.
3. Start a new task.
4. Type `@` and select **Ana HR Operations**, or ask for it by name.
5. Use this safe test:

> Use Ana HR Operations. Explain the six stages and list the information you need before a first client call. Use placeholders only and do not create or send anything.

Expected stages: first call, kickoff, job description, offer, invoice, and send preparation.

## Keep a fork updated

Use GitHub's **Sync fork** button to bring Frank's new releases into Ana's `main` branch. Then refresh the Codex marketplace:

```powershell
codex plugin marketplace upgrade ana-business-kit
codex plugin list
```

Review changes before using an updated plugin with live client work.

## Migrate from the original `personal` release

The first release used the generic marketplace name `personal`. If `codex plugin marketplace list` shows that `personal` points to this Ana repository, migrate it once:

```powershell
codex plugin remove ana-hr-operations@personal
codex plugin marketplace remove personal
codex plugin marketplace add frankxai/ana-ai-business-kit --ref main
codex plugin add ana-hr-operations@ana-business-kit
codex plugin list
```

If Ana installs from her fork, replace `frankxai` in the marketplace-add command with her GitHub owner. Do not remove a marketplace named `personal` when it points to a different repository.

## Troubleshooting

### `codex` is not recognized

Install or update Codex, then reopen the terminal. In the ChatGPT desktop app, plugin browsing is also available from **Codex → Plugins**.

### The marketplace already exists

List configured sources:

```powershell
codex plugin marketplace list
```

If `ana-business-kit` already points to the correct repository, do not add it again. Run the plugin add command or upgrade it.

### The plugin is installed but Codex does not use it

Start a new task. Then type `@` and choose **Ana HR Operations** explicitly.

### Google Docs is blocked

Confirm that Google Drive is installed, the correct Google account is connected, and Ana supplied an exact template URL. The safe fallback is a local draft marked `TEMPLATE_BLOCKED`.

Official reference: [OpenAI's plugin installation and permissions guide](https://learn.chatgpt.com/docs/plugins).
