"""Small dependency-free primitives for draft-only structured record validation."""
from datetime import date
import json
import math
from pathlib import Path
import re
import sys


def obj(value, fields, path, errors):
    if not isinstance(value, dict):
        errors.append(f'{path} must be an object.')
        return {}
    for key in set(value) - set(fields):
        errors.append(f'{path}.{key} is not an allowed field.')
    for key in set(fields) - set(value):
        errors.append(f'{path}.{key} is required.')
    return value


def nonempty(value, path, errors):
    if not isinstance(value, str) or not value.strip():
        errors.append(f'{path} must be nonempty text.')


def number(value, path, errors, minimum=0, integer=False, maximum=None):
    valid = type(value) is int if integer else type(value) in (int, float)
    valid = valid and (type(value) is int or math.isfinite(value)) and value >= minimum
    valid = valid and (maximum is None or value <= maximum)
    if not valid:
        errors.append(f'{path} must be a finite {"integer" if integer else "number"} >= {minimum}' + (f' and <= {maximum}' if maximum is not None else '') + '.')
        return None
    return value


def array(value, path, errors, minimum=0):
    if not isinstance(value, list) or len(value) < minimum:
        errors.append(f'{path} must be a list with at least {minimum} item(s).')
        return []
    return value


def expected(value, target, path, errors):
    if type(value) is not type(target) or value != target:
        errors.append(f'{path} must be {target!r}.')


def iso(value, path, errors):
    try:
        if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
            raise ValueError()
        return date.fromisoformat(value)
    except (ValueError, TypeError):
        errors.append(f'{path} must be an ISO date.')
        return None


def ordered_dates(start, end, path, errors):
    a, b = iso(start, f'{path}.start', errors), iso(end, f'{path}.end', errors)
    if a and b and b < a:
        errors.append(f'{path} end must not precede start.')


def review(value, errors):
    row = obj(value, ['owner', 'reviewed_at', 'next_review_due'], 'review', errors)
    nonempty(row.get('owner'), 'review.owner', errors)
    ordered_dates(row.get('reviewed_at'), row.get('next_review_due'), 'review', errors)


def count_pair(row, total_key, pass_key, path, errors, minimum=1):
    total = number(row.get(total_key), f'{path}.{total_key}', errors, minimum, True)
    passed = number(row.get(pass_key), f'{path}.{pass_key}', errors, 0, True)
    if total is not None and passed is not None and passed > total:
        errors.append(f'{path}.{pass_key} exceeds denominator {total_key}.')
    return total, passed


def reference(value, demo, path, errors):
    prefix = 'SYNTHETIC' if demo else 'PRIVATE'
    if not isinstance(value, str) or not re.fullmatch(prefix + r'-[A-Z0-9][A-Z0-9._-]{2,127}', value):
        errors.append(f'{path} must be a {prefix}- reference.')


def cli(validate):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('record', type=Path)
    args = parser.parse_args()
    try:
        record = json.loads(args.record.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        print(f'Cannot read JSON record: {exc}', file=sys.stderr)
        return 1
    errors = validate(record)
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print('Validated draft structure; human review and action authorization remain separate.')
    return 0
