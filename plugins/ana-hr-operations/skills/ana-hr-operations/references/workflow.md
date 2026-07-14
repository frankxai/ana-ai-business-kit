# Engagement workflow

Use one engagement record per client and role. Never use chat history as the system of record. Execute the stage through `sop-index.md` and its named SOP.

## State sequence

1. `first-call` — capture the 20–30 minute discovery call.
2. `kickoff` — confirm scope, stakeholders, cadence, selection process, privacy, and next document.
3. `job-description` — create the role scorecard and job description when recruiting a role.
4. `offer` — create the service offer from Ana-approved scope and pricing.
5. `recruiting` — launch and operate the structured search after job-description approval; keep candidate data in the ATS.
6. `invoice` — create an invoice draft from the approved offer or completed milestone.
7. `send` — prepare the final email and attachment only after artifact and send approvals exist.

Job description and offer can run in parallel after kickoff. Recruiting depends on an approved job description and recruiting-launch approval. Invoice depends on an approved offer. Send depends on the relevant approved artifact plus fresh send approval.

## First-call output

Capture facts, open decisions, owner, due date, and the next artifact. Mark assumptions separately. Do not invent missing price, tax, payment, legal, role, or candidate facts. End the call with a short readback for the client to confirm.

## Kickoff output

Confirm:

- business outcome and role outcome;
- scope and exclusions;
- decision-makers and daily contact;
- document owners and approval deadlines;
- structured selection stages and job-relevant evidence;
- candidate-data handling and deletion expectations;
- communication cadence;
- Ana's approved Google Docs template and nearest comparable completed document;
- the private template-registry ID, platform (Google Docs or Canva), master-copy route, document owner, and visual-check requirement;
- pricing source, currency, billing identity, tax treatment, and payment terms.

## Administration rule

At every transition, write a short status block:

- current stage;
- complete facts;
- missing decisions;
- approvals obtained;
- next owner and due date;
- external action still requiring Ana.

Use `scripts/validate_engagement.py` before advancing a stage.

For each document route, prepare a content pack from approved facts before making a copy. Google Docs work requires copy/readback; Canva work requires copy plus a named visual check. A template/source/access gap remains `TEMPLATE_BLOCKED`; a Canva copy without visual review remains `CANVA_RENDER_PENDING`.

For multiple clients, run `SOP-00` and render `assets/daily-operations-board.md`. Use client aliases only; the board is not a system of record.
