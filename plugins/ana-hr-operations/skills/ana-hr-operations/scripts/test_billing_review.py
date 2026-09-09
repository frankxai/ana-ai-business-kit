#!/usr/bin/env python3
"""Synthetic regression tests for local invoice review boundaries."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import copy
from decimal import Decimal
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

import billing_review as ledger
from render_documents import render


SCRIPT = Path(__file__).with_name("billing_review.py")
ASSETS = SCRIPT.parent.parent / "assets"
EXAMPLE = ledger.read_json(ASSETS / "engagement.example.json")


class BillingReviewTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.path = self.directory / "review.sqlite3"
        self.agency = "AGENCY-DEMO"
        self.source = self.directory / "source.txt"
        self.source.write_bytes(b"Fictional completed kickoff; EUR 1000.00; not real approval.\n")
        self.record = copy.deepcopy(EXAMPLE)
        self.event = {
            "schema_version": "billing-event/v1", "agency_alias": self.agency,
            "event_id": "EVENT-DEMO-001", "engagement_id": self.record["engagement_id"],
            "source_reference": "SOURCE-DEMO", "source_sha256": ledger.digest(self.source.read_bytes()),
            "source_review_reference": "SOURCE-REVIEW-DEMO", "evidence_reference": "DELIVERY-DEMO",
            "currency": "EUR", "billable_subtotal": "1000.00",
            "finance_destination_reference": "FINANCE-DEMO",
            "policy_version": "POLICY-DEMO-v1",
        }
        ledger.initialize(self.path, self.agency)
        ledger.record_event(self.path, self.agency, self.event, self.source)

    def prepare(self, record=None, event_id=None):
        return ledger.prepare(self.path, self.agency, event_id or self.event["event_id"], self.record if record is None else record)

    def artifact(self, receipt, filename="invoice.md"):
        out = self.directory / filename
        ledger.export(self.path, self.agency, receipt["revision_id"], receipt["receipt_sha256"], out)
        return out

    def acknowledge(self, receipt, record=None, artifact=None):
        record = self.record if record is None else record
        artifact = render(record, "invoice").encode() if artifact is None else artifact
        return ledger.review(self.path, self.agency, receipt["revision_id"], receipt["receipt_sha256"], record, artifact, "REVIEWER-DEMO", "MANUAL-REVIEW-DEMO")

    def test_shipped_source_and_event_fixture(self):
        event = ledger.read_json(ASSETS / "billing-event.example.json")
        result = ledger.validate_event(event, event["agency_alias"], ASSETS / "billing-source.example.md")
        self.assertEqual(result["billable_subtotal"], "1000.00")
        example = copy.deepcopy(EXAMPLE)
        artifact = ledger.validate_record(example)
        receipt = ledger.receipt_content(result, example, artifact)
        self.assertEqual(receipt["source_sha256"], event["source_sha256"])
        self.assertEqual(receipt["finance_destination_reference"], "FINANCE-DEMO")
        self.assertEqual(receipt["payment_details_reference"], "APPROVED-FINANCE-PROFILE")

    def test_source_mismatch_and_immutable_event(self):
        retry = ledger.record_event(self.path, self.agency, self.event, self.source)
        self.assertFalse(retry["created"])
        self.assertFalse(retry["source_review_verified"])
        for field, value in [("policy_version", "POLICY-v2"), ("source_review_reference", "OTHER-REVIEW")]:
            changed = dict(self.event, **{field: value})
            with self.assertRaisesRegex(ledger.LedgerError, "Immutable"):
                ledger.record_event(self.path, self.agency, changed, self.source)
        self.source.write_bytes(b"Edited source")
        with self.assertRaisesRegex(ledger.LedgerError, "SHA256"):
            ledger.record_event(self.path, self.agency, self.event, self.source)

    def test_malformed_events_fail_closed(self):
        cases = [[], None, dict(self.event, unknown=True), dict(self.event, schema_version="billing-event/v2")]
        for field, value in [("billable_subtotal", "0"), ("billable_subtotal", "1000.001"), ("billable_subtotal", "NaN"), ("billable_subtotal", True), ("currency", "JPY"), ("currency", []), ("evidence_reference", "bad reference"), ("agency_alias", "OTHER"), ("source_sha256", "bad")]:
            cases.append(dict(self.event, **{field: value}))
        missing = dict(self.event)
        missing.pop("source_review_reference")
        cases.append(missing)
        for case in cases:
            with self.subTest(case=case), self.assertRaises(ValueError):
                ledger.record_event(self.path, self.agency, case, self.source)
        self.assertEqual(ledger.status(self.path, self.agency)["revisions"], [])

    def test_event_matches_engagement_currency_and_amount(self):
        for field, value in [("engagement_id", "OTHER-ENGAGEMENT"), ("currency", "USD"), ("billable_subtotal", "999.00")]:
            event = dict(self.event, event_id="EVENT-" + field, **{field: value})
            ledger.record_event(self.path, self.agency, event, self.source)
            with self.subTest(field=field), self.assertRaises(ledger.LedgerError):
                self.prepare(event_id=event["event_id"])
        self.assertEqual(ledger.status(self.path, self.agency)["revisions"], [])

    def test_duplicate_number_and_second_invoice_for_event_blocked(self):
        first = self.prepare()
        self.assertEqual(self.prepare()["revision_id"], first["revision_id"])
        other = dict(self.event, event_id="EVENT-OTHER")
        ledger.record_event(self.path, self.agency, other, self.source)
        with self.assertRaisesRegex(ledger.LedgerError, "reserved"):
            self.prepare(event_id=other["event_id"])
        changed = copy.deepcopy(self.record)
        changed["invoice"]["invoice_number"] = "DRAFT-SECOND"
        with self.assertRaisesRegex(ledger.LedgerError, "reserved"):
            self.prepare(changed)
        self.assertEqual(len(ledger.status(self.path, self.agency)["revisions"]), 1)

    def test_review_is_manual_and_json_approver_does_not_grant_it(self):
        self.record["approvals"]["invoice"]["approved_by"] = "FORGED-APPROVER"
        first = self.prepare()
        self.assertEqual(first["state"], "HUMAN_REVIEW_REQUIRED")
        artifact = self.artifact(first)
        checked = ledger.check(self.path, self.agency, first["revision_id"], first["receipt_sha256"], self.record, artifact.read_bytes())
        self.assertEqual(checked["state"], "HUMAN_REVIEW_REQUIRED")
        reviewed = self.acknowledge(first, artifact=artifact.read_bytes())
        self.assertEqual(reviewed["state"], "LOCAL_REVIEW_ACKNOWLEDGED")
        self.assertEqual(reviewed["reviewer_alias"], "REVIEWER-DEMO")
        self.assertFalse(reviewed["authenticated"])
        self.assertFalse(reviewed["external_send_allowed"])
        self.assertEqual(self.acknowledge(first)["reviewed_at"], reviewed["reviewed_at"])
        with self.assertRaisesRegex(ledger.LedgerError, "immutable manual"):
            ledger.review(self.path, self.agency, first["revision_id"], first["receipt_sha256"], self.record, artifact.read_bytes(), "OTHER", "OTHER")

    def test_changed_and_reverted_content_never_revives_old_review(self):
        first = self.prepare()
        self.acknowledge(first)
        changed = copy.deepcopy(self.record)
        changed["invoice"]["line_items"][0]["description"] = "Changed fictional kickoff description"
        second = self.prepare(changed)
        self.assertNotEqual(second["revision_id"], first["revision_id"])
        self.assertEqual(second["state"], "HUMAN_REVIEW_REQUIRED")
        with self.assertRaisesRegex(ledger.LedgerError, "superseded"):
            self.acknowledge(first)
        self.acknowledge(second, changed)
        third = self.prepare()
        self.assertNotIn(third["revision_id"], [first["revision_id"], second["revision_id"]])
        self.assertNotEqual(third["receipt_sha256"], first["receipt_sha256"])
        self.assertEqual(third["state"], "HUMAN_REVIEW_REQUIRED")
        history = ledger.status(self.path, self.agency)["revisions"]
        self.assertEqual(len(history), 3)
        self.assertEqual(sum(row["current"] for row in history), 1)
        self.assertEqual(sum(bool(row["reviewed_at"]) for row in history), 2)

    def test_entire_record_changes_invalidate_even_when_not_rendered(self):
        first = self.prepare()
        self.acknowledge(first)
        changed = copy.deepcopy(self.record)
        changed["administration"]["next_action"] = "Different internal next action"
        self.assertEqual(render(self.record, "invoice"), render(changed, "invoice"))
        with self.assertRaisesRegex(ledger.LedgerError, "differs"):
            ledger.check(self.path, self.agency, first["revision_id"], first["receipt_sha256"], changed, render(changed, "invoice").encode())
        second = self.prepare(changed)
        self.assertNotEqual(first["receipt"]["engagement_sha256"], second["receipt"]["engagement_sha256"])
        self.assertEqual(second["state"], "HUMAN_REVIEW_REQUIRED")

    def test_recipient_change_and_numeric_type_change_bind_new_revision(self):
        first = self.prepare()
        changed = copy.deepcopy(self.record)
        changed["client"]["billing_email"] = "other@example.invalid"
        second = self.prepare(changed)
        self.assertNotEqual(first["receipt_sha256"], second["receipt_sha256"])
        changed["invoice"]["subtotal"] = "1000.0"
        third = self.prepare(changed)
        self.assertNotEqual(third["receipt"]["engagement_sha256"], second["receipt"]["engagement_sha256"])
        self.assertEqual(ledger.canonical(Decimal("1000.0")), ledger.canonical(1000))
        self.assertNotEqual(ledger.canonical(Decimal("1000.0")), ledger.canonical("1000"))

    def test_payment_instructions_and_accounting_destination_are_distinct(self):
        first = self.prepare()
        self.assertEqual(first["receipt"]["finance_destination_reference"], "FINANCE-DEMO")
        self.assertEqual(first["receipt"]["payment_details_reference"], "APPROVED-FINANCE-PROFILE")
        self.record["invoice"]["payment_details_reference"] = "OTHER-PAYMENT-PROFILE"
        changed = self.prepare()
        self.assertNotEqual(first["receipt_sha256"], changed["receipt_sha256"])
        self.assertEqual(changed["receipt"]["finance_destination_reference"], "FINANCE-DEMO")

    def test_edited_artifact_and_wrong_receipt_cannot_be_reviewed(self):
        first = self.prepare()
        artifact = self.artifact(first).read_bytes()
        with self.assertRaisesRegex(ledger.LedgerError, "differs"):
            self.acknowledge(first, artifact=artifact + b"Edited")
        with self.assertRaisesRegex(ledger.LedgerError, "receipt SHA256"):
            ledger.check(self.path, self.agency, first["revision_id"], "0" * 64, self.record, artifact)
        self.acknowledge(first)
        with self.assertRaisesRegex(ledger.LedgerError, "differs"):
            ledger.check(self.path, self.agency, first["revision_id"], first["receipt_sha256"], self.record, artifact + b"Edited")

    def test_renderer_bytes_are_exactly_the_exported_bytes(self):
        first = self.prepare()
        exported = self.artifact(first)
        if sys.platform != "win32":
            self.assertEqual(exported.stat().st_mode & 0o777, 0o600)
            self.assertEqual(self.path.stat().st_mode & 0o777, 0o600)
        self.assertEqual(exported.read_bytes(), render(self.record, "invoice").encode())
        self.assertEqual(ledger.digest(exported.read_bytes()), first["receipt"]["artifact_sha256"])

    def test_export_retry_and_failed_export_recovery(self):
        first = self.prepare()
        unavailable = self.directory / "missing-parent" / "invoice.md"
        with self.assertRaises(OSError):
            ledger.export(self.path, self.agency, first["revision_id"], first["receipt_sha256"], unavailable)
        self.assertEqual(self.prepare()["revision_id"], first["revision_id"])
        out = self.artifact(first)
        self.artifact(first)
        out.write_bytes(b"Other content, retain it")
        with self.assertRaisesRegex(ledger.LedgerError, "different content"):
            self.artifact(first)
        self.assertEqual(out.read_bytes(), b"Other content, retain it")
        self.assertEqual(self.artifact(first, "recovered.md").read_bytes(), render(self.record, "invoice").encode())

    def test_superseded_revision_cannot_be_exported_as_current(self):
        first = self.prepare()
        self.record["invoice"]["payment_terms"] = "Changed fictional terms"
        self.prepare()
        with self.assertRaisesRegex(ledger.LedgerError, "superseded"):
            self.artifact(first)

    def test_agency_boundary_and_database_version(self):
        with self.assertRaisesRegex(ledger.LedgerError, "agency"):
            ledger.prepare(self.path, "OTHER-AGENCY", self.event["event_id"], self.record)
        with self.assertRaisesRegex(ledger.LedgerError, "agency"):
            ledger.initialize(self.path, "OTHER-AGENCY")
        with sqlite3.connect(self.path) as db:
            db.execute("PRAGMA user_version=99")
        with self.assertRaisesRegex(ledger.LedgerError, "version"):
            ledger.status(self.path, self.agency)

    def test_unknown_and_malformed_engagement_fields_fail_closed(self):
        cases = [dict(self.record, approved_by="FORGED"), dict(self.record, invoice=[]), dict(self.record, demo_only="yes")]
        for section, name, value in [("invoice", "unknown", "hidden"), ("client", "billing_email", []), ("offer", "subtotal", "Infinity"), ("invoice", "line_items", [None]), ("kickoff", "decision_makers", "person"), ("recruiting", "pipeline_counts", {"hidden": 1})]:
            changed = copy.deepcopy(self.record)
            changed[section][name] = value
            cases.append(changed)
        changed = copy.deepcopy(self.record)
        changed["approvals"]["invoice"]["authenticated"] = True
        cases.append(changed)
        for changed in cases:
            with self.subTest(record=changed), self.assertRaises(ValueError):
                self.prepare(changed)
        self.assertEqual(ledger.status(self.path, self.agency)["revisions"], [])

    def test_concurrent_identical_prepare_creates_one_revision(self):
        with ThreadPoolExecutor(max_workers=6) as pool:
            results = list(pool.map(lambda _: self.prepare(), range(12)))
        self.assertEqual(len({r["revision_id"] for r in results}), 1)
        self.assertEqual(sum(r["created"] for r in results), 1)
        self.assertEqual(len(ledger.status(self.path, self.agency)["revisions"]), 1)

    def test_concurrent_different_events_cannot_share_invoice_number(self):
        other = dict(self.event, event_id="EVENT-OTHER")
        ledger.record_event(self.path, self.agency, other, self.source)
        def attempt(event_id):
            try:
                return self.prepare(event_id=event_id)
            except ledger.LedgerError:
                return None
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(attempt, [self.event["event_id"], other["event_id"]]))
        self.assertEqual(sum(r is not None for r in results), 1)
        self.assertEqual(len(ledger.status(self.path, self.agency)["revisions"]), 1)

    def test_json_duplicate_keys_nonfinite_and_exact_decimal(self):
        for text in ['{"a":1,"a":2}', '{"nested":{"a":1,"a":2}}', '{"x":NaN}', '{"x":Infinity}', '{"x":1e999999}']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                ledger.decode(text)
        decoded = ledger.decode('{"amount":0.1234567890123456789012345678}')
        self.assertEqual(decoded["amount"], Decimal("0.1234567890123456789012345678"))

    def test_cli_malformed_input_never_creates_database(self):
        destination = self.directory / "must-not-exist.sqlite3"
        record = self.directory / "bad.json"
        for text in ['{"a":1,"a":2}', '{"x":NaN}', '[]', '{"schema_version":"billing-event/v9"}']:
            record.write_text(text, encoding="utf-8")
            for command in [["prepare", "--record", str(record), "--event-id", "EVENT"], ["record-event", "--event", str(record), "--source", str(self.source)]]:
                result = subprocess.run([sys.executable, str(SCRIPT), *command, "--ledger", str(destination), "--agency", self.agency], capture_output=True, text=True)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertFalse(destination.exists())
        result = subprocess.run([sys.executable, str(SCRIPT), "init", "--ledger", str(destination), "--agency", "bad agency"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertFalse(destination.exists())

    def test_cli_end_to_end_explicit_review_and_check(self):
        record_file = self.directory / "engagement.json"
        record_file.write_text(ledger.canonical(self.record), encoding="utf-8")
        def cli(*args):
            result = subprocess.run([sys.executable, str(SCRIPT), *args, "--ledger", str(self.path), "--agency", self.agency], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            return json.loads(result.stdout)
        prepared = cli("prepare", "--event-id", self.event["event_id"], "--record", str(record_file))
        common = ["--revision", prepared["revision_id"], "--receipt", prepared["receipt_sha256"]]
        out = self.directory / "cli.md"
        cli("export", *common, "--out", str(out))
        inputs = [*common, "--record", str(record_file), "--artifact", str(out)]
        reviewed = cli("review", *inputs, "--reviewer", "REVIEWER-DEMO", "--review-reference", "REVIEW-DEMO")
        self.assertEqual(reviewed["state"], "LOCAL_REVIEW_ACKNOWLEDGED")
        self.assertFalse(cli("check", *inputs)["external_send_allowed"])


if __name__ == "__main__":
    unittest.main()
