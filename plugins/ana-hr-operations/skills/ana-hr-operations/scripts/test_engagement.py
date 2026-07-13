#!/usr/bin/env python3
"""Dependency-free tests for the engagement gates and render templates."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from string import Template

from render_documents import context
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

currency_mismatch = copy.deepcopy(EXAMPLE)
currency_mismatch["invoice"]["currency"] = "USD"
require(any("currency" in error.lower() for error in validate(currency_mismatch, "invoice")), "Currency mismatch must fail.")

render_context = context(EXAMPLE)
for document in ["job-description", "offer", "invoice"]:
    template = Template((ROOT / "assets" / f"{document}.md").read_text(encoding="utf-8"))
    rendered = template.safe_substitute(render_context)
    require("${" not in rendered, f"{document} has unresolved placeholders.")
    require("DRAFT" in rendered, f"{document} must remain visibly draft-labeled.")

print("Ana HR engagement gate tests passed.")
