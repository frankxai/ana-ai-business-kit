# Use with Codex

Codex reads project-level `AGENTS.md` files when it starts work in a repository or workspace. This kit includes a small private `AGENTS.md` so the safety boundary travels with the folder.

1. Unzip `ana-operator-kit` into a private folder.
2. Open that folder as the Codex workspace. Keep `AGENTS.md`, `START-HERE.md`, and `reference/` in the folder.
3. Start a fresh task and paste the prompt from `prompts/OPERATOR-SETUP.md`.
4. Give Codex only the minimum approved source material needed for the current task.
5. Review the draft yourself; then manually personalize the client packet before sending.

## Safe first prompt

> Read `AGENTS.md`, `START-HERE.md`, and `reference/PRIVACY-AND-SCOPE.md`. We are preparing one approved [offer] for [date]. The intended human outcome is [outcome]. Use only the material below. Ask up to three questions if something material is missing. Create a labeled draft for my review; do not write to client files or send anything.

Do not add API keys, connectors, browser access, or client databases to make this kit work. They are not needed for the first client loop.
