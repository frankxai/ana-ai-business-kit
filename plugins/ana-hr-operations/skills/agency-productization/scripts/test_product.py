#!/usr/bin/env python3
"""Behavioral failures for evidence, licensing, delivery scope and economics."""
import copy
import json
from pathlib import Path
import unittest
from validate_product import validate

EXAMPLE = json.loads((Path(__file__).resolve().parents[1] / 'assets/product.example.json').read_text())


class ProductTests(unittest.TestCase):
    def test_synthetic_draft(self):
        self.assertEqual(validate(EXAMPLE), [])

    def test_private_receipts_and_permitted_additions(self):
        record = copy.deepcopy(EXAMPLE)
        record['demo_only'] = False
        record['product_id'] = 'PRIVATE-PRODUCT-001'
        for i, receipt in enumerate(record['delivery_evidence']):
            receipt['reference'] = f'PRIVATE-DELIVERY-00{i + 1}'
        record['rights']['licensed_additions'] = [{'name': 'Original facilitator guide', 'rights_reference': 'PRIVATE-RIGHTS-001'}]
        self.assertEqual(validate(record), [])

    def test_failure_cases(self):
        cases = [
            ('ownership.product_owner', '', 'product_owner'),
            ('ownership.adaptation_owner', '', 'adaptation_owner'),
            ('ownership.approval_owner', '', 'approval_owner'),
            ('delivery_evidence', [], 'at least 2'),
            ('scope.included', [], 'at least 1'),
            ('scope.excluded', [], 'at least 1'),
            ('scope.acceptance', '', 'acceptance'),
            ('scope.implementation_hours_ceiling', 0, 'implementation_hours_ceiling'),
            ('scope.tool_spend_ceiling', float('nan'), 'finite'),
            ('rights.public_base_license', 'exclusive resale', 'CC-BY-4.0'),
            ('rights.exclusive_public_base_rights', True, 'exclusive_public_base_rights'),
            ('rights.ana_identity_included', True, 'ana_identity_included'),
            ('rights.attribution', '', 'attribution'),
            ('rights.third_party_review', '', 'third_party_review'),
            ('support.hours_ceiling', -1, 'hours_ceiling'),
            ('support.ends_on', '2020-01-01', 'precede'),
            ('support.updates_end_on', 'forever', 'ISO date'),
            ('outcomes.active_operators', 6, 'denominator'),
            ('outcomes.baseline_completed', 0, 'baseline_completed'),
            ('outcomes.baseline_quality_passed', 21, 'denominator'),
            ('outcomes.minimum_quality_rate', .7, 'preserve'),
            ('outcomes.quality_rubric', '', 'quality_rubric'),
            ('boundaries.clinical_claims', True, 'clinical_claims'),
            ('boundaries.employee_profiling', True, 'employee_profiling'),
            ('boundaries.private_reflection_included', True, 'private_reflection_included'),
            ('boundaries.identity_endorsement_claimed', True, 'identity_endorsement_claimed'),
            ('routes.invoice', 'new autonomous invoice tool', 'SOP-06'),
            ('review.owner', '', 'owner'),
            ('review.next_review_due', '2020-01-01', 'precede'),
            ('status', 'APPROVED_FOR_SALE', 'DRAFT_REVIEW_REQUIRED'),
            ('price', 10000, 'not an allowed field'),
            ('client_notes', 'PRIVATE DISCLOSURE', 'not an allowed field'),
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

    def test_duplicate_or_unreviewed_delivery_is_not_repeat_evidence(self):
        record = copy.deepcopy(EXAMPLE)
        record['delivery_evidence'][1]['reference'] = record['delivery_evidence'][0]['reference']
        self.assertTrue(any('distinct' in e for e in validate(record)))
        record = copy.deepcopy(EXAMPLE)
        record['delivery_evidence'][1]['reviewed'] = False
        self.assertTrue(validate(record))
        record = copy.deepcopy(EXAMPLE)
        record['delivery_evidence'][1]['workflow'] = 'Unrelated workshop'
        self.assertTrue(validate(record))

    def test_client_send_and_unknown_license_rights_fail(self):
        record = copy.deepcopy(EXAMPLE)
        record['artifacts'][0]['audience'] = 'client_sendable'
        self.assertTrue(validate(record))
        record = copy.deepcopy(EXAMPLE)
        record['rights']['licensed_additions'] = [{'name': 'Unverified add-on', 'rights_reference': ''}]
        self.assertTrue(validate(record))

    def test_malformed_json_shapes_fail_without_crashing(self):
        for value in [None, [], True, 'text', 12]:
            self.assertTrue(validate(value))
        for key in EXAMPLE:
            record = copy.deepcopy(EXAMPLE)
            record[key] = None
            self.assertTrue(validate(record), key)


if __name__ == '__main__':
    unittest.main()
