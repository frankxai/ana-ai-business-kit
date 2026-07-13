# Ana AI Business Kit

A calm, privacy-first operating kit for a reflective-practice business. It helps a practitioner turn approved ideas into clear offers, prepared sessions, thoughtful aftercare, and reusable content—without putting AI in front of the client relationship.

## Two downloads, two jobs

| Download | For | It solves |
| --- | --- | --- |
| **Ana Operator Kit** | Ana or another practitioner | A private working space for offers, session preparation, approved aftercare, workshop planning, and content repurposing. It can be used in Codex or Claude Cowork. |
| **Client Session Kit** | A client receiving a session or circle | A clean, sendable preparation and aftercare pack. It requires no AI account and must be reviewed before it is sent. |

This separation is deliberate. A client never needs access to the operator prompts, private notes, or agent instructions.

## What makes this useful

The original FrankX starter had good raw material: an offer map, clarity session, guided circle, workshop, aftercare, and eight agent briefs. Its weakness was audience mixing: one ZIP asked a practitioner, a client, and a technical agent user to interpret the same folder. This release turns it into two short, usable paths.

The value is not a set of personalities. It is a disciplined loop:

1. Ana chooses one approved offer and one human outcome.
2. AI prepares a draft from only the material she supplies.
3. Ana edits, verifies, and sends the final client-facing material.
4. Repeated, approved patterns become a guide, template, or content seed.

## Start in five minutes

1. Download the two ZIPs from the repository release (or create them locally with `npm run package`).
2. Unzip **ana-operator-kit** into a private folder that is not shared with clients.
3. Choose [Codex setup](packages/ana-operator-kit/INSTALL-CODEX.md) or [Claude Cowork setup](packages/ana-operator-kit/INSTALL-CLAUDE-COWORK.md).
4. Read `START-HERE.md`, then run only the next real offer—not the whole system.
5. Send the **client-session-kit** only after you have reviewed and personalized it.

## Codex plugin for Ana's HR company

The repository also includes **Ana HR Operations**, an installable Codex plugin for client discovery, kickoff, recruiting setup, job descriptions, offers, approved pricing, invoice drafts, and administration.

```powershell
git clone https://github.com/frankxai/ana-ai-business-kit.git
codex plugin marketplace add ./ana-ai-business-kit
codex plugin add ana-hr-operations@personal
```

Install `google-drive@openai-curated` separately when Ana is ready to connect her real Google Docs template. The plugin requires the exact template URL, creates a copy, and blocks final document claims until connector readback verifies the result. Gmail is optional and is limited to preparing a draft after Ana explicitly approves the invoice and recipient.

Starter requests:

- “Run the first client call and capture everything needed for kickoff.”
- “Turn this approved kickoff into a job description using Ana’s Google Docs template.”
- “Create the 20–30 minute offer, verify pricing, and prepare an invoice draft.”

## Safety and privacy

- AI drafts and organizes; it does not diagnose, counsel, make clinical claims, decide for a client, or impersonate Ana.
- Keep raw client notes, contact data, recordings, health information, and employment-sensitive material out of public repositories and unapproved AI workspaces.
- Never promise a result, clinical outcome, hiring outcome, or confidentiality level you cannot actually provide.
- Pause and route to appropriate local, qualified support if a client discloses immediate danger or needs clinical, legal, or employment advice.
- Human approval is required before every client-facing output.

See [privacy and scope](packages/ana-operator-kit/reference/PRIVACY-AND-SCOPE.md) for the working boundary.

## Repository layout

```text
packages/
  ana-operator-kit/       # private practitioner workspace
  ana-client-session-kit/ # clean client-facing packet
scripts/                  # validation and reproducible ZIP creation
```

## Verify or package

No runtime, API key, or dependency installation is required.

```powershell
npm test
npm run package
```

`npm run package` creates two ZIP files and SHA-256 checksums under `dist/`. The generated artifacts are intentionally not committed.

## License and name use

The templates are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). “Ana”, Ana Cecilia Cancino’s name, voice, and identity are not licensed for reuse, endorsement, or impersonation. Replace all identity-specific text before adapting this kit for another practitioner.
