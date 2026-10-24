#!/usr/bin/env python3
"""Behavioral failures for consent, reporting, denominators and owner boundaries."""
import copy
import json
from pathlib import Path
import unittest
from validate_practice import validate

EXAMPLE = json.loads((Path(__file__).resolve().parents[1] / 'assets/practice.example.json').read_text())


class PracticeTests(unittest.TestCase):
    def test_synthetic_draft_and_pending_measurement(self):
        self.assertEqual(validate(EXAMPLE), [])

    def test_completed_pilot_does_not_hide_low_quality(self):
        record = copy.deepcopy(EXAMPLE)
        record['outcome']['pilot'] = dict(record['outcome']['baseline'])
        record['outcome']['pilot']['quality_passed'] = 20
        self.assertEqual(validate(record), [])  # Observations remain truthful; targets stay fixed.

    def test_small_group_suppression_is_possible(self):
        record = copy.deepcopy(EXAMPLE)
        record['participation']['consenting'] = 3
        record['reporting']['consenting'] = 3
        record['reporting']['suppressed'] = True
        self.assertEqual(validate(record), [])

    def test_live_aliases_can_validate_without_personal_records(self):
        record = copy.deepcopy(EXAMPLE)
        record['demo_only'] = False
        record['practice_id'] = 'PRIVATE-PRACTICE-001'
        record['evidence'][0]['reference'] = 'PRIVATE-RESEARCH-001'
        self.assertEqual(validate(record), [])

    def test_failure_cases(self):
        cases = [
            ('participation.voluntary', False, 'voluntary'),
            ('participation.reflection_optional', False, 'reflection_optional'),
            ('participation.alternative', '', 'alternative'),
            ('participation.consenting', 9, 'consenting'),
            ('participation.eligible', True, 'eligible'),
            ('reflection.collected', True, 'collected'),
            ('reflection.employer_access', True, 'employer_access'),
            ('reflection.ai_access', True, 'ai_access'),
            ('reflection.answers', 'PRIVATE DISCLOSURE', 'not an allowed field'),
            ('reporting.consenting', 7, 'participant count'),
            ('reporting.consenting', 3, 'suppressed'),
            ('reporting.minimum_group_size', 2, 'minimum_group_size'),
            ('reporting.fields', ['employee_name'], 'aggregate task metrics'),
            ('reporting.task_data_scope', 'all_employees', 'task_data_scope'),
            ('reporting.individual_assessment', True, 'individual_assessment'),
            ('boundaries.clinical_claims', True, 'clinical_claims'),
            ('boundaries.employee_profiling', True, 'employee_profiling'),
            ('boundaries.emotion_inference', True, 'emotion_inference'),
            ('boundaries.employment_decisions', True, 'employment_decisions'),
            ('outcome.baseline.completed', 0, 'completed'),
            ('outcome.baseline.quality_passed', 41, 'denominator'),
            ('outcome.baseline.window_end', '2020-01-01', 'precede'),
            ('outcome.quality_rubric', '', 'quality_rubric'),
            ('targets.minimum_quality_rate', .7, 'preserve'),
            ('targets.operator_hours_ceiling', float('inf'), 'finite'),
            ('targets.tool_spend_ceiling', -1, 'tool_spend_ceiling'),
            ('scope.facilitator', '', 'facilitator'),
            ('scope.included', '', 'included'),
            ('review.owner', '', 'owner'),
            ('review.next_review_due', '2026-08-01', 'precede'),
            ('status', 'APPROVED', 'DRAFT_REVIEW_REQUIRED'),
            ('demo_only', False, 'PRIVATE-'),
            ('evidence', [], 'at least 1'),
        ]
        for path, value, expected in cases:
            with self.subTest(path=path, value=value):
                record = copy.deepcopy(EXAMPLE)
                target = record
                parts = path.split('.')
                for key in parts[:-1]:
                    target = target[key]
                target[parts[-1]] = value
                self.assertTrue(any(expected in e for e in validate(record)), validate(record))

    def test_evidence_cannot_be_promoted_or_have_limits_removed(self):
        for key, value in [('class', 'proven_neuroscience'), ('limitations', '')]:
            record = copy.deepcopy(EXAMPLE)
            record['evidence'][0][key] = value
            self.assertTrue(validate(record))

    def test_malformed_json_shapes_fail_without_crashing(self):
        for value in [None, [], True, 'text', 12]:
            self.assertTrue(validate(value))
        for key in EXAMPLE:
            record = copy.deepcopy(EXAMPLE)
            record[key] = None
            if key != 'pilot':
                self.assertTrue(validate(record), key)


if __name__ == '__main__':
    unittest.main()
