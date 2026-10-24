#!/usr/bin/env python3
"""Validate team-level facts and render an internal practice review draft."""
import argparse
import json
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urlparse

TEXT = ('team_alias', 'purpose', 'facilitator_role', 'reviewer_role', 'participation_notice', 'neutral_alternative')
FLAGS = {'non_clinical': True, 'voluntary': True, 'individual_assessment': False, 'spiritual_content': False, 'contains_personal_data': False, 'human_data_review_complete': True}
KEYS = set(TEXT) | set(FLAGS) | {'schema', 'demo_only', 'reporting', 'session_date', 'duration_minutes', 'agenda', 'agreements', 'evidence'}

def has_text(value):
    return isinstance(value, str) and bool(value.strip())

def iso_date(value):
    try:
        parsed = date.fromisoformat(value) if isinstance(value, str) else None
        return parsed if parsed and parsed.isoformat() == value else None
    except ValueError:
        return None

def validate(brief):
    if not isinstance(brief, dict):
        return ['Brief must be a JSON object.']
    errors = []
    if set(brief) - KEYS:
        errors.append('Unknown fields are not accepted; keep individual records outside this contract.')
    if brief.get('schema') != 'team-practice/v1':
        errors.append('schema must be team-practice/v1.')
    for key in TEXT:
        if not has_text(brief.get(key)):
            errors.append(f'{key} must be non-empty text.')
    for key, expected in FLAGS.items():
        if brief.get(key) is not expected:
            errors.append(f'{key} must be {expected}.')
    if 'demo_only' in brief and type(brief['demo_only']) is not bool:
        errors.append('demo_only must be boolean.')
    if brief.get('reporting') != 'process_outputs_only':
        errors.append('reporting must be process_outputs_only.')
    session = iso_date(brief.get('session_date'))
    if session is None or session > date.max - timedelta(days=30):
        errors.append('session_date must be YYYY-MM-DD and allow a 30-day follow-through.')
    duration = brief.get('duration_minutes')
    if type(duration) is not int or not 15 <= duration <= 120:
        errors.append('duration_minutes must be an integer from 15 to 120.')
    specs = {'agenda': ({'minutes', 'activity'}, ('activity',)), 'agreements': ({'behavior', 'owner_role', 'review_date'}, ('behavior', 'owner_role')), 'evidence': ({'url', 'limits'}, ('url', 'limits'))}
    total = 0
    for key, (allowed, texts) in specs.items():
        entries = brief.get(key)
        if not isinstance(entries, list) or not entries:
            errors.append(f'{key} must be a non-empty list.')
            continue
        for index, entry in enumerate(entries):
            label = f'{key}[{index}]'
            if not isinstance(entry, dict) or set(entry) != allowed:
                errors.append(f'{label} must contain exactly {sorted(allowed)}.')
                continue
            for field in texts:
                if not has_text(entry.get(field)):
                    errors.append(f'{label}.{field} must be non-empty text.')
            if key == 'agenda':
                minutes = entry.get('minutes')
                if type(minutes) is not int or not 1 <= minutes <= 120:
                    errors.append(f'{label}.minutes must be an integer from 1 to 120.')
                else:
                    total += minutes
            elif key == 'agreements':
                review = iso_date(entry.get('review_date'))
                if review is None or (session and review < session):
                    errors.append(f'{label}.review_date must be at or after the session.')
            else:
                try:
                    url = urlparse(entry['url'] if isinstance(entry['url'], str) else '')
                    if url.scheme != 'https' or not url.hostname or url.username or url.password:
                        errors.append(f'{label}.url must be HTTPS without credentials.')
                except ValueError:
                    errors.append(f'{label}.url is malformed.')
    if type(duration) is int and total != duration:
        errors.append('Agenda minutes must total duration_minutes.')
    return errors

def clean(value):
    value = ' '.join(str(value).split())
    for char in ('\\', '`', '*', '_', '[', ']', '<', '>', '|', '#', '!'):
        value = value.replace(char, '\\' + char)
    return value

def render(brief):
    errors = validate(brief)
    if errors:
        raise ValueError('; '.join(errors))
    rows = ['# Team practice — internal review draft', '', 'Status: HUMAN_REVIEW_REQUIRED', '']
    rows += [f'{key}: {clean(brief[key])}' for key in TEXT]
    rows += ['', f"Session: {brief['session_date']} · {brief['duration_minutes']} minutes", '', '## Proposed agenda', '']
    rows += [f"- {item['minutes']} min: {clean(item['activity'])}" for item in brief['agenda']]
    rows += ['', '## Proposed agreements', '']
    rows += [f"- {clean(item['behavior'])} Owner: {clean(item['owner_role'])}. Review: {item['review_date']}." for item in brief['agreements']]
    rows += ['', '## Follow-through', '']
    for days, action in [(7, 'Coordinator: check usability'), (14, 'Facilitator: review process adoption'), (30, 'Practice owner: retain, amend, or retire agreements')]:
        rows.append(f"- {iso_date(brief['session_date']) + timedelta(days=days)}: {action}.")
    rows += ['', 'Checkpoint roles are proposed and need confirmation. Agreement-specific dates are additional reviews; reconcile them with these checkpoints before delivery.', '', 'Use the bundled handoff-rehearsal.md for the fictional exercise and checklist.', '', '## Evidence and limits', '']
    rows += [f"- Source: {clean(item['url'])}. Limits: {clean(item['limits'])}" for item in brief['evidence']]
    rows += ['', 'Report process outputs only. Human content and suitability review is required. This is not approved or client-sendable.', '']
    return '\n'.join(rows)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('brief', type=Path)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    try:
        draft = render(json.loads(args.brief.read_text(encoding='utf-8')))
        if args.out:
            if args.out.resolve() == args.brief.resolve():
                raise ValueError('Output must not overwrite the source brief.')
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(draft, encoding='utf-8')
    except (OSError, ValueError) as error:
        parser.exit(1, f'Team practice blocked: {error}\n')
    print('Rendered internal review draft. Status: HUMAN_REVIEW_REQUIRED' if args.out else 'Brief validated; no file written. Use --out to render a review draft.')

if __name__ == '__main__':
    main()
