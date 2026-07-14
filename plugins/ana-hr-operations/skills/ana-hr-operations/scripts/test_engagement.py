#!/usr/bin/env python3
"""Dependency-free tests for the engagement gates and render templates."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from string import Template

from render_documents import DOCUMENT_ASSETS, context
from validate_engagement import STAGE_CHAIN, validate


ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = json.loads((ROOT / "assets" / "engagement.example.json").read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


for stage in STAGE_CHAIN:
    require(not validate(EXAMPLE, stage), f"Example should pass {stage}.")

require(validate(EXAMPLE, "offer", require_template=True), "Placeholder template URL must fail the live-template gate.")

bad_total = copy.deepcopy(EXAMPLE)
bad_total["offer"]["total"] = 9999
require(any("offer.total" in error for error in validate(bad_total, "offer")), "Incorrect offer total must fail.")

missing_send = copy.deepcopy(EXAMPLE)
missing_send["approvals"].pop("send")
require(any("approvals.send" in error for error in validate(missing_send, "send")), "Missing send approval must fail.")

job_description_send = copy.deepcopy(EXAMPLE)
job_description_send["handoff"] = {
    "artifact_type": "job-description",
    "artifact_reference": "PRIVATE-JD-DEMO-001",
    "artifact_revision": "rev-2",
}
job_description_send.pop("offer")
job_description_send.pop("invoice")
for approval in ["price", "offer", "invoice"]:
    job_description_send["approvals"].pop(approval)
require(not validate(job_description_send, "send"), "A job-description handoff must not require the invoice path.")

bad_handoff_type = copy.deepcopy(EXAMPLE)
bad_handoff_type["handoff"]["artifact_type"] = "unknown"
require(any("handoff.artifact_type" in error for error in validate(bad_handoff_type, "send")), "Unknown handoff artifact type must fail.")

currency_mismatch = copy.deepcopy(EXAMPLE)
currency_mismatch["invoice"]["currency"] = "USD"
require(any("currency" in error.lower() for error in validate(currency_mismatch, "invoice")), "Currency mismatch must fail.")

missing_admin = copy.deepcopy(EXAMPLE)
missing_admin["administration"].pop("next_owner")
require(any("administration.next_owner" in error for error in validate(missing_admin, "first-call")), "Missing multi-client owner must fail.")

sensitive_candidate = copy.deepcopy(EXAMPLE)
sensitive_candidate["recruiting"]["candidate_email"] = "person@example.invalid"
require(any("Forbidden sensitive field" in error for error in validate(sensitive_candidate, "recruiting")), "Candidate PII in the engagement record must fail.")

missing_team_owner = copy.deepcopy(EXAMPLE)
missing_team_owner["team"].pop("manager_approver")
require(any("team.manager_approver" in error for error in validate(missing_team_owner, "first-call")), "Missing team manager must fail.")

wrong_template_state = copy.deepcopy(EXAMPLE)
wrong_template_state["template"]["document_routes"]["offer"]["platform"] = "google-docs"
require(any("CANVA_RENDER_PENDING" in error for error in validate(wrong_template_state, "offer")), "Canva state must match Canva platform.")

bad_line_amount = copy.deepcopy(EXAMPLE)
bad_line_amount["invoice"]["line_items"][0]["amount"] = 999.0
require(any("quantity × unit_price" in error for error in validate(bad_line_amount, "invoice")), "Incorrect invoice line arithmetic must fail.")

bad_due_date = copy.deepcopy(EXAMPLE)
bad_due_date["invoice"]["due_date"] = "2026-07-01"
require(any("due_date" in error for error in validate(bad_due_date, "invoice")), "An invoice due before issue date must fail.")

bad_pipeline_count = copy.deepcopy(EXAMPLE)
bad_pipeline_count["recruiting"]["pipeline_counts"]["screened"] = -1
require(any("non-negative integer" in error for error in validate(bad_pipeline_count, "recruiting")), "Invalid aggregate pipeline counts must fail.")

null_privacy = copy.deepcopy(EXAMPLE)
null_privacy["privacy"] = None
null_privacy_context = context(null_privacy)
require(
    null_privacy_context["client_system"] == "[Approved client system]",
    "Null privacy must render safe placeholders without crashing.",
)

render_context = context(EXAMPLE)
for document in ["kickoff", "job-description", "offer", "invoice"]:
    template = Template((ROOT / "assets" / DOCUMENT_ASSETS[document]).read_text(encoding="utf-8"))
    rendered = template.safe_substitute(render_context)
    require("${" not in rendered, f"{document} has unresolved placeholders.")
    require("DRAFT" in rendered, f"{document} must remain visibly draft-labeled.")

print("Ana HR engagement, recruiting, privacy, and money gate tests passed.")
