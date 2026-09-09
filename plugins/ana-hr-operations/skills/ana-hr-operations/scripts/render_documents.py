#!/usr/bin/env python3
"""Render human-review Markdown drafts from one validated engagement record."""

from __future__ import annotations

import argparse
import json
from decimal import Decimal
from pathlib import Path
from string import Template

from validate_engagement import object_block, round_money, validate


DOCUMENT_STAGES = {
    "kickoff": "kickoff",
    "job-description": "job-description",
    "offer": "offer",
    "invoice": "invoice",
}
DOCUMENT_ASSETS = {
    "kickoff": "client-kickoff.md",
    "job-description": "job-description.md",
    "offer": "offer.md",
    "invoice": "invoice.md",
}


def bullets(values) -> str:
    return "\n".join(f"- {value}" for value in values) if values else "- [Complete before approval]"


def decimal_text(value) -> str:
    text = format(Decimal(str(value)), "f")
    return text.rstrip("0").rstrip(".") if "." in text else text


def amount_text(value) -> str:
    return format(round_money(Decimal(str(value))), ".2f")


def line_items(values, currency: str) -> str:
    rows = ["| Description | Quantity | Unit price | Amount |", "| --- | ---: | ---: | ---: |"]
    for item in values:
        rows.append(
            f"| {item['description']} | {decimal_text(item['quantity'])} | {currency} {amount_text(item['unit_price'])} | {currency} {amount_text(item['amount'])} |"
        )
    return "\n".join(rows)


def context(record: dict, document: str | None = None) -> dict[str, str]:
    client = record["client"]
    kickoff = record["kickoff"]
    privacy = record.get("privacy") or {}
    role = object_block(record, "role")
    offer = object_block(record, "offer") if document in {None, "offer", "invoice"} else {}
    invoice = object_block(record, "invoice") if document in {None, "invoice"} else {}
    commercial = invoice if document == "invoice" else offer
    return {
        "engagement_id": record["engagement_id"],
        "client_name": client["legal_name"],
        "contact_name": client["contact_name"],
        "billing_name": client.get("billing_name", "[Billing name]"),
        "billing_address": client.get("billing_address", "[Billing address]"),
        "billing_email": client.get("billing_email", "[Billing email]"),
        "company_context": kickoff["company_context"],
        "hiring_need": kickoff.get("hiring_need", "[Hiring need]"),
        "kickoff_scope": kickoff.get("scope", "[Scope]"),
        "kickoff_timeline": kickoff.get("timeline", "[Timeline]"),
        "kickoff_outcomes": bullets(kickoff.get("success_outcomes", [])),
        "decision_makers": bullets(kickoff.get("decision_makers", [])),
        "communication_cadence": kickoff.get("communication_cadence", "[Communication cadence]"),
        "selection_process": kickoff.get("selection_process", "[Selection process]"),
        "client_system": privacy.get("client_system", "[Approved client system]"),
        "candidate_system": privacy.get("candidate_system", "[Approved candidate system]"),
        "retention_owner": privacy.get("retention_owner", "[Retention owner]"),
        "deletion_rule": privacy.get("deletion_rule", "[Deletion rule]"),
        "role_title": role.get("title", "[Role title]"),
        "location": role.get("location", "[Location]"),
        "employment_type": role.get("employment_type", "[Employment type]"),
        "reporting_to": role.get("reporting_to", "[Reporting line]"),
        "mission": role.get("mission", "[Mission]"),
        "outcomes": bullets(role.get("outcomes", [])),
        "responsibilities": bullets(role.get("responsibilities", [])),
        "must_have": bullets(role.get("must_have", [])),
        "nice_to_have": bullets(role.get("nice_to_have", [])),
        "compensation": role.get("compensation", "[Approved compensation range]"),
        "recruitment_process": role.get("recruitment_process", "[Recruitment process]"),
        "service_name": offer.get("service_name", "[Service]"),
        "deliverables": bullets(offer.get("deliverables", [])),
        "exclusions": bullets(offer.get("exclusions", [])),
        "offer_timeline": offer.get("timeline", "[Timeline]"),
        "currency": commercial.get("currency", "[Currency]"),
        "offer_subtotal": amount_text(offer.get("subtotal", 0)),
        "offer_tax_rate": decimal_text(offer.get("tax_rate", 0)),
        "offer_tax_amount": amount_text(offer.get("tax_amount", 0)),
        "offer_total": amount_text(offer.get("total", 0)),
        "payment_terms": commercial.get("payment_terms", "[Payment terms]"),
        "valid_until": offer.get("valid_until", "[Validity date]"),
        "invoice_number": invoice.get("invoice_number", "[Invoice number]"),
        "issue_date": invoice.get("issue_date", "[Issue date]"),
        "due_date": invoice.get("due_date", "[Due date]"),
        "invoice_items": line_items(invoice.get("line_items", []), invoice.get("currency", "EUR")),
        "invoice_subtotal": amount_text(invoice.get("subtotal", 0)),
        "invoice_tax_rate": decimal_text(invoice.get("tax_rate", 0)),
        "invoice_tax_amount": amount_text(invoice.get("tax_amount", 0)),
        "invoice_total": amount_text(invoice.get("total", 0)),
        "payment_details_reference": invoice.get("payment_details_reference", "[Approved finance-system reference]"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    parser.add_argument("--document", choices=DOCUMENT_STAGES, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    try:
        record = json.loads(args.record.read_text(encoding="utf-8"), parse_float=Decimal)
    except (OSError, ValueError) as exc:
        raise SystemExit(f"Cannot read engagement record: {exc}") from None
    errors = validate(record, DOCUMENT_STAGES[args.document])
    if errors:
        raise SystemExit("Cannot render:\n- " + "\n- ".join(errors))

    asset = Path(__file__).resolve().parent.parent / "assets" / DOCUMENT_ASSETS[args.document]
    rendered = Template(asset.read_text(encoding="utf-8")).safe_substitute(context(record, args.document))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(rendered, encoding="utf-8")
    print(f"Rendered review draft: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
