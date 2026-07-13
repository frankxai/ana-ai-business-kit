# Ana AI Business Kit instructions

This is a client-care toolkit, not an autonomous agent system.

- Keep client material private by default. Never add client names, transcripts, contact details, medical information, employment records, or credentials to Git.
- Draft only from material the practitioner explicitly provides. Do not invent biography, qualifications, testimonials, outcomes, or research claims.
- Keep AI backstage: a human must approve every client-facing output.
- Do not frame reflective practice as diagnosis, therapy, medical, legal, or HR advice.
- Preserve the two-package boundary. `ana-operator-kit` is private; `ana-client-session-kit` is the only sendable package.
- Run `npm test` after changes to manifests, package lists, or templates. Run `npm run package` before a release.
