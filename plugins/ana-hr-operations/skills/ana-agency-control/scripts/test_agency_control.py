"""Behavioral checks for the private-reference-only planning boundary."""

from copy import deepcopy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from agency_control import ContractError, build_plan, render_markdown, validate


HERE = Path(__file__).resolve().parent
EXAMPLE = HERE.parent / "assets" / "agency-control.example.json"


class AgencyControlTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def task(self, key="refresh-policy", record=None):
        return next(task for task in (record or self.record)["tasks"] if task["task_id"] == key)

    def source(self, key="policy", record=None):
        return next(source for source in (record or self.record)["sources"] if source["source_id"] == key)

    def result(self, key="refresh-policy", record=None):
        return next(task for task in build_plan(record or self.record)["tasks"] if task["task_id"] == key)

    def meeting(self, key="status-sync", record=None):
        return next(meeting for meeting in (record or self.record)["meetings"] if meeting["meeting_id"] == key)

    def meeting_result(self, key="status-sync", record=None):
        return next(meeting for meeting in build_plan(record or self.record)["meetings"] if meeting["meeting_id"] == key)

    def cli(self, record_text, *arguments):
        with tempfile.TemporaryDirectory() as directory:
            record = Path(directory) / "input.json"
            output = Path(directory) / "draft.md"
            record.write_text(record_text, encoding="utf-8")
            process = subprocess.run([sys.executable, str(HERE / "agency_control.py"), "plan", str(record),
                                      "--out", str(output), *arguments], text=True, capture_output=True)
            return process, output.read_text(encoding="utf-8") if output.exists() else None

    def test_complete_fictional_example_is_proposed_work_only(self):
        plan = build_plan(self.record)
        self.assertFalse(plan["authenticated"])
        self.assertFalse(plan["external_actions_allowed"])
        self.assertEqual(plan["source_access_basis"], "OPERATOR_DECLARATION_NOT_ACCESS_ENFORCEMENT")
        self.assertEqual({group["proposed_specialist"] for group in plan["dispatch_groups"]},
                         {"commercial", "finance", "knowledge-curator", "meeting-coordinator", "talent-operations"})
        self.assertEqual(self.result("intake-closed")["state"], "COMPLETED")
        self.assertEqual(self.result("pipeline-update")["state"], "READY")

    def test_blocked_sources_never_reach_dispatch_cards_or_report(self):
        for kind, agency, access, reason in [
            ("company-policy", "different-agency", "confirmed", "SOURCE_OUTSIDE_AGENCY"),
            ("clinical", "fictional-agency-a", "confirmed", "SOURCE_DOMAIN_FORBIDDEN"),
            ("personal-reflection", "fictional-agency-a", "confirmed", "SOURCE_DOMAIN_FORBIDDEN"),
            ("company-policy", "fictional-agency-a", "unknown", "SOURCE_ACCESS_UNCONFIRMED"),
            ("company-policy", "fictional-agency-a", "revoked", "SOURCE_ACCESS_UNCONFIRMED"),
        ]:
            with self.subTest(kind=kind, agency=agency, access=access):
                record = deepcopy(self.record)
                source = self.source(record=record)
                source.update(kind=kind, agency_alias=agency, access_state=access,
                              engagement_alias="fictional-engagement-a",
                              source_id="sensitive-id", reference="sensitive-reference", version="sensitive-version")
                for task in record["tasks"]:
                    for ref in task["source_refs"]:
                        if ref["source_id"] == "policy":
                            ref.update(source_id="sensitive-id", version="sensitive-version")
                plan = build_plan(record)
                result = self.result(record=record)
                self.assertEqual(result["state"], "BLOCKED")
                self.assertIn(reason, result["blocker_codes"])
                self.assertEqual(result["source_refs"], [])
                serialized = json.dumps(plan) + render_markdown(plan)
                for private_marker in ("sensitive-id", "sensitive-reference", "sensitive-version", "different-agency"):
                    self.assertNotIn(private_marker, serialized)

    def test_stale_future_and_version_mismatch_block_readiness(self):
        for update, reason in [({"review_due": "2026-09-08"}, "SOURCE_REVIEW_OVERDUE"),
                               ({"updated_at": "2026-09-10"}, "SOURCE_FROM_FUTURE"),
                               ({"version": "v2"}, "SOURCE_VERSION_MISMATCH")]:
            with self.subTest(reason=reason):
                record = deepcopy(self.record)
                self.source(record=record).update(update)
                result = self.result(record=record)
                self.assertEqual(result["state"], "BLOCKED")
                self.assertIn(reason, result["blocker_codes"])

    def test_same_agency_wrong_engagement_source_blocks_and_withholds_metadata_and_question(self):
        source = self.source("engagement")
        source.update(engagement_alias="private-other-engagement", source_id="private-source-id",
                      reference="private-reference", version="private-version")
        for task in self.record["tasks"]:
            for ref in task["source_refs"]:
                if ref["source_id"] == "engagement":
                    ref.update(source_id="private-source-id", version="private-version")
        self.task("employment-review")["decision_question"] = "Confidential fictional question must be withheld"
        result = self.result("employment-review")
        self.assertEqual(result["state"], "BLOCKED")
        self.assertIn("SOURCE_OUTSIDE_ENGAGEMENT", result["blocker_codes"])
        self.assertEqual(result["source_refs"], [])
        plan = build_plan(self.record)
        serialized = json.dumps(plan) + render_markdown(plan)
        for marker in ("private-other-engagement", "private-source-id", "private-reference", "private-version",
                       "Confidential fictional question must be withheld"):
            self.assertNotIn(marker, serialized)

    def test_agency_wide_policy_catalog_and_talent_pool_permit_matching_engagement_work(self):
        for key in ("policy", "catalog", "talent-index"):
            self.assertEqual(self.source(key)["engagement_alias"], "agency-wide")
        for key in ("refresh-policy", "service-proposal", "employment-review", "pipeline-update"):
            self.assertEqual(self.result(key)["state"], "READY")
        self.source("talent-index")["engagement_alias"] = "fictional-other-engagement"
        self.assertEqual(self.result("employment-review")["state"], "BLOCKED")

    def test_specific_sources_cannot_claim_agency_wide_scope_and_scope_is_required(self):
        for kind in ("engagement", "meeting-note", "clinical", "personal-reflection"):
            record = deepcopy(self.record)
            self.source("engagement", record).update(kind=kind, engagement_alias="agency-wide")
            with self.assertRaises(ContractError):
                validate(record)
        del self.source()["engagement_alias"]
        with self.assertRaises(ContractError):
            validate(self.record)

    def test_forbidden_domains_remain_blocked_for_matching_and_different_engagements(self):
        for kind in ("clinical", "personal-reflection"):
            for scope in ("fictional-engagement-a", "fictional-other-engagement"):
                record = deepcopy(self.record)
                self.source(record=record).update(kind=kind, engagement_alias=scope)
                result = self.result(record=record)
                self.assertEqual(result["state"], "BLOCKED")
                self.assertIn("SOURCE_DOMAIN_FORBIDDEN", result["blocker_codes"])
                self.assertEqual(result["source_refs"], [])

    def test_current_day_source_is_valid_and_deadlines_are_explicit(self):
        self.source().update(updated_at="2026-09-09", review_due="2026-09-09")
        self.assertEqual(self.result()["state"], "READY")
        for due, expected in [("2026-09-08", "overdue"), ("2026-09-09", "due_today"), ("2026-09-10", "upcoming")]:
            self.task()["due_date"] = due
            self.assertEqual(self.result()["deadline_state"], expected)

    def test_pending_dependency_waits_and_completed_dependency_permits_work(self):
        self.assertEqual(self.result("candidate-followup")["state"], "WAITING_ON_DEPENDENCY")
        self.task("pipeline-update")["status"] = "completed"
        self.assertEqual(self.result("candidate-followup")["state"], "READY")
        self.source("talent-index")["access_state"] = "revoked"
        # A historical completed label does not permit reuse of a now-revoked source.
        self.assertEqual(self.result("pipeline-update")["state"], "BLOCKED")
        self.assertEqual(self.result("candidate-followup")["state"], "BLOCKED")

    def test_blocked_completed_dependency_does_not_unlock_clean_downstream_task(self):
        self.task()["depends_on"] = ["expired-source"]
        self.task("expired-source")["status"] = "completed"
        self.assertEqual(self.result()["state"], "WAITING_ON_DEPENDENCY")

    def test_cycles_and_unknown_dependency_ids_are_rejected(self):
        for dependency in ("refresh-policy", "missing-task"):
            with self.subTest(dependency=dependency):
                record = deepcopy(self.record)
                self.task(record=record)["depends_on"] = [dependency]
                with self.assertRaises(ContractError):
                    build_plan(record)
        self.task("intake-closed")["depends_on"] = ["candidate-followup"]
        with self.assertRaises(ContractError):
            build_plan(self.record)

    def test_unknown_source_and_meeting_task_ids_are_rejected(self):
        self.task()["source_refs"][0]["source_id"] = "missing-source"
        with self.assertRaises(ContractError):
            validate(self.record)
        self.setUp()
        self.meeting()["task_ids"] = ["missing-task"]
        with self.assertRaises(ContractError):
            validate(self.record)

    def test_service_and_employment_offers_have_distinct_human_decision_owners(self):
        cards = {card["task_id"]: card for card in build_plan(self.record)["decision_cards"]}
        self.assertEqual(cards["service-proposal"]["proposed_decision_owner_role"], "agency-owner")
        self.assertEqual(cards["employment-review"]["proposed_decision_owner_role"], "client-decision-owner")
        self.assertEqual(cards["employment-review"]["decision_state"], "DRAFT_QUESTION_PREPARATION_REQUIRED")
        self.assertEqual(self.result("employment-review")["proposed_human_owner_role"], "talent-operator")
        for key in ("service-proposal", "invoice-review", "client-handoff"):
            self.assertEqual(self.result(key)["proposed_human_owner_role"], "document-operator")
        self.task("employment-review")["decision_question"] = "  "
        with self.assertRaises(ContractError):
            validate(self.record)

    def test_handoffs_are_bounded_versioned_and_require_host_access_checks(self):
        for index in range(8):
            task = deepcopy(self.task())
            task["task_id"] = f"extra-task-{index}"
            self.record["tasks"].append(task)
        groups = build_plan(self.record)["dispatch_groups"]
        self.assertTrue(all(1 <= len(group["task_ids"]) <= 3 for group in groups))
        for group in groups:
            self.assertEqual(group["execution_state"], "PROPOSED_ONLY")
            for packet in group["handoff_packets"]:
                self.assertEqual(packet["allowed_actions"], ["read_source", "draft_artifact"])
                self.assertEqual(packet["source_read_authorization"], "HOST_MUST_VERIFY_ACCESS_BEFORE_ANY_READ")
                self.assertEqual(packet["agency_alias"], "fictional-agency-a")
                task = self.task(packet["task_id"])
                self.assertEqual(packet["due_date"], task["due_date"])
                self.assertEqual(packet["depends_on"], task["depends_on"])
                self.assertTrue(packet["requested_outcome"])
                self.assertTrue(all(set(ref) == {"source_id", "version"} for ref in packet["source_refs"]))
                contract = packet["return_contract"]
                self.assertEqual(contract["status_values"], ["draft_ready", "blocked", "failed"])
                self.assertEqual(set(contract["required_fields"]),
                                 {"task_id", "agency_alias", "engagement_alias", "status", "source_versions",
                                  "artifact_ref", "artifact_digest", "unresolved_facts", "requested_human_decision",
                                  "execution_receipt", "measured_duration_seconds", "measured_cost"})
                self.assertNotIn("execution_receipt", packet)
                self.assertIn("null when unknown", contract["field_rules"]["measured_cost"])

    def test_every_protected_meeting_purpose_remains_live_even_with_broken_pre_read(self):
        for purpose in ("interview", "relationship", "workshop", "conflict", "care"):
            with self.subTest(purpose=purpose):
                self.meeting().update(purpose=purpose, task_ids=["expired-source"])
                result = self.meeting_result()
                self.assertEqual(result["recommendation"], "KEEP_LIVE")
                self.assertEqual(result["pre_read_state"], "REPAIR_REQUIRED")
                self.assertEqual(result["modeled_meeting_minutes"], 0)

    def test_explicit_live_requirement_wins_over_async_readiness(self):
        self.meeting()["requires_live"] = True
        self.assertEqual(self.meeting_result()["recommendation"], "KEEP_LIVE")

    def test_waiting_or_blocked_work_requires_repaired_pre_read(self):
        for key in ("client-handoff", "expired-source", "other-agency-task"):
            with self.subTest(task=key):
                self.meeting()["task_ids"] = [key]
                result = self.meeting_result()
                self.assertEqual(result["recommendation"], "REPAIR_PRE_READ")
                self.assertEqual(result["modeled_person_minutes"], 0)

    def test_completed_current_work_permits_async_pre_read_without_unresolved_dependency(self):
        self.meeting()["task_ids"] = ["intake-closed"]
        self.assertEqual(self.meeting_result()["recommendation"], "ASYNC_CANDIDATE")
        self.task("intake-closed")["depends_on"] = ["refresh-policy"]
        self.assertEqual(self.meeting_result()["recommendation"], "REPAIR_PRE_READ")
        self.task("intake-closed")["depends_on"] = []
        self.source()["review_due"] = "2026-09-08"
        self.assertEqual(self.meeting_result()["recommendation"], "REPAIR_PRE_READ")

    def test_fresh_irrelevant_sources_do_not_unlock_work_or_leak_references(self):
        for key in ("pipeline-update", "candidate-followup", "employment-review", "service-proposal",
                    "invoice-review", "client-handoff", "status-brief", "scope-decision"):
            with self.subTest(task=key):
                record = deepcopy(self.record)
                self.task(key, record)["source_refs"] = [{"source_id": "policy", "version": "v1"}]
                result = self.result(key, record)
                self.assertEqual(result["state"], "BLOCKED")
                self.assertIn("MISSING_REQUIRED_SOURCE_DOMAIN", result["blocker_codes"])
                self.assertEqual(result["source_refs"], [])

    def test_one_bad_task_prevents_whole_meeting_becoming_async_candidate(self):
        self.meeting()["task_ids"].append("expired-source")
        self.assertEqual(self.meeting_result()["recommendation"], "REPAIR_PRE_READ")

    def test_planning_does_not_verify_decision_or_meeting_artifacts(self):
        plan = build_plan(self.record)
        self.assertTrue(plan["decision_cards"])
        for card in plan["decision_cards"]:
            self.assertFalse(card["reviewable_artifact_verified"])
            self.assertEqual(card["decision_state"], "DRAFT_QUESTION_PREPARATION_REQUIRED")
        candidates = [meeting for meeting in plan["meetings"] if meeting["recommendation"].startswith("ASYNC_")]
        self.assertTrue(candidates)
        for meeting in candidates:
            self.assertEqual(meeting["pre_read_state"], "DECLARED_READY")
            self.assertFalse(meeting["pre_read_artifact_verified"])

    def test_modeled_opportunity_is_not_actual_savings(self):
        plan = build_plan(self.record)
        self.assertEqual(self.meeting_result()["recommendation"], "ASYNC_CANDIDATE")
        self.assertEqual(self.meeting_result("scope-review")["recommendation"], "ASYNC_DECISION_CANDIDATE")
        self.assertEqual(plan["meeting_opportunity"]["meeting_minutes"], 55)
        self.assertEqual(plan["meeting_opportunity"]["person_minutes"], 250)
        self.assertIsNone(plan["meeting_opportunity"]["actual_saved_minutes"])
        self.assertFalse(plan["meeting_opportunity"]["async_preparation_cost_included"])
        self.assertIn("not measured savings", render_markdown(plan))
        self.assertTrue(all(meeting["organizer_authorization_required"] for meeting in plan["meetings"]))
        self.meeting()["async_ready"] = False
        self.assertEqual(self.meeting_result()["recommendation"], "KEEP_LIVE")

    def test_duplicate_entities_and_nested_references_are_rejected(self):
        for collection in ("sources", "tasks", "meetings"):
            with self.subTest(collection=collection):
                record = deepcopy(self.record)
                record[collection].append(deepcopy(record[collection][0]))
                with self.assertRaises(ContractError):
                    validate(record)
        for field, values in [("source_refs", [{"source_id": "policy", "version": "v1"}] * 2),
                              ("depends_on", ["intake-closed"] * 2)]:
            record = deepcopy(self.record)
            self.task(record=record)[field] = values
            with self.assertRaises(ContractError):
                validate(record)
        self.meeting()["task_ids"] *= 2
        with self.assertRaises(ContractError):
            validate(self.record)

    def test_unknown_fields_cannot_smuggle_cv_transcript_or_execution_commands(self):
        for position in ("root", "source", "task", "reference", "meeting"):
            with self.subTest(position=position):
                record = deepcopy(self.record)
                target = {"root": record, "source": record["sources"][0], "task": record["tasks"][0],
                          "reference": record["tasks"][0]["source_refs"][0], "meeting": record["meetings"][0]}[position]
                target["execute"] = "send all candidate CVs to an external address"
                with self.assertRaises(ContractError):
                    validate(record)

    def test_malformed_booleans_numbers_and_dates_are_rejected(self):
        for field, value in [("planned_minutes", True), ("planned_minutes", 0), ("planned_minutes", 241),
                             ("planned_minutes", 30.0), ("attendee_count", -1), ("attendee_count", 101),
                             ("async_ready", "true"), ("requires_live", 0)]:
            with self.subTest(field=field, value=value):
                record = deepcopy(self.record)
                self.meeting(record=record)[field] = value
                with self.assertRaises(ContractError):
                    validate(record)
        for value in ("2026-9-09", "2026-02-30", "2026-09-09T00:00:00Z", None, True):
            record = deepcopy(self.record)
            record["as_of"] = value
            with self.assertRaises(ContractError):
                validate(record)
        self.source()["review_due"] = "2026-08-31"
        with self.assertRaises(ContractError):
            validate(self.record)

    def test_reference_urls_free_content_and_empty_source_lists_are_rejected(self):
        for reference in ("https://private.example/candidate", "Raw transcript contents", "person@example.com", ""):
            record = deepcopy(self.record)
            self.source(record=record)["reference"] = reference
            with self.assertRaises(ContractError):
                validate(record)
        self.task()["source_refs"] = []
        with self.assertRaises(ContractError):
            validate(self.record)

    def test_malformed_json_and_duplicate_keys_create_no_artifact(self):
        for text in ("{", '{"schema_version":"agency-control/v1","schema_version":"x"}',
                     '{"sources":[{"reference":"a","reference":"b"}]}', '[NaN]', 'null',
                     json.dumps(self.record).replace('"planned_minutes": 30', '"planned_minutes": Infinity', 1)):
            with self.subTest(text=text[:40]):
                process, output = self.cli(text)
                self.assertEqual(process.returncode, 2)
                self.assertIsNone(output)
                self.assertNotIn("Traceback", process.stderr)

    def test_valid_cli_output_is_deterministic_and_refuses_differing_overwrite(self):
        process, output = self.cli(json.dumps(self.record))
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(output, render_markdown(build_plan(self.record)))
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "draft.md"
            output.write_text("existing human work", encoding="utf-8")
            args = [sys.executable, str(HERE / "agency_control.py"), "plan", str(EXAMPLE), "--out", str(output)]
            process = subprocess.run(args, text=True, capture_output=True)
            self.assertEqual(process.returncode, 2)
            self.assertEqual(output.read_text(encoding="utf-8"), "existing human work")
            output.write_text(render_markdown(build_plan(self.record)), encoding="utf-8")
            self.assertEqual(subprocess.run(args, capture_output=True).returncode, 0)

    def test_markdown_does_not_render_raw_html_from_decision_question(self):
        self.task("service-proposal")["decision_question"] = '<script>alert("fictional")</script> | `text`'
        draft = render_markdown(build_plan(self.record))
        self.assertNotIn("<script>", draft)
        self.assertIn("&lt;script&gt;", draft)

    def test_unicode_controls_and_large_invalid_numbers_fail_without_output(self):
        for value in ("line\u2028break", "surrogate\ud800", "hidden\u202efact"):
            record = deepcopy(self.record)
            self.task("service-proposal", record)["decision_question"] = value
            process, output = self.cli(json.dumps(record))
            self.assertEqual(process.returncode, 2)
            self.assertIsNone(output)
        process, output = self.cli('{"value":' + '9' * 5000 + '}')
        self.assertEqual(process.returncode, 2)
        self.assertIsNone(output)
        self.assertNotIn("Traceback", process.stderr)

    @unittest.skipUnless(os.name == "posix", "POSIX file permissions")
    def test_new_draft_uses_owner_only_permissions(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "draft.md"
            process = subprocess.run([sys.executable, str(HERE / "agency_control.py"), "plan", str(EXAMPLE),
                                      "--out", str(output)], text=True, capture_output=True)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual(output.stat().st_mode & 0o777, 0o600)


if __name__ == "__main__":
    unittest.main()
