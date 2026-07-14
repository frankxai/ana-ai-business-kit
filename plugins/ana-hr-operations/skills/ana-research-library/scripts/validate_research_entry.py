#!/usr/bin/env python3
"""Validate a privacy-safe Ana research library entry without external dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


REQUIRED_PATHS = [
    "schema",
    "entry_id",
    "status",
    "topic",
    "question",
    "intended_audience",
    "proposed_safe_use",
    "source.title",
    "source.publisher",
    "source.url",
    "source.source_class",
    "source.published_or_accessed",
    "claim.source_supported_claim",
    "claim.team_interpretation",
    "claim.limitations",
    "applicability.allowed_contexts",
    "applicability.prohibited_uses",
    "evidence.strength",
    "ownership.curator",
    "ownership.reviewer",
    "ownership.reviewed_at",
    "ownership.next_review_due",
    "privacy.contains_personal_data",
    "privacy.approved_for_external_summary",
]
VALID_STATUSES = {
    "CAPTURED",
    "CURATOR_REVIEWED",
    "ANA_APPROVED_FOR_INTERNAL_REFERENCE",
    "EXPIRED_OR_SUPERSEDED",
}
FORBIDDEN_KEYS = {
    "candidate",
    "candidates",
    "candidate_name",
    "candidate_email",
    "employee_name",
    "employee_email",
    "cv",
    "resume",
    "interview_notes",
    "medical_information",
    "health_data",
    "diagnosis",
}
REQUIRED_PROHIBITIONS = {
    "candidate ranking by ai",
    "protected-trait inference",
    "personality or emotion profiling",
    "automated employment decision",
}
PRIVATE_REFERENCE_RE = re.compile(r"^PRIVATE-[A-Z0-9][A-Z0-9._-]{2,127}$")


def get_path(data: dict, dotted: str):
    current = data
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def present(value) -> bool:
    return value is not None and value != "" and value != [] and value != {}


def find_forbidden_keys(value, path: str = "") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else key
            if key.lower() in FORBIDDEN_KEYS:
                found.append(child_path)
            found.extend(find_forbidden_keys(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(find_forbidden_keys(child, f"{path}[{index}]"))
    return found


def parse_iso_date(value, label: str, errors: list[str]) -> date | None:
    try:
        return date.fromisoformat(str(value))
    except (TypeError, ValueError):
        errors.append(f"{label} must be an ISO date (YYYY-MM-DD).")
        return None


def validate(entry: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(entry, dict):
        return ["Research entry must be a JSON object."]
    if entry.get("schema") != "ana-research-entry/v1":
        errors.append("schema must be ana-research-entry/v1.")
    if entry.get("demo_only") is not True and get_path(entry, "privacy.contains_personal_data") is not False:
        errors.append("Live research entries must explicitly confirm contains_personal_data is false.")
    for path in REQUIRED_PATHS:
        if not present(get_path(entry, path)) and get_path(entry, path) is not False:
            errors.append(f"Missing {path}.")
    for forbidden_path in find_forbidden_keys(entry):
        errors.append(f"Forbidden sensitive field in research entry: {forbidden_path}.")
    if entry.get("status") not in VALID_STATUSES:
        errors.append("status must be a known research review status.")
    source_url = str(get_path(entry, "source.url") or "")
    parsed = urlparse(source_url)
    is_private_reference = PRIVATE_REFERENCE_RE.fullmatch(source_url) is not None
    if not is_private_reference and (parsed.scheme != "https" or not parsed.netloc):
        errors.append("source.url must be an absolute HTTPS URL or approved private reference URL.")
    reviewed = parse_iso_date(get_path(entry, "ownership.reviewed_at"), "ownership.reviewed_at", errors)
    due = parse_iso_date(get_path(entry, "ownership.next_review_due"), "ownership.next_review_due", errors)
    if reviewed and due and due < reviewed:
        errors.append("ownership.next_review_due must not be before ownership.reviewed_at.")
    if get_path(entry, "privacy.contains_personal_data") is not False:
        errors.append("privacy.contains_personal_data must be false.")
    prohibited = {str(value).lower() for value in (get_path(entry, "applicability.prohibited_uses") or [])}
    for required in REQUIRED_PROHIBITIONS:
        if required not in prohibited:
            errors.append(f"applicability.prohibited_uses must include: {required}.")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("entry", type=Path)
    args = parser.parse_args()
    entry = json.loads(args.entry.read_text(encoding="utf-8"))
    errors = validate(entry)
    if errors:
        print("Research entry validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Validated research entry: {args.entry.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
