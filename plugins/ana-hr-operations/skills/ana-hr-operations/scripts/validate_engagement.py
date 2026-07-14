#!/usr/bin/env python3
"""Validate an Ana HR engagement record without external dependencies."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path


STAGE_FIELDS = {
    "first-call": [
        "engagement_id",
        "administration.client_alias",
        "administration.record_owner",
        "administration.next_action",
        "administration.next_owner",
        "administration.next_due_date",
        "administration.last_reviewed_at",
        "administration.risk_level",
        "client.legal_name",
        "client.contact_name",
        "client.contact_email",
        "kickoff.company_context",
        "kickoff.hiring_need",
        "kickoff.success_outcomes",
        "kickoff.timeline",
    ],
    "kickoff": [
        "kickoff.scope",
        "kickoff.decision_makers",
        "kickoff.communication_cadence",
        "kickoff.selection_process",
        "privacy.client_system",
        "privacy.candidate_system",
        "privacy.retention_owner",
        "privacy.deletion_rule",
        "approvals.kickoff.approved_by",
        "approvals.kickoff.approved_at",
    ],
    "job-description": [
        "role.title",
        "role.location",
        "role.employment_type",
        "role.reporting_to",
        "role.mission",
        "role.outcomes",
        "role.responsibilities",
        "role.must_have",
        "role.recruitment_process",
        "recruiting.scorecard_reference",
        "approvals.job_description.approved_by",
        "approvals.job_description.approved_at",
    ],
    "recruiting": [
        "recruiting.ats_reference",
        "recruiting.requisition_status",
        "recruiting.scorecard_reference",
        "recruiting.structured_process",
        "recruiting.pipeline_counts",
        "recruiting.pipeline_snapshot_at",
        "recruiting.next_client_update",
        "approvals.recruiting_launch.approved_by",
        "approvals.recruiting_launch.approved_at",
    ],
    "offer": [
        "offer.service_name",
        "offer.deliverables",
        "offer.exclusions",
        "offer.timeline",
        "offer.currency",
        "offer.subtotal",
        "offer.tax_rate",
        "offer.tax_amount",
        "offer.total",
        "offer.payment_terms",
        "offer.valid_until",
        "approvals.price.approved_by",
        "approvals.price.approved_at",
        "approvals.offer.approved_by",
        "approvals.offer.approved_at",
    ],
    "invoice": [
        "client.billing_name",
        "client.billing_address",
        "client.billing_email",
        "invoice.invoice_number",
        "invoice.issue_date",
        "invoice.due_date",
        "invoice.currency",
        "invoice.line_items",
        "invoice.subtotal",
        "invoice.tax_rate",
        "invoice.tax_amount",
        "invoice.total",
        "invoice.payment_terms",
        "invoice.payment_details_reference",
        "approvals.invoice.approved_by",
        "approvals.invoice.approved_at",
    ],
    "send": [
        "handoff.artifact_type",
        "handoff.artifact_reference",
        "handoff.artifact_revision",
        "approvals.send.approved_by",
        "approvals.send.approved_at",
        "approvals.send.channel",
        "approvals.send.recipient",
    ],
}

STAGE_CHAIN = ["first-call", "kickoff", "job-description", "offer", "recruiting", "invoice", "send"]
STAGE_DEPENDENCIES = {
    "first-call": ["first-call"],
    "kickoff": ["first-call", "kickoff"],
    "job-description": ["first-call", "kickoff", "job-description"],
    "offer": ["first-call", "kickoff", "offer"],
    "recruiting": ["first-call", "kickoff", "job-description", "recruiting"],
    "invoice": ["first-call", "kickoff", "offer", "invoice"],
    "send": ["first-call", "kickoff", "send"],
}
SEND_DEPENDENCIES = {
    "kickoff": [],
    "job-description": ["job-description"],
    "offer": ["offer"],
    "recruiting-status": ["job-description", "recruiting"],
    "invoice": ["offer", "invoice"],
}
FORBIDDEN_RECORD_KEYS = {
    "candidate",
    "candidates",
    "candidate_name",
    "candidate_email",
    "cv",
    "resume",
    "interview_notes",
    "interview_recording",
    "protected_traits",
    "bank_account",
    "iban",
    "bic",
    "swift",
    "candidate_id",
    "employee_name",
    "employee_email",
    "medical_information",
    "health_data",
    "neurotype",
    "personality_profile",
    "emotion_inference",
}
TEAM_ROLES = {
    "manager_approver",
    "engagement_coordinator",
    "research_recruiting_operator",
    "document_client_experience_operator",
}
TEMPLATE_PLATFORMS = {"google-docs", "canva"}
TEMPLATE_STATUSES = {
    "TEMPLATE_BLOCKED",
    "DRAFT_CONTENT_READY",
    "COPY_CREATED",
    "GOOGLE_DOCS_READBACK_COMPLETE",
    "CANVA_RENDER_PENDING",
    "ANA_CONTENT_APPROVED",
    "READY_FOR_HANDOFF_REVIEW",
}


def get_path(data: dict, dotted: str):
    current = data
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def is_present(value) -> bool:
    return value is not None and value != "" and value != [] and value != {}


def money(value, label: str, errors: list[str]) -> Decimal:
    try:
        return Decimal(str(value)).quantize(Decimal("0.01"))
    except (InvalidOperation, TypeError, ValueError):
        errors.append(f"{label} must be a decimal amount.")
        return Decimal("0.00")


def find_forbidden_keys(value, path: str = "") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else key
            if key.lower() in FORBIDDEN_RECORD_KEYS:
                found.append(child_path)
            found.extend(find_forbidden_keys(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(find_forbidden_keys(child, f"{path}[{index}]"))
    return found


def iso_date(value, label: str, errors: list[str]) -> date | None:
    try:
        return date.fromisoformat(str(value))
    except (TypeError, ValueError):
        errors.append(f"{label} must be an ISO date (YYYY-MM-DD).")
        return None


def validate(record: dict, stage: str, require_template: bool = False) -> list[str]:
    errors: list[str] = []
    required_stages = list(STAGE_DEPENDENCIES[stage])
    if stage == "send":
        artifact_type = str(get_path(record, "handoff.artifact_type") or "")
        if artifact_type not in SEND_DEPENDENCIES:
            errors.append(f"handoff.artifact_type must be one of: {', '.join(SEND_DEPENDENCIES)}.")
        else:
            required_stages[2:2] = SEND_DEPENDENCIES[artifact_type]

    for forbidden_path in find_forbidden_keys(record):
        errors.append(f"Forbidden sensitive field in engagement record: {forbidden_path}.")

    team = record.get("team")
    if team is not None:
        if not isinstance(team, dict):
            errors.append("team must be an object when supplied.")
        else:
            for role in TEAM_ROLES:
                if not is_present(team.get(role)):
                    errors.append(f"Missing team.{role}.")

    routes = get_path(record, "template.document_routes")
    if routes is not None:
        if not isinstance(routes, dict):
            errors.append("template.document_routes must be an object when supplied.")
        else:
            for document_type, route in routes.items():
                if not isinstance(route, dict):
                    errors.append(f"template.document_routes.{document_type} must be an object.")
                    continue
                if not is_present(route.get("template_id")):
                    errors.append(f"template.document_routes.{document_type}.template_id is required.")
                platform = route.get("platform")
                status = route.get("status")
                if platform not in TEMPLATE_PLATFORMS:
                    errors.append(f"template.document_routes.{document_type}.platform must be google-docs or canva.")
                if status not in TEMPLATE_STATUSES:
                    errors.append(f"template.document_routes.{document_type}.status is not a recognized template status.")
                if not isinstance(route.get("visual_check_required"), bool):
                    errors.append(f"template.document_routes.{document_type}.visual_check_required must be boolean.")
                if status == "CANVA_RENDER_PENDING" and platform != "canva":
                    errors.append(f"template.document_routes.{document_type} cannot use CANVA_RENDER_PENDING outside Canva.")
                if status == "GOOGLE_DOCS_READBACK_COMPLETE" and platform != "google-docs":
                    errors.append(f"template.document_routes.{document_type} cannot use GOOGLE_DOCS_READBACK_COMPLETE outside Google Docs.")

    for required_stage in required_stages:
        for dotted in STAGE_FIELDS[required_stage]:
            if not is_present(get_path(record, dotted)):
                errors.append(f"Missing {dotted} for {required_stage}.")

    if require_template:
        url = str(get_path(record, "template.google_doc_url") or "")
        if "docs.google.com/document/d/" not in url or "REPLACE_" in url:
            errors.append("An exact approved Google Docs template URL is required.")

    risk_level = str(get_path(record, "administration.risk_level") or "").upper()
    if risk_level not in {"RED", "AMBER", "GREEN", "PAUSED"}:
        errors.append("administration.risk_level must be RED, AMBER, GREEN, or PAUSED.")

    if stage == "recruiting":
        counts = get_path(record, "recruiting.pipeline_counts") or {}
        if not isinstance(counts, dict) or not counts:
            errors.append("recruiting.pipeline_counts must be a non-empty object of aggregate counts.")
        else:
            for name, count in counts.items():
                if not isinstance(count, int) or isinstance(count, bool) or count < 0:
                    errors.append(f"recruiting.pipeline_counts.{name} must be a non-negative integer.")

    if "offer" in required_stages:
        for section in ["offer"] + (["invoice"] if "invoice" in required_stages else []):
            block = record.get(section, {})
            subtotal = money(block.get("subtotal"), f"{section}.subtotal", errors)
            tax_rate = money(block.get("tax_rate"), f"{section}.tax_rate", errors)
            tax_amount = money(block.get("tax_amount"), f"{section}.tax_amount", errors)
            total = money(block.get("total"), f"{section}.total", errors)
            expected_tax = (subtotal * tax_rate / Decimal("100")).quantize(Decimal("0.01"))
            if tax_amount != expected_tax:
                errors.append(f"{section}.tax_amount must equal subtotal × tax_rate (expected {expected_tax}).")
            if total != subtotal + tax_amount:
                errors.append(f"{section}.total must equal subtotal + tax_amount (expected {subtotal + tax_amount}).")

    if "invoice" in required_stages:
        items = record.get("invoice", {}).get("line_items", [])
        item_total = Decimal("0.00")
        for index, item in enumerate(items):
            quantity = money(item.get("quantity"), f"invoice.line_items[{index}].quantity", errors)
            unit_price = money(item.get("unit_price"), f"invoice.line_items[{index}].unit_price", errors)
            amount = money(item.get("amount"), f"invoice.line_items[{index}].amount", errors)
            expected_amount = (quantity * unit_price).quantize(Decimal("0.01"))
            if amount != expected_amount:
                errors.append(f"invoice.line_items[{index}].amount must equal quantity × unit_price (expected {expected_amount}).")
            item_total += amount
        invoice_subtotal = money(record.get("invoice", {}).get("subtotal"), "invoice.subtotal", errors)
        if item_total != invoice_subtotal:
            errors.append(f"Invoice line items must total invoice.subtotal (expected {item_total}).")
        if record.get("invoice", {}).get("currency") != record.get("offer", {}).get("currency"):
            errors.append("Invoice currency must match the approved offer currency.")
        issue_date = iso_date(record.get("invoice", {}).get("issue_date"), "invoice.issue_date", errors)
        due_date = iso_date(record.get("invoice", {}).get("due_date"), "invoice.due_date", errors)
        if issue_date and due_date and due_date < issue_date:
            errors.append("invoice.due_date must not be before invoice.issue_date.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    parser.add_argument("--stage", choices=STAGE_CHAIN, required=True)
    parser.add_argument("--require-template", action="store_true")
    args = parser.parse_args()

    record = json.loads(args.record.read_text(encoding="utf-8"))
    errors = validate(record, args.stage, args.require_template)
    if errors:
        print("Engagement validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Validated {args.record.name} for stage: {args.stage}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
