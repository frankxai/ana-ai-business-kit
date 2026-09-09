#!/usr/bin/env python3
"""Validate a reusable agency product draft and its bounded operator obligations."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'scripts'))
from record_contracts import (obj, nonempty, number, array, expected, ordered_dates,
                              review, count_pair, reference, cli)

FIELDS = ['schema', 'demo_only', 'status', 'product_id', 'workflow', 'buyer', 'job',
          'ownership', 'delivery_evidence', 'scope', 'artifacts', 'rights',
          'support', 'outcomes', 'boundaries', 'routes', 'review']


def validate(record):
    errors = []
    row = obj(record, FIELDS, 'product', errors)
    expected(row.get('schema'), 'agency-product/v1', 'schema', errors)
    expected(row.get('status'), 'DRAFT_REVIEW_REQUIRED', 'status', errors)
    if type(row.get('demo_only')) is not bool:
        errors.append('demo_only must be a boolean.')
    reference(row.get('product_id'), row.get('demo_only') is True, 'product_id', errors)
    for key in ['workflow', 'job']:
        nonempty(row.get(key), key, errors)
    if row.get('buyer') not in ['agency_operators', 'team_leaders', 'founder_hosts']:
        errors.append('buyer must identify a supported product operator.')
    own = obj(row.get('ownership'), ['product_owner', 'adaptation_owner', 'approval_owner'], 'ownership', errors)
    for key in ['product_owner', 'adaptation_owner', 'approval_owner']:
        nonempty(own.get(key), f'ownership.{key}', errors)
    seen = set()
    for i, value in enumerate(array(row.get('delivery_evidence'), 'delivery_evidence', errors, 2)):
        path = f'delivery_evidence[{i}]'
        d = obj(value, ['reference', 'reviewed', 'workflow', 'completed', 'quality_passed'], path, errors)
        ref = d.get('reference')
        reference(ref, row.get('demo_only') is True, f'{path}.reference', errors)
        if isinstance(ref, str):
            if ref in seen:
                errors.append('delivery_evidence must contain distinct receipts.')
            seen.add(ref)
        expected(d.get('reviewed'), True, f'{path}.reviewed', errors)
        expected(d.get('workflow'), row.get('workflow'), f'{path}.workflow', errors)
        count_pair(d, 'completed', 'quality_passed', path, errors)

    scope = obj(row.get('scope'), ['included', 'excluded', 'acceptance', 'implementation_hours_ceiling', 'tool_spend_ceiling', 'currency'], 'scope', errors)
    for key in ['included', 'excluded']:
        for item in array(scope.get(key), f'scope.{key}', errors, 1):
            nonempty(item, f'scope.{key} item', errors)
    nonempty(scope.get('acceptance'), 'scope.acceptance', errors)
    number(scope.get('implementation_hours_ceiling'), 'scope.implementation_hours_ceiling', errors, 0.000001)
    number(scope.get('tool_spend_ceiling'), 'scope.tool_spend_ceiling', errors)
    if scope.get('currency') not in ['EUR', 'USD', 'GBP']:
        errors.append('scope.currency must be EUR, USD or GBP; extend explicitly for another currency.')
    for i, artifact in enumerate(array(row.get('artifacts'), 'artifacts', errors, 1)):
        a = obj(artifact, ['name', 'audience'], f'artifacts[{i}]', errors)
        nonempty(a.get('name'), f'artifacts[{i}].name', errors)
        if a.get('audience') not in ['operator_only', 'client_review_required']:
            errors.append(f'artifacts[{i}].audience must preserve the operator/client boundary.')

    rights = obj(row.get('rights'), ['public_base_license', 'attribution', 'exclusive_public_base_rights', 'ana_identity_included', 'third_party_review', 'licensed_additions'], 'rights', errors)
    expected(rights.get('public_base_license'), 'CC-BY-4.0', 'rights.public_base_license', errors)
    for key in ['exclusive_public_base_rights', 'ana_identity_included']:
        expected(rights.get(key), False, f'rights.{key}', errors)
    for key in ['attribution', 'third_party_review']:
        nonempty(rights.get(key), f'rights.{key}', errors)
    for i, addition in enumerate(array(rights.get('licensed_additions'), 'rights.licensed_additions', errors)):
        a = obj(addition, ['name', 'rights_reference'], f'rights.licensed_additions[{i}]', errors)
        nonempty(a.get('name'), f'rights.licensed_additions[{i}].name', errors)
        reference(a.get('rights_reference'), row.get('demo_only') is True, f'rights.licensed_additions[{i}].rights_reference', errors)

    support = obj(row.get('support'), ['starts_on', 'ends_on', 'hours_ceiling', 'updates_end_on'], 'support', errors)
    ordered_dates(support.get('starts_on'), support.get('ends_on'), 'support', errors)
    ordered_dates(support.get('starts_on'), support.get('updates_end_on'), 'support.updates', errors)
    number(support.get('hours_ceiling'), 'support.hours_ceiling', errors)
    out = obj(row.get('outcomes'), ['eligible_operators', 'active_operators', 'quality_rubric', 'baseline_completed', 'baseline_quality_passed', 'minimum_quality_rate', 'maximum_operator_hours_per_engagement'], 'outcomes', errors)
    count_pair(out, 'eligible_operators', 'active_operators', 'outcomes', errors)
    total, passed = count_pair(out, 'baseline_completed', 'baseline_quality_passed', 'outcomes', errors)
    quality = number(out.get('minimum_quality_rate'), 'outcomes.minimum_quality_rate', errors, 0, maximum=1)
    if total and passed is not None and quality is not None and quality < passed / total:
        errors.append('outcomes.minimum_quality_rate must preserve baseline quality.')
    nonempty(out.get('quality_rubric'), 'outcomes.quality_rubric', errors)
    number(out.get('maximum_operator_hours_per_engagement'), 'outcomes.maximum_operator_hours_per_engagement', errors, 0.000001)
    boundary_keys = ['clinical_claims', 'employee_profiling', 'private_reflection_included', 'identity_endorsement_claimed']
    b = obj(row.get('boundaries'), boundary_keys, 'boundaries', errors)
    for key in boundary_keys:
        expected(b.get(key), False, f'boundaries.{key}', errors)
    routes = obj(row.get('routes'), ['offer', 'invoice', 'content', 'templates'], 'routes', errors)
    for key, target in [('offer', 'SOP-04'), ('invoice', 'SOP-06'), ('content', 'ana-approved-content'), ('templates', 'ana-template-studio')]:
        expected(routes.get(key), target, f'routes.{key}', errors)
    review(row.get('review'), errors)
    return errors


if __name__ == '__main__':
    raise SystemExit(cli(validate))
