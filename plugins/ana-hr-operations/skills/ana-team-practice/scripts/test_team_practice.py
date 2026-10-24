import copy
import json
import unittest
from pathlib import Path
from team_practice import FLAGS, render, validate

class TeamPracticeTests(unittest.TestCase):
    def setUp(self):
        self.brief = json.loads((Path(__file__).resolve().parent.parent / 'assets/team-practice.example.json').read_text())

    def test_render_follow_through_and_ownership(self):
        self.assertEqual([], validate(self.brief))
        draft = render(self.brief)
        for value in ['HUMAN_REVIEW_REQUIRED', 'engagement\\_coordinator', '2026-10-08', '2026-10-15', '2026-10-31']:
            self.assertIn(value, draft)

    def test_demo_never_bypasses_boundaries(self):
        for key in FLAGS:
            brief = copy.deepcopy(self.brief)
            brief[key] = not brief[key]
            self.assertTrue(validate(brief), key)
            with self.assertRaises(ValueError):
                render(brief)

    def test_reject_extra_individual_records(self):
        self.brief['employee_records'] = [{'name': 'Fictional person'}]
        self.assertTrue(validate(self.brief))

    def test_reject_individual_fields_in_rows(self):
        self.brief['agreements'][0]['employee_name'] = 'Fictional person'
        self.assertTrue(validate(self.brief))

    def test_agenda_reconciles(self):
        self.brief['agenda'][0]['minutes'] = 6
        self.assertTrue(validate(self.brief))

    def test_review_after_session(self):
        self.brief['agreements'][0]['review_date'] = '2026-09-30'
        self.assertTrue(validate(self.brief))

    def test_malformed_inputs_fail_without_crash(self):
        for value in [None, [], 'text', 4, True]:
            self.assertTrue(validate(value))
        for key in ['agenda', 'agreements', 'evidence']:
            for value in [None, {}, 7, [None], ['text'], [False]]:
                brief = copy.deepcopy(self.brief)
                brief[key] = value
                self.assertTrue(validate(brief))

    def test_no_boolean_or_date_coercion(self):
        for key, value in [('voluntary', 'true'), ('duration_minutes', True), ('session_date', '20261001'), ('session_date', '9999-12-31')]:
            brief = copy.deepcopy(self.brief)
            brief[key] = value
            self.assertTrue(validate(brief))

    def test_sources_require_https_without_credentials(self):
        for value in ['http://example.com', 'https://user:secret@example.com', 'https://[', []]:
            self.brief['evidence'][0]['url'] = value
            self.assertTrue(validate(self.brief))

    def test_free_text_cannot_emit_html_or_new_heading(self):
        self.brief['purpose'] = '<script>alert(1)</script>\n# Approved'
        draft = render(self.brief)
        self.assertNotIn('<script>', draft)
        self.assertNotIn('\n# Approved', draft)

if __name__ == '__main__':
    unittest.main()
