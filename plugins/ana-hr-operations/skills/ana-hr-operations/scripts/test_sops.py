#!/usr/bin/env python3
"""Dependency-free structural tests for Ana's operating SOPs."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOP_ROOT = ROOT / "references" / "sops"
EXPECTED = {
    "SOP-00-multi-client-control.md": "SOP-00",
    "SOP-01-first-client-call.md": "SOP-01",
    "SOP-02-client-kickoff.md": "SOP-02",
    "SOP-03-job-description.md": "SOP-03",
    "SOP-04-offer-and-pricing.md": "SOP-04",
    "SOP-05-recruiting-delivery.md": "SOP-05",
    "SOP-06-invoice.md": "SOP-06",
    "SOP-07-send-and-handoff.md": "SOP-07",
}
REQUIRED_SECTIONS = [
    "## Purpose",
    "## Trigger",
    "## Entry criteria",
    "## Procedure",
    "## Exit criteria",
    "## Evidence",
    "## Exceptions",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


index_text = (ROOT / "references" / "sop-index.md").read_text(encoding="utf-8")
skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
require("references/sop-index.md" in skill_text, "Skill must always load the SOP index.")
require("Standard SOP receipt" in index_text, "SOP index must define the evidence receipt.")

for filename, sop_id in EXPECTED.items():
    path = SOP_ROOT / filename
    require(path.is_file(), f"Missing SOP: {filename}")
    text = path.read_text(encoding="utf-8")
    require(text.startswith(f"# {sop_id}"), f"{filename} must start with its SOP identifier.")
    require(sop_id in index_text and filename in index_text, f"SOP index must route {sop_id} to {filename}.")
    for section in REQUIRED_SECTIONS:
        require(section in text, f"{filename} missing section: {section}")
    require("SOP receipt" in text, f"{filename} must require an SOP receipt.")

board = (ROOT / "assets" / "daily-operations-board.md").read_text(encoding="utf-8")
for required in ["Client alias", "Next action", "Awaiting approval", "candidate identities", "not the system of record"]:
    require(required.lower() in board.lower(), f"Daily board missing privacy/control text: {required}")

status = (ROOT / "assets" / "recruiting-weekly-status.md").read_text(encoding="utf-8")
for required in ["ATS snapshot", "Aggregate pipeline", "Client decisions needed", "Candidate identities"]:
    require(required.lower() in status.lower(), f"Recruiting status missing control text: {required}")

print(f"Validated {len(EXPECTED)} Ana HR SOPs and 2 operational assets.")
