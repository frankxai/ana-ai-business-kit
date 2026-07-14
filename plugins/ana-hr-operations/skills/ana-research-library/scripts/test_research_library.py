#!/usr/bin/env python3
"""Dependency-free tests for Ana Research Library entry controls."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from validate_research_entry import validate


ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = json.loads((ROOT / "assets" / "research-entry.example.json").read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


require(not validate(EXAMPLE), "Research example must validate.")

candidate_data = copy.deepcopy(EXAMPLE)
candidate_data["candidate_name"] = "Example Person"
require(any("Forbidden sensitive field" in error for error in validate(candidate_data)), "Candidate data must fail.")

missing_boundary = copy.deepcopy(EXAMPLE)
missing_boundary["applicability"]["prohibited_uses"].remove("automated employment decision")
require(any("automated employment decision" in error for error in validate(missing_boundary)), "Employment-decision boundary must be required.")

bad_date = copy.deepcopy(EXAMPLE)
bad_date["ownership"]["next_review_due"] = "2020-01-01"
require(any("next_review_due" in error for error in validate(bad_date)), "Review dates must be ordered.")

null_privacy = copy.deepcopy(EXAMPLE)
null_privacy["privacy"] = None
require(any("privacy.contains_personal_data" in error for error in validate(null_privacy)), "Null privacy must fail without crashing.")

private_reference = copy.deepcopy(EXAMPLE)
private_reference["source"]["url"] = "PRIVATE-SOURCE-STRUCTURED-INTERVIEWS-001"
require(not validate(private_reference), "A constrained approved private source reference must validate.")

unsafe_reference = copy.deepcopy(EXAMPLE)
unsafe_reference["source"]["url"] = "file:///private/source.txt"
require(any("source.url" in error for error in validate(unsafe_reference)), "Arbitrary URL schemes must fail.")

require(
    validate(["not", "an", "object"]) == ["Research entry must be a JSON object."],
    "Non-object JSON must fail without crashing.",
)

print("Ana Research Library privacy, evidence, and boundary tests passed.")
