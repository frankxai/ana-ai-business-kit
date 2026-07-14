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

print("Ana Approved Content source, claim, and approval gate tests passed.")
