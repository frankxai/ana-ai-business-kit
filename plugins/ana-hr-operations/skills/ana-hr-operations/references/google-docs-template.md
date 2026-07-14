# Google Docs template fidelity

Use the installed `$google-docs` skill and the official Google Drive plugin for every live template operation.

## Hard preconditions

Require:

1. the exact approved template URL or document id;
2. the exact document type: kickoff, job description, offer, or invoice;
3. the nearest comparable completed document when available;
4. the intended destination folder and title;
5. Ana's approval to create a copy.
6. the private template-registry ID and a named owner for template fidelity.

If any precondition is missing, create only a labeled local draft and report `TEMPLATE_BLOCKED`. Do not search broadly through Drive for an unspecified template.

## Template-preserving route

1. Read the source through the connector.
2. Create a copy; never edit the master template.
3. Re-read the copy and record document id, URL, tab id, revision, section order, heading styles, tables, lists, links, and placeholders.
4. Map engagement fields to existing placeholders and sections.
5. Write the smallest verified batches using current indexes and revision control.
6. Re-read after each substantial write.
7. Compare the final structure with the source and nearest comparable document.
8. Keep the document labeled as a draft until Ana approves content and template fidelity.

Do not claim visual fidelity from plain text alone. If PDF export and page inspection are unavailable, report that rendered layout has not been verified.

## Canva boundary

For a Canva offer, invoice, or presentation, use the exact private Canva master and a separate content pack. Create a copy only, preserve the master visual system, and record `CANVA_RENDER_PENDING` until a named human completes an in-Canva visual check. Google Docs readback does not replace Canva visual review, and neither connector authorizes sharing or sending.
