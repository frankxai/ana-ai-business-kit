#!/usr/bin/env python3
"""Render human-review Markdown drafts from one validated engagement record."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from string import Template

from validate_engagement import validate


DOCUMENT_STAGES = {
    "job-description": "job-description",
    "offer": "offer",
    "invoice": "invoice",
}


def bullets(values) -> str:
    return "\n".join(f"- {value}" for value in values) if values else "- [Complete before approval]"


def line_items(values, currency: str) -> str:
    rows = ["| Description | Quantity | Unit price | Amount |", "| --- | ---: | ---: | ---: |"]
    for item in values:
        rows.append(
            f"| {item['description']} | {item['quantity']} | {currency} {item['unit_price']:.2f} | {currency} {item['amount']:.2f} |"
        )
    return "\n".join(rows)


def context(record: dict) -> dict[str, str]:
    client = record["client"]
    kickoff = record["kickoff"]
    role = record.get("role", {})
    offer = record.get("offer", {})
    invoice = record.get("invoice", {})
    return {
        "engagement_id": record["engagement_id"],
        "client_name": client["legal_name"],
        "contact_name": client["contact_name"],
        "billing_name": client.get("billing_name", "[Billing name]"),
        "billing_address": client.get("billing_address", "[Billing address]"),
        "billing_email": client.get("billing_email", "[Billing email]"),
        "company_context": kickoff["company_context"],
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
        "currency": offer.get("currency", invoice.get("currency", "EUR")),
        "offer_subtotal": f"{offer.get('subtotal', 0):.2f}",
        "offer_tax_rate": f"{offer.get('tax_rate', 0):.2f}",
        "offer_tax_amount": f"{offer.get('tax_amount', 0):.2f}",
        "offer_total": f"{offer.get('total', 0):.2f}",
        "payment_terms": offer.get("payment_terms", invoice.get("payment_terms", "[Payment terms]")),
        "valid_until": offer.get("valid_until", "[Validity date]"),
        "invoice_number": invoice.get("invoice_number", "[Invoice number]"),
        "issue_date": invoice.get("issue_date", "[Issue date]"),
        "due_date": invoice.get("due_date", "[Due date]"),
        "invoice_items": line_items(invoice.get("line_items", []), invoice.get("currency", "EUR")),
        "invoice_subtotal": f"{invoice.get('subtotal', 0):.2f}",
        "invoice_tax_rate": f"{invoice.get('tax_rate', 0):.2f}",
        "invoice_tax_amount": f"{invoice.get('tax_amount', 0):.2f}",
        "invoice_total": f"{invoice.get('total', 0):.2f}",
        "payment_details_reference": invoice.get("payment_details_reference", "[Approved finance-system reference]"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    parser.add_argument("--document", choices=DOCUMENT_STAGES, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    record = json.loads(args.record.read_text(encoding="utf-8"))
    errors = validate(record, DOCUMENT_STAGES[args.document])
    if errors:
        raise SystemExit("Cannot render:\n- " + "\n- ".join(errors))

    asset = Path(__file__).resolve().parent.parent / "assets" / f"{args.document}.md"
    rendered = Template(asset.read_text(encoding="utf-8")).safe_substitute(context(record))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(rendered, encoding="utf-8")
    print(f"Rendered review draft: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
