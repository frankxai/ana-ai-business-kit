#!/usr/bin/env python3
"""Dependency-free tests for Ana Approved Content controls."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from validate_content_brief import validate


ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = json.loads((ROOT / "assets" / "content-brief.example.json").read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


require(not validate(EXAMPLE), "Draft content example must validate.")

unsupported = copy.deepcopy(EXAMPLE)
unsupported["draft"] += " This is guaranteed to transform hiring."
require(any("guaranteed" in error for error in validate(unsupported)), "Guarantee language must fail.")

unattributed = copy.deepcopy(EXAMPLE)
unattributed["claims"][0]["source_entry_id"] = "LIB-NOT-IN-BRIEF"
require(any("source_entry_id" in error for error in validate(unattributed)), "Every claim must point to a supplied source entry.")

false_approval = copy.deepcopy(EXAMPLE)
false_approval["approval"]["approved_by"] = "Ana"
require(any("Draft content" in error for error in validate(false_approval)), "Drafts cannot contain an approval receipt.")

published_without_receipt = copy.deepcopy(EXAMPLE)
published_without_receipt["status"] = "PUBLISHED_EXTERNALLY_RECEIPTED"
published_without_receipt["approval"] = {"required_from": "Ana", "approved_by": "Ana", "approved_at": "2026-07-14"}
require(any("Published receipt" in error for error in validate(published_without_receipt)), "Published status must require a human receipt.")

bad_schema = copy.deepcopy(EXAMPLE)
bad_schema["schema"] = "bad-schema/v1"
require(any("schema must be ana-approved-content/v1" in error for error in validate(bad_schema)), "Bad schema validation must fail.")

missing_path = copy.deepcopy(EXAMPLE)
missing_path.pop("content_id")
require(any("Missing content_id" in error for error in validate(missing_path)), "Missing content_id must fail.")

missing_nested_path = copy.deepcopy(EXAMPLE)
missing_nested_path["approval"].pop("required_from")
require(any("Missing approval.required_from" in error for error in validate(missing_nested_path)), "Missing nested approval path must fail.")

bad_status = copy.deepcopy(EXAMPLE)
bad_status["status"] = "UNKNOWN_STATUS"
require(any("status must be a known approval-gated content status" in error for error in validate(bad_status)), "Unknown status must fail.")

bad_source_ids = copy.deepcopy(EXAMPLE)
bad_source_ids["source_entry_ids"] = ["BAD-ID-123"]
require(any("non-empty list of reviewed LIB-*" in error for error in validate(bad_source_ids)), "Invalid source ID prefixes must fail.")

published_missing_approved_by = copy.deepcopy(EXAMPLE)
published_missing_approved_by["status"] = "PUBLISHED_EXTERNALLY_RECEIPTED"
published_missing_approved_by["approval"]["approved_by"] = None
published_missing_approved_by["publication_receipt"] = {"reported_by": "Jane", "url_or_reference": "https://example.com/published"}
require(any("Approved content must name approval.approved_by" in error for error in validate(published_missing_approved_by)), "Missing approved_by must fail.")

bad_date_format = copy.deepcopy(EXAMPLE)
bad_date_format["status"] = "ANA_CONTENT_APPROVED"
bad_date_format["approval"] = {"required_from": "Ana", "approved_by": "Ana", "approved_at": "bad-date"}
require(any("approval.approved_at must be an ISO date" in error for error in validate(bad_date_format)), "Invalid date format must fail.")

published_invalid_date = copy.deepcopy(EXAMPLE)
published_invalid_date["status"] = "PUBLISHED_EXTERNALLY_RECEIPTED"
published_invalid_date["approval"] = {"required_from": "Ana", "approved_by": "Ana", "approved_at": "2026-07-14"}
published_invalid_date["publication_receipt"] = {"reported_by": "Jane", "url_or_reference": "https://example.com", "published_at": "bad-date"}
require(any("publication_receipt.published_at must be an ISO date" in error for error in validate(published_invalid_date)), "Invalid publication date format must fail.")

draft_with_receipt = copy.deepcopy(EXAMPLE)
draft_with_receipt["publication_receipt"] = {"reported_by": "Jane", "url_or_reference": "https://example.com"}
require(any("Only a published receipt status may include publication_receipt" in error for error in validate(draft_with_receipt)), "Draft with publication receipt must fail.")

print("Ana Approved Content source, claim, and approval gate tests passed.")
