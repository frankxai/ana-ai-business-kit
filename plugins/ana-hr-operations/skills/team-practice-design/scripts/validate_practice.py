#!/usr/bin/env python3
"""Validate a bounded team practice draft; never process participant reflections."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'scripts'))
from record_contracts import (obj, nonempty, number, array, expected, ordered_dates,
                              review, count_pair, reference, cli)

FIELDS = ['schema', 'demo_only', 'status', 'practice_id', 'workflow', 'scope',
          'participation', 'reflection', 'reporting', 'boundaries', 'outcome',
          'targets', 'evidence', 'review']


def validate(record):
    errors = []
    row = obj(record, FIELDS, 'practice', errors)
    expected(row.get('schema'), 'team-practice/v1', 'schema', errors)
    expected(row.get('status'), 'DRAFT_REVIEW_REQUIRED', 'status', errors)
    if type(row.get('demo_only')) is not bool:
        errors.append('demo_only must be a boolean.')
    reference(row.get('practice_id'), row.get('demo_only') is True, 'practice_id', errors)
    nonempty(row.get('workflow'), 'workflow', errors)
    scope = obj(row.get('scope'), ['included', 'excluded', 'facilitator', 'sponsor'], 'scope', errors)
    for key in ['included', 'excluded', 'facilitator', 'sponsor']:
        nonempty(scope.get(key), f'scope.{key}', errors)

    p = obj(row.get('participation'), ['eligible', 'invited', 'consenting', 'voluntary', 'reflection_optional', 'alternative'], 'participation', errors)
    counts = [number(p.get(key), f'participation.{key}', errors, 0, True) for key in ['eligible', 'invited', 'consenting']]
    if all(value is not None for value in counts) and not counts[2] <= counts[1] <= counts[0]:
        errors.append('participation counts must satisfy consenting <= invited <= eligible.')
    for key in ['voluntary', 'reflection_optional']:
        expected(p.get(key), True, f'participation.{key}', errors)
    nonempty(p.get('alternative'), 'participation.alternative', errors)
    reflection = obj(row.get('reflection'), ['storage', 'collected', 'employer_access', 'ai_access'], 'reflection', errors)
    expected(reflection.get('storage'), 'participant_only', 'reflection.storage', errors)
    for key in ['collected', 'employer_access', 'ai_access']:
        expected(reflection.get(key), False, f'reflection.{key}', errors)
    b = obj(row.get('boundaries'), ['clinical_claims', 'employee_profiling', 'emotion_inference', 'employment_decisions'], 'boundaries', errors)
    for key in ['clinical_claims', 'employee_profiling', 'emotion_inference', 'employment_decisions']:
        expected(b.get(key), False, f'boundaries.{key}', errors)

    r = obj(row.get('reporting'), ['audience', 'consenting', 'minimum_group_size', 'suppressed', 'fields', 'individual_assessment', 'task_data_scope'], 'reporting', errors)
    expected(r.get('audience'), 'employer_aggregate', 'reporting.audience', errors)
    n = number(r.get('consenting'), 'reporting.consenting', errors, 0, True)
    floor = number(r.get('minimum_group_size'), 'reporting.minimum_group_size', errors, 5, True)
    if n is not None and counts[2] is not None and n > counts[2]:
        errors.append('reporting.consenting exceeds voluntary participant count.')
    if type(r.get('suppressed')) is not bool:
        errors.append('reporting.suppressed must be a boolean.')
    if n is not None and floor is not None and n < floor and r.get('suppressed') is not True:
        errors.append('reporting must be suppressed below the minimum consenting group size.')
    expected(r.get('task_data_scope'), 'report_consented_only', 'reporting.task_data_scope', errors)
    expected(r.get('individual_assessment'), False, 'reporting.individual_assessment', errors)
    allowed = {'task_count', 'quality_pass_count', 'total_operator_minutes'}
    for field in array(r.get('fields'), 'reporting.fields', errors, 1):
        if not isinstance(field, str) or field not in allowed:
            errors.append('reporting.fields permits aggregate task metrics only.')

    outcome = obj(row.get('outcome'), ['task_definition', 'quality_rubric', 'baseline', 'pilot'], 'outcome', errors)
    for key in ['task_definition', 'quality_rubric']:
        nonempty(outcome.get(key), f'outcome.{key}', errors)
    baseline_rate = None
    for key in ['baseline', 'pilot']:
        value = outcome.get(key)
        if key == 'pilot' and value is None:
            continue
        path = f'outcome.{key}'
        period = obj(value, ['window_start', 'window_end', 'completed', 'quality_passed', 'operator_minutes'], path, errors)
        ordered_dates(period.get('window_start'), period.get('window_end'), path, errors)
        total, passed = count_pair(period, 'completed', 'quality_passed', path, errors)
        number(period.get('operator_minutes'), f'{path}.operator_minutes', errors, 0)
        if key == 'baseline' and total and passed is not None:
            baseline_rate = passed / total

    t = obj(row.get('targets'), ['minimum_quality_rate', 'maximum_minutes_per_unit', 'operator_hours_ceiling', 'tool_spend_ceiling', 'currency'], 'targets', errors)
    quality = number(t.get('minimum_quality_rate'), 'targets.minimum_quality_rate', errors, 0, maximum=1)
    if baseline_rate is not None and quality is not None and quality < baseline_rate:
        errors.append('targets.minimum_quality_rate must preserve the baseline quality rate.')
    for key in ['maximum_minutes_per_unit', 'operator_hours_ceiling']:
        number(t.get(key), f'targets.{key}', errors, 0.000001)
    number(t.get('tool_spend_ceiling'), 'targets.tool_spend_ceiling', errors)
    if t.get('currency') not in ['EUR', 'USD', 'GBP']:
        errors.append('targets.currency must be EUR, USD or GBP; extend explicitly for another currency.')
    for i, entry in enumerate(array(row.get('evidence'), 'evidence', errors, 1)):
        e = obj(entry, ['reference', 'class', 'statement', 'limitations'], f'evidence[{i}]', errors)
        reference(e.get('reference'), row.get('demo_only') is True, f'evidence[{i}].reference', errors)
        if e.get('class') not in ['primary_research', 'systematic_review', 'official_guidance', 'practice_hypothesis']:
            errors.append(f'evidence[{i}].class must identify evidence strength.')
        for key in ['statement', 'limitations']:
            nonempty(e.get(key), f'evidence[{i}].{key}', errors)
    review(row.get('review'), errors)
    return errors


if __name__ == '__main__':
    raise SystemExit(cli(validate))
