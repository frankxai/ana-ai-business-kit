#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

ARTIFACTS = {"kickoff", "job-description", "offer", "offer-presentation", "invoice", "client-presentation", "handoff"}
MODES = {"guided", "orchestrated"}
PLATFORMS = {"google-docs", "canva", "markdown"}
ROUTES = {"exact-master", "starter-practice", "generated-candidate", "local-fallback"}
STATUSES = {
    "TEMPLATE_BLOCKED", "DRAFT_CONTENT_READY", "CANVA_CANDIDATE_SELECTION_PENDING",
    "CANVA_CANDIDATE_SELECTED", "COPY_CREATED", "GOOGLE_DOCS_READBACK_COMPLETE",
    "CANVA_RENDER_PENDING", "REVIEW_COMPLETE", "ANA_CONTENT_APPROVED", "READY_FOR_HANDOFF_REVIEW",
}

def require(data, path, failures):
    value = data
    for part in path.split("."):
        if not isinstance(value, dict) or part not in value:
            failures.append(f"Missing required field: {path}")
            return None
        value = value[part]
    if value in (None, "", []):
        failures.append(f"Required field is empty: {path}")
    return value

def validate(data):
    failures = []
    for path in [
        "schema", "job_id", "engagement_id", "client_alias", "artifact_type", "mode", "platform",
        "status", "upstream.sop_id", "upstream.stage", "upstream.validation",
        "upstream.receipt_reference", "route", "source.content_pack_reference",
        "source.destination_reference", "source.facts_reviewed_at", "content.approved_fact_references",
        "content.required_sections", "artifact.master_never_edit", "artifact.downstream_stage",
        "verification.google_docs_readback", "verification.canva_candidate_selection",
        "verification.canva_visual_check", "approvals.copy", "approvals.content", "approvals.send",
        "next.action", "next.owner", "next.due_date", "next.external_action_still_requiring_ana",
    ]:
        require(data, path, failures)
    if data.get("schema") != "ana-template-job/v1": failures.append("schema must be ana-template-job/v1")
    if data.get("artifact_type") not in ARTIFACTS: failures.append("unsupported artifact_type")
    if data.get("mode") not in MODES: failures.append("mode must be guided or orchestrated")
    if data.get("platform") not in PLATFORMS: failures.append("unsupported platform")
    if data.get("route") not in ROUTES: failures.append("unsupported route")
    if data.get("status") not in STATUSES: failures.append("unsupported status")
    if data.get("upstream", {}).get("validation") != "pass": failures.append("upstream validation must pass")
    if data.get("artifact", {}).get("master_never_edit") is not True: failures.append("master_never_edit must be true")

    route = data.get("route")
    status = data.get("status")
    platform = data.get("platform")
    artifact = data.get("artifact", {})
    verification = data.get("verification", {})
    if route == "generated-candidate":
        if platform != "canva": failures.append("generated-candidate route requires canva")
        if not artifact.get("generation_job_reference"): failures.append("generated-candidate route needs generation_job_reference")
        if status not in {"CANVA_CANDIDATE_SELECTION_PENDING", "CANVA_CANDIDATE_SELECTED", "COPY_CREATED", "CANVA_RENDER_PENDING", "REVIEW_COMPLETE", "ANA_CONTENT_APPROVED", "READY_FOR_HANDOFF_REVIEW"}:
            failures.append("generated-candidate route has incompatible status")
        if status != "CANVA_CANDIDATE_SELECTION_PENDING" and not artifact.get("candidate_reference"):
            failures.append("selected/generated Canva states need candidate_reference")
    if platform == "google-docs" and status in {"GOOGLE_DOCS_READBACK_COMPLETE", "REVIEW_COMPLETE", "ANA_CONTENT_APPROVED", "READY_FOR_HANDOFF_REVIEW"}:
        if verification.get("google_docs_readback") != "complete": failures.append("Google Docs ready states require complete readback")
    if platform == "canva" and status in {"REVIEW_COMPLETE", "ANA_CONTENT_APPROVED", "READY_FOR_HANDOFF_REVIEW"}:
        if verification.get("canva_visual_check") != "complete": failures.append("Canva ready states require complete visual check")
        if not verification.get("visual_checked_by") or not verification.get("visual_checked_at"):
            failures.append("Canva ready states require named visual check evidence")
    if status == "READY_FOR_HANDOFF_REVIEW" and data.get("approvals", {}).get("content") not in {"approved", "approved-fictional"}:
        failures.append("READY_FOR_HANDOFF_REVIEW requires content approval")
    if data.get("demo_only") is not True:
        failures.append("public validator accepts demo_only records only; live records stay private")
    return failures

def main():
    parser = argparse.ArgumentParser(description="Validate a public-safe Ana template job.")
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    data = json.loads(args.record.read_text(encoding="utf-8"))
    failures = validate(data)
    if failures:
        print("Template job validation failed:")
        for failure in failures: print(f"- {failure}")
        raise SystemExit(1)
    print(f"Template job validated: {data['job_id']} ({data['status']})")

if __name__ == "__main__":
    main()
