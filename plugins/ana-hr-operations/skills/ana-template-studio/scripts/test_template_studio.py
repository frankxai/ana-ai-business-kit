#!/usr/bin/env python3
import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validator", Path(__file__).with_name("validate_template_job.py"))
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)
example = json.loads((ROOT / "assets" / "template-job.example.json").read_text(encoding="utf-8"))

assert validator.validate(example) == []

bad_master = copy.deepcopy(example)
bad_master["artifact"]["master_never_edit"] = False
assert any("master_never_edit" in failure for failure in validator.validate(bad_master))

bad_selection = copy.deepcopy(example)
bad_selection["status"] = "CANVA_CANDIDATE_SELECTED"
assert any("candidate_reference" in failure for failure in validator.validate(bad_selection))

false_ready = copy.deepcopy(example)
false_ready["status"] = "READY_FOR_HANDOFF_REVIEW"
false_ready["artifact"]["candidate_reference"] = "DEMO-CANDIDATE"
assert any("visual check" in failure for failure in validator.validate(false_ready))

live_record = copy.deepcopy(example)
live_record["demo_only"] = False
assert any("live records stay private" in failure for failure in validator.validate(live_record))

print("Ana Template Studio tests passed.")
