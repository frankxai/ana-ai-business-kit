# Practice record contract

The validator checks a narrow structured planning record; it does not inspect natural-language meaning, prove consent, certify legal compliance, or audit external data access. Human source and privacy review is still necessary. Unknown structured fields are rejected so reflections and individual employee data cannot be added as convenient extra fields.

- `participation`: eligible, invited and consenting counts; voluntary participation, optional reflection, and an equivalent non-reflection activity. Counts are nonnegative integers with consenting ≤ invited ≤ eligible. Live choice records remain separately controlled; the shared plan contains no names or responses.
- `reporting`: employer output is aggregate workflow evidence only. At least five consenting participants and the owner's stricter minimum are required to release it; otherwise `suppressed` is true. Report consent cannot exceed participating consent, and lack of consent cannot reduce employment opportunity. Never report individual usage, reflection, rankings, attendance judgments, or group spiritual beliefs.
- `reflection`: `participant_only`, `collected=false`, `employer_access=false`, `ai_access=false`. This is storage policy metadata, not a place to store answers.
- `outcome`: one observable task definition, common quality rubric, baseline and pilot measurement windows, raw completed/quality-passed counts and total operator minutes. `pilot` may be null until measured. Report quality-passed/completed and minutes/completed; don't infer individual performance, causal impact, or statistical significance from a before/after comparison.
- `targets`: owner-proposed quality floor, maximum minutes per completed unit, maximum operator hours, tool spend ceiling/currency. Label targets separately from results. Count reviewer rework within operator time. A reduced task time must never hide a lower quality result.
- `evidence`: each claim has a source or private research-library reference, class, supported statement and limitations. Allowed classes are `primary_research`, `systematic_review`, `official_guidance`, `practice_hypothesis`. Review reference authenticity externally. Synthetic fixtures prove validator behavior only.
- `review`: named accountable roles, reviewed date and next review date. Public examples use fictional roles only.

All records remain drafts. On a failed condition, report the exact field and return to the owner; do not silently delete the disallowed request or manufacture an approval.
