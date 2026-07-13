# Connect Ana's Google Docs template

The goal is template fidelity: keep Ana's approved structure and styling while replacing only the intended content.

## One-time setup

1. In the ChatGPT desktop app, open **Plugins** from Codex.
2. Find **Google Drive** in the **OpenAI** section and install it with the plus button.
3. Connect the approved Google account from the plugin screen.
4. Confirm that the account can read the master template and create a copy in the destination folder.
5. Keep the master template in a controlled folder with appropriate permissions.

Do not put the template URL, client folder URL, or customer identifiers in this public repository.

## What to provide in the private task

- Exact approved template URL or document ID.
- Document type: kickoff, job description, offer, or invoice.
- Nearest comparable completed document, when available.
- Intended destination folder.
- New document title.
- Explicit approval to create a copy.

Use this prompt:

> Use Ana HR Operations and Google Docs. The exact approved master template is [private URL]. Create a copy in [private destination folder] titled [title]. The document type is [type]. [Comparable document URL] is the nearest approved example. Preserve the source structure, edit the copy only, re-read the result, and keep it labeled draft. Do not send or share it.

## What Codex must verify

1. It can read the source template.
2. It creates a copy and never edits the master.
3. It records the new document ID and URL.
4. It preserves the visible section order, headings, tables, lists, links, and placeholders exposed by the connector.
5. It writes in small batches and re-reads after substantial changes.
6. It compares the finished structure with the source and comparable example.
7. It reports whether rendered page layout was actually inspected.

Connector readback confirms document structure, not necessarily visual page fidelity. If a PDF export or rendered-page inspection was not performed, Codex must say so.

## When to stop

The document remains `TEMPLATE_BLOCKED` when the exact template, access, destination, or copy approval is missing. In that case Codex may make a private local Markdown draft, but it must not claim that the final Google Doc exists.

The document remains a draft until Ana approves both its content and its template fidelity.
