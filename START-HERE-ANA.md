# Start here, Ana

This repository gives you a repeatable way to run the administrative side of an HR engagement without lowering your standard or handing decisions to AI.

Your normal path is:

> first client call → confirmed kickoff → job description and/or service offer → approved price → invoice draft → your approval to send

Codex remembers the structure through a private engagement record. It shows what is complete, what is missing, who owns the next action, and which approval is still required.

## What to do today

### 1. Install the HR plugin

Use the exact steps in [Fork and install in Codex](docs/FORK-AND-INSTALL-CODEX.md). You may install Frank's maintained version immediately or fork it into your own GitHub account first.

Forking is useful when you want your own copy and change history. It is not required to start.

### 2. Start a new Codex task

Installed plugins become available in new tasks. Paste this:

> Use Ana HR Operations. I have a new recruiting client. Set up a private engagement record outside the repository and guide me through the first-call capture one section at a time. Separate facts from assumptions. Do not send or schedule anything.

Codex should ask for the client outcome, role or service need, stakeholders, timing, process, document requirements, template source, pricing inputs, and next owner. If a fact is unknown, it remains an open decision.

### 3. Connect your Google Docs template

Install and connect Google Drive, then provide the template only inside the private Codex task. Do not paste the private template URL into GitHub.

Codex needs:

- the exact master-template URL;
- the document type;
- the closest approved completed example, if one exists;
- the destination folder and desired title;
- your approval to create a copy.

It must copy the master, never edit it. See [Google Docs setup](docs/GOOGLE-DOCS-SETUP.md).

### 4. Run one real client

Do not try to configure every possible service first. Run one active engagement through [the first-client walkthrough](docs/FIRST-CLIENT-FLOW.md), review where the structure helps, and then adjust your fork.

## Where information belongs

| Information | Where it belongs |
| --- | --- |
| Plugin instructions and blank templates | This GitHub repository |
| Live client engagement record | Private company-approved storage outside GitHub |
| Candidate CVs and interview evidence | Your approved ATS or HR system, not this repository |
| Master Google Docs template | Ana's controlled Google Drive |
| Local draft before Google Docs is connected | Private client folder, labeled draft |
| Final document | Copied Google Doc, reviewed and approved by Ana |

## Your approval gates

Codex must stop for you at four points:

1. Kickoff scope and role requirements.
2. Price, currency, tax treatment, and payment terms.
3. Invoice facts and final amount.
4. Exact recipient, channel, and permission to send.

Silence is never approval. If Codex is missing a fact, the correct result is a clear question or a blocked draft—not a guess.

## About the two ZIP downloads

The ZIPs solve a separate sharing problem:

- Keep the **Operator Kit** private for offers and reflective session preparation.
- Send only the reviewed **Client Session Kit** when a client needs preparation or aftercare material.

They are useful, but they are not required for the core HR plugin. Start with the plugin.
