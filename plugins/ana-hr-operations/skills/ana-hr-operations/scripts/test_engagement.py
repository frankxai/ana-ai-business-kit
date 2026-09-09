#!/usr/bin/env python3
"""Dependency-free tests for the engagement gates and render templates."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
from decimal import Inexact, Rounded, localcontext, ROUND_DOWN
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

for document in ["kickoff", "job-description", "offer", "invoice"]:
    template = Template((ROOT / "assets" / DOCUMENT_ASSETS[document]).read_text(encoding="utf-8"))
    rendered = template.safe_substitute(context(EXAMPLE, document))
    require("${" not in rendered, f"{document} has unresolved placeholders.")
    require("DRAFT" in rendered, f"{document} must remain visibly draft-labeled.")

# These cases previously accepted invalid arithmetic or raised a traceback.
for section in ["offer", "invoice"]:
    for field in ["subtotal", "tax_rate", "tax_amount", "total"]:
        for value in ["NaN", "sNaN", "Infinity", "-Infinity", float("nan"), -1, True, {}, [], "1e999999"]:
            malformed = copy.deepcopy(EXAMPLE)
            malformed[section][field] = value
            require(any(f"{section}.{field}" in error for error in validate(malformed, "invoice")),
                    f"{section}.{field}={value!r} must fail without crashing.")

for field in ["quantity", "unit_price", "amount"]:
    for value in ["NaN", "Infinity", -1, False, None, {}]:
        malformed = copy.deepcopy(EXAMPLE)
        malformed["invoice"]["line_items"][0][field] = value
        require(any(f"line_items[0].{field}" in error for error in validate(malformed, "invoice")),
                f"Malformed line {field} must fail without crashing.")

for root in [None, [], "record", 42]:
    require(validate(root, "invoice"), "Non-object records must fail without crashing.")
for section in ["offer", "invoice", "client", "kickoff"]:
    for value in [None, [], "block", 42]:
        malformed = copy.deepcopy(EXAMPLE)
        malformed[section] = value
        require(validate(malformed, "invoice"), f"Malformed {section} must fail without crashing.")
for value in [None, {}, "items", 1, [], [None], ["item"], [{}]]:
    malformed = copy.deepcopy(EXAMPLE)
    malformed["invoice"]["line_items"] = value
    require(validate(malformed, "invoice"), "Malformed line collections must fail without crashing.")
for field in ["platform", "status"]:
    malformed = copy.deepcopy(EXAMPLE)
    malformed["template"]["document_routes"]["invoice"][field] = []
    require(validate(malformed, "invoice"), "Unhashable template values must fail without crashing.")

for currency in ["JPY", "KWD", "eur", {}, "INVALID"]:
    unsupported = copy.deepcopy(EXAMPLE)
    unsupported["offer"]["currency"] = currency
    unsupported["invoice"]["currency"] = currency
    require(any("currency" in error for error in validate(unsupported, "invoice")),
            "Unknown or unsupported minor-unit precision must fail.")

extra_cents = copy.deepcopy(EXAMPLE)
extra_cents["invoice"]["line_items"][0]["unit_price"] = "1000.001"
require(any("two decimal places" in error for error in validate(extra_cents, "invoice")),
        "Money input must never be silently rounded.")

fractional = copy.deepcopy(EXAMPLE)
fractional["invoice"]["line_items"] = [
    {"description": "Synthetic fractional service", "quantity": "0.005", "unit_price": "1.00", "amount": "0.01"}
]
for section in ["offer", "invoice"]:
    fractional[section].update(subtotal="0.01", tax_rate="50", tax_amount="0.01", total="0.02")
with localcontext() as ctx:
    ctx.rounding = ROUND_DOWN
    ctx.prec = 6
    ctx.traps[Inexact] = True
    ctx.traps[Rounded] = True
    require(not validate(fractional, "invoice"),
            "Half-cent line and tax results must round half up, independent of caller decimal context.")
require("| 0.005 | EUR 1.00 | EUR 0.01 |" in context(fractional, "invoice")["invoice_items"],
        "Fractional quantities and decimal strings must render exactly.")

precise_rate = copy.deepcopy(EXAMPLE)
for section in ["offer", "invoice"]:
    precise_rate[section].update(tax_rate="0.125", tax_amount="1.25", total="1001.25")
require(not validate(precise_rate, "invoice"), "Rates must retain more than two decimal places.")
require(context(precise_rate, "invoice")["invoice_tax_rate"] == "0.125", "Rendered rate must match arithmetic.")

invoice_terms = copy.deepcopy(EXAMPLE)
invoice_terms["invoice"]["payment_terms"] = "Approved invoice milestone terms"
require(not validate(invoice_terms, "invoice"), "Independently approved invoice terms are supported.")
invoice_context = context(invoice_terms, "invoice")
require(invoice_context["payment_terms"] == "Approved invoice milestone terms", "Invoice must use its own terms.")
require(context(invoice_terms, "offer")["payment_terms"] == EXAMPLE["offer"]["payment_terms"],
        "Offer must retain its own terms.")
# Test selection directly; the separate validation gate still rejects mismatched currencies.
invoice_terms["invoice"]["currency"] = "USD"
require(context(invoice_terms, "invoice")["currency"] == "USD", "Invoice context must use its own currency.")

# Exercise the actual CLI boundary, including exact JSON decimal parsing and no writes on failure.
with tempfile.TemporaryDirectory(prefix="ana-invoice-test-") as temporary:
    work = Path(temporary)
    record_path = work / "synthetic.json"
    output_path = work / "invoice.md"
    renderer = ROOT / "scripts" / "render_documents.py"
    validator = ROOT / "scripts" / "validate_engagement.py"
    record_path.write_text(json.dumps(fractional), encoding="utf-8")
    result = subprocess.run([sys.executable, str(renderer), str(record_path), "--document", "invoice", "--out", str(output_path)],
                            capture_output=True, text=True)
    require(result.returncode == 0, f"Valid decimal-string invoice must render: {result.stderr}")
    require("EUR 0.02" in output_path.read_text(encoding="utf-8"), "CLI must render the validated total.")
    output_path.unlink()
    for invalid_json in ["{", "null", '{"invoice": []}']:
        record_path.write_text(invalid_json, encoding="utf-8")
        for command in [
            [sys.executable, str(validator), str(record_path), "--stage", "invoice"],
            [sys.executable, str(renderer), str(record_path), "--document", "invoice", "--out", str(output_path)],
        ]:
            result = subprocess.run(command, capture_output=True, text=True)
            require(result.returncode != 0 and "Traceback" not in result.stderr,
                    "Invalid CLI input must fail with a useful message, without a traceback.")
            require(not output_path.exists(), "Rejected records must produce no draft artifact.")

print("Ana HR engagement, recruiting, privacy, and money gate tests passed.")
