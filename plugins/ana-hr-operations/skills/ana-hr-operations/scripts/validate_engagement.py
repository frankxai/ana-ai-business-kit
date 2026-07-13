#!/usr/bin/env python3
"""Validate an Ana HR engagement record without external dependencies."""

from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path


STAGE_FIELDS = {
    "first-call": [
        "engagement_id",
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
        "approvals.job_description.approved_by",
        "approvals.job_description.approved_at",
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
        "approvals.send.approved_by",
        "approvals.send.approved_at",
        "approvals.send.channel",
        "approvals.send.recipient",
    ],
}

STAGE_CHAIN = ["first-call", "kickoff", "job-description", "offer", "invoice", "send"]


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


def validate(record: dict, stage: str, require_template: bool = False) -> list[str]:
    errors: list[str] = []
    target_index = STAGE_CHAIN.index(stage)
    required_stages = STAGE_CHAIN[: target_index + 1]

    # Job description and offer are parallel outputs; an invoice requires the offer path.
    if stage == "job-description":
        required_stages = ["first-call", "kickoff", "job-description"]
    elif stage in {"offer", "invoice", "send"}:
        required_stages = ["first-call", "kickoff", "offer"]
        if stage in {"invoice", "send"}:
            required_stages.append("invoice")
        if stage == "send":
            required_stages.append("send")

    for required_stage in required_stages:
        for dotted in STAGE_FIELDS[required_stage]:
            if not is_present(get_path(record, dotted)):
                errors.append(f"Missing {dotted} for {required_stage}.")

    if require_template:
        url = str(get_path(record, "template.google_doc_url") or "")
        if "docs.google.com/document/d/" not in url or "REPLACE_" in url:
            errors.append("An exact approved Google Docs template URL is required.")

    if stage in {"offer", "invoice", "send"}:
        for section in ["offer"] + (["invoice"] if stage in {"invoice", "send"} else []):
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

    if stage in {"invoice", "send"}:
        items = record.get("invoice", {}).get("line_items", [])
        item_total = sum((money(item.get("amount"), "invoice.line_items[].amount", errors) for item in items), Decimal("0.00"))
        invoice_subtotal = money(record.get("invoice", {}).get("subtotal"), "invoice.subtotal", errors)
        if item_total != invoice_subtotal:
            errors.append(f"Invoice line items must total invoice.subtotal (expected {item_total}).")
        if record.get("invoice", {}).get("currency") != record.get("offer", {}).get("currency"):
            errors.append("Invoice currency must match the approved offer currency.")

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
