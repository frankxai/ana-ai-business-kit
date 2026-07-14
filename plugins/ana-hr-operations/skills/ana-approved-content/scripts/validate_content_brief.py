#!/usr/bin/env python3
"""Validate an approval-gated Ana content brief without external dependencies."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path


REQUIRED_PATHS = [
    "schema",
    "content_id",
    "status",
    "audience",
    "format",
    "proposed_channel",
    "title",
    "source_entry_ids",
    "claims",
    "draft",
    "call_to_action",
    "boundaries",
    "approval.required_from",
]
VALID_STATUSES = {
    "DRAFT_REVIEW_REQUIRED",
    "ANA_CONTENT_APPROVED",
    "PUBLISHED_EXTERNALLY_RECEIPTED",
}
FORBIDDEN_TERMS = {
    "guaranteed",
    "guarantee",
    "neuroscience proves",
    "diagnose",
    "personality type",
    "emotion inference",
    "fake testimonial",
    "limited spots",
}


def get_path(data: dict, dotted: str):
    current = data
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def present(value) -> bool:
    return value is not None and value != "" and value != [] and value != {}


def parse_iso_date(value, label: str, errors: list[str]) -> date | None:
    try:
        return date.fromisoformat(str(value))
    except (TypeError, ValueError):
        errors.append(f"{label} must be an ISO date (YYYY-MM-DD).")
        return None


def all_text(value) -> str:
    if isinstance(value, dict):
        return " ".join(all_text(child) for child in value.values())
    if isinstance(value, list):
        return " ".join(all_text(child) for child in value)
    return str(value)


def validate(brief: dict) -> list[str]:
    errors: list[str] = []
    if brief.get("schema") != "ana-approved-content/v1":
        errors.append("schema must be ana-approved-content/v1.")
    for path in REQUIRED_PATHS:
        if not present(get_path(brief, path)):
            errors.append(f"Missing {path}.")
    if brief.get("status") not in VALID_STATUSES:
        errors.append("status must be a known approval-gated content status.")
    source_ids = brief.get("source_entry_ids") or []
    if not isinstance(source_ids, list) or not all(str(value).startswith("LIB-") for value in source_ids):
        errors.append("source_entry_ids must be a non-empty list of reviewed LIB-* entries.")
    for index, claim in enumerate(brief.get("claims") or []):
        if not isinstance(claim, dict) or not present(claim.get("text")) or claim.get("source_entry_id") not in source_ids:
            errors.append(f"claims[{index}] must have text and a source_entry_id included in source_entry_ids.")
    text = all_text({key: value for key, value in brief.items() if key != "publication_receipt"}).lower()
    for term in FORBIDDEN_TERMS:
        if term in text:
            errors.append(f"Content brief contains prohibited or unsupported phrasing: {term}.")
    status = brief.get("status")
    approval = brief.get("approval") or {}
    if status in {"ANA_CONTENT_APPROVED", "PUBLISHED_EXTERNALLY_RECEIPTED"}:
        if not present(approval.get("approved_by")):
            errors.append("Approved content must name approval.approved_by.")
        parse_iso_date(approval.get("approved_at"), "approval.approved_at", errors)
    elif approval.get("approved_by") is not None or approval.get("approved_at") is not None:
        errors.append("Draft content must not contain an approval receipt.")
    receipt = brief.get("publication_receipt")
    if status == "PUBLISHED_EXTERNALLY_RECEIPTED":
        if not isinstance(receipt, dict) or not present(receipt.get("reported_by")) or not present(receipt.get("url_or_reference")):
            errors.append("Published receipt requires a human-reported author and URL/reference.")
        elif receipt.get("published_at"):
            parse_iso_date(receipt.get("published_at"), "publication_receipt.published_at", errors)
    elif receipt is not None:
        errors.append("Only a published receipt status may include publication_receipt.")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("brief", type=Path)
    args = parser.parse_args()
    brief = json.loads(args.brief.read_text(encoding="utf-8"))
    errors = validate(brief)
    if errors:
        print("Content brief validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Validated content brief: {args.brief.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
