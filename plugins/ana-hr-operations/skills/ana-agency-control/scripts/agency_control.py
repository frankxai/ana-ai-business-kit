#!/usr/bin/env python3
"""Deterministic, local agency planning. No connector calls or external actions."""

import argparse
from collections import deque
from datetime import date
import json
import os
from pathlib import Path
import re
import sys


VERSION = "agency-control/v1"
TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,79}\Z")
ROLES = {"agency-owner", "coordinator", "talent-operator", "document-operator"}
SOURCE_KINDS = {"company-policy", "service-catalog", "engagement", "talent-index",
                "meeting-note", "personal-reflection", "clinical"}
AGENCY_WIDE_KINDS = {"company-policy", "service-catalog", "talent-index"}
# Each entry is a proposed specialist and accountable human role, not a delegation.
ROUTES = {
    "knowledge-refresh": ("knowledge-curator", "coordinator"),
    "pipeline-update": ("talent-operations", "talent-operator"),
    "candidate-followup": ("talent-operations", "talent-operator"),
    "service-offer": ("commercial", "document-operator"),
    "employment-offer": ("talent-operations", "talent-operator"),
    "invoice-review": ("finance", "document-operator"),
    "status-update": ("meeting-coordinator", "coordinator"),
    "meeting-decision": ("meeting-coordinator", "coordinator"),
    "client-handoff": ("document-quality", "document-operator"),
}
DECISIONS = {"service-offer", "employment-offer", "invoice-review", "meeting-decision"}
DECISION_OWNERS = {kind: "agency-owner" for kind in DECISIONS | {"client-handoff"}}
DECISION_OWNERS["employment-offer"] = "client-decision-owner"
REQUIRED_DOMAINS = {
    "knowledge-refresh": set(), "pipeline-update": {"talent-index"},
    "candidate-followup": {"talent-index", "engagement"},
    "employment-offer": {"talent-index", "engagement"},
    "service-offer": {"service-catalog", "engagement"},
    **{kind: {"engagement"} for kind in
       ("invoice-review", "client-handoff", "status-update", "meeting-decision")},
}
LIVE_PURPOSES = {"interview", "relationship", "workshop", "conflict", "care"}
OUTCOMES = {
    "knowledge-refresh": "Draft a source change note with proposed owner review and unresolved facts.",
    "pipeline-update": "Draft an alias-only pipeline status update; do not rank or infer candidate suitability.",
    "candidate-followup": "Draft a factual follow-up for human review; do not contact the candidate.",
    "service-offer": "Draft an agency service proposal using approved scope and commercial sources.",
    "employment-offer": "Prepare an employment-offer review checklist for the client decision owner; do not decide selection or terms.",
    "invoice-review": "Prepare an invoice review checklist linked to the approved billable source.",
    "status-update": "Draft an asynchronous status brief with owners, dates, blockers, and next decisions.",
    "meeting-decision": "Draft a decision pre-read with source-backed options and unresolved facts.",
    "client-handoff": "Draft a client handoff checklist with exact artifact revisions and human review state.",
}


class ContractError(ValueError):
    """Invalid structural input; error messages intentionally omit input values."""


def require(condition, message):
    if not condition:
        raise ContractError(message)


def fields(value, required, label):
    require(isinstance(value, dict), f"{label} must be an object")
    require(set(value) == set(required.split()), f"{label} has missing or unknown fields")


def token(value, label):
    require(isinstance(value, str) and TOKEN.fullmatch(value) is not None,
            f"{label} must be a short opaque token, not content or a URL")


def choice(value, options, label):
    require(isinstance(value, str) and value in options, f"{label} is unsupported")


def iso_date(value, label):
    require(isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value),
            f"{label} must be an ISO calendar date")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ContractError(f"{label} must be a valid calendar date") from exc


def array(value, label, minimum=0, maximum=1000):
    require(isinstance(value, list) and minimum <= len(value) <= maximum,
            f"{label} must be an array of {minimum} to {maximum} items")


def unique_tokens(values, label, minimum=0):
    array(values, label, minimum)
    for value in values:
        token(value, label)
    require(len(values) == len(set(values)), f"{label} contains duplicates")


def object_index(items, key, label):
    result = {}
    for item in items:
        require(item[key] not in result, f"{label} contains duplicate identifiers")
        result[item[key]] = item
    return result


def task_order(tasks):
    degree = {key: len(task["depends_on"]) for key, task in tasks.items()}
    children = {key: [] for key in tasks}
    for key, task in tasks.items():
        for dependency in task["depends_on"]:
            require(dependency in tasks, "task dependency references an unknown identifier")
            children[dependency].append(key)
    pending = deque(sorted(key for key in degree if degree[key] == 0))
    ordered = []
    while pending:
        key = pending.popleft()
        ordered.append(key)
        for child in sorted(children[key]):
            degree[child] -= 1
            if degree[child] == 0:
                pending.append(child)
    require(len(ordered) == len(tasks), "task dependencies contain a cycle")
    return ordered


def validate(record):
    fields(record, "schema_version agency_alias as_of sources tasks meetings", "record")
    require(record["schema_version"] == VERSION, "schema_version is unsupported")
    token(record["agency_alias"], "agency_alias")
    iso_date(record["as_of"], "as_of")
    array(record["sources"], "sources", 1)
    array(record["tasks"], "tasks", 1)
    array(record["meetings"], "meetings", maximum=500)
    for source in record["sources"]:
        fields(source, "source_id agency_alias engagement_alias kind reference version owner_role updated_at review_due access_state", "source")
        for key in ("source_id", "agency_alias", "engagement_alias", "reference", "version"):
            token(source[key], "source " + key)
        choice(source["kind"], SOURCE_KINDS, "source kind")
        require(source["engagement_alias"] != "agency-wide" or source["kind"] in AGENCY_WIDE_KINDS,
                "agency-wide scope is only supported for policy, catalog, or talent index sources")
        choice(source["owner_role"], ROLES, "source owner_role")
        choice(source["access_state"], {"confirmed", "unknown", "revoked"}, "source access_state")
        updated = iso_date(source["updated_at"], "source updated_at")
        review = iso_date(source["review_due"], "source review_due")
        require(review >= updated, "source review_due precedes updated_at")
    sources = object_index(record["sources"], "source_id", "sources")
    for task in record["tasks"]:
        fields(task, "task_id kind engagement_alias due_date status source_refs depends_on decision_question", "task")
        token(task["task_id"], "task_id")
        token(task["engagement_alias"], "engagement_alias")
        choice(task["kind"], ROUTES, "task kind")
        iso_date(task["due_date"], "task due_date")
        choice(task["status"], {"pending", "completed"}, "task status")
        unique_tokens(task["depends_on"], "task depends_on")
        array(task["source_refs"], "task source_refs", 1)
        for ref in task["source_refs"]:
            fields(ref, "source_id version", "source reference")
            token(ref["source_id"], "reference source_id")
            token(ref["version"], "reference version")
            require(ref["source_id"] in sources, "task references an unknown source identifier")
        unique_tokens([ref["source_id"] for ref in task["source_refs"]], "task source references", 1)
        question = task["decision_question"]
        require(isinstance(question, str) and len(question) <= 280
                and all(character.isprintable() for character in question),
                "decision_question must be a single line of at most 280 characters")
        if task["kind"] in DECISIONS:
            require(bool(question.strip()), "decision work requires a decision_question")
    tasks = object_index(record["tasks"], "task_id", "tasks")
    task_order(tasks)
    for meeting in record["meetings"]:
        fields(meeting, "meeting_id purpose task_ids planned_minutes attendee_count async_ready requires_live", "meeting")
        token(meeting["meeting_id"], "meeting_id")
        choice(meeting["purpose"], LIVE_PURPOSES | {"status", "decision"}, "meeting purpose")
        unique_tokens(meeting["task_ids"], "meeting task_ids", 1)
        require(all(key in tasks for key in meeting["task_ids"]), "meeting references an unknown task identifier")
        for key, maximum in (("planned_minutes", 240), ("attendee_count", 100)):
            require(type(meeting[key]) is int and 1 <= meeting[key] <= maximum,
                    f"meeting {key} must be an integer from 1 to {maximum}")
        for key in ("async_ready", "requires_live"):
            require(type(meeting[key]) is bool, f"meeting {key} must be a boolean")
    object_index(record["meetings"], "meeting_id", "meetings")
    return record


def source_blockers(source, version, agency, engagement, as_of):
    # Never return IDs, references, versions, owners, or content from blocked sources.
    reasons = []
    if source["agency_alias"] != agency:
        reasons.append("SOURCE_OUTSIDE_AGENCY")
    if source["engagement_alias"] not in {"agency-wide", engagement}:
        reasons.append("SOURCE_OUTSIDE_ENGAGEMENT")
    if source["kind"] in {"personal-reflection", "clinical"}:
        reasons.append("SOURCE_DOMAIN_FORBIDDEN")
    if source["access_state"] != "confirmed":
        reasons.append("SOURCE_ACCESS_UNCONFIRMED")
    if source["version"] != version:
        reasons.append("SOURCE_VERSION_MISMATCH")
    if source["updated_at"] > as_of:
        reasons.append("SOURCE_FROM_FUTURE")
    if source["review_due"] < as_of:
        reasons.append("SOURCE_REVIEW_OVERDUE")
    return reasons


def build_plan(record):
    validate(record)
    sources = {source["source_id"]: source for source in record["sources"]}
    tasks = {task["task_id"]: task for task in record["tasks"]}
    results = {}
    for key in task_order(tasks):
        task = tasks[key]
        reasons = sorted({reason for ref in task["source_refs"]
                          for reason in source_blockers(sources[ref["source_id"]], ref["version"],
                                                        record["agency_alias"], task["engagement_alias"], record["as_of"])})
        domains = {sources[ref["source_id"]]["kind"] for ref in task["source_refs"]
                   if not source_blockers(sources[ref["source_id"]], ref["version"],
                                          record["agency_alias"], task["engagement_alias"], record["as_of"])}
        if not domains or not REQUIRED_DOMAINS[task["kind"]] <= domains:
            reasons.append("MISSING_REQUIRED_SOURCE_DOMAIN")
        waiting = [dependency for dependency in task["depends_on"]
                   if results[dependency]["state"] != "COMPLETED"]
        state = ("BLOCKED" if reasons else "WAITING_ON_DEPENDENCY" if waiting
                 else "COMPLETED" if task["status"] == "completed" else "READY")
        specialist, human = ROUTES[task["kind"]]
        results[key] = {
            "task_id": key, "kind": task["kind"], "due_date": task["due_date"],
            "deadline_state": ("overdue" if task["due_date"] < record["as_of"] else
                               "due_today" if task["due_date"] == record["as_of"] else "upcoming"),
            "state": state, "proposed_specialist": specialist, "proposed_human_owner_role": human,
            "proposed_approval_owner_role": DECISION_OWNERS.get(task["kind"], human),
            "human_review_required": True, "blocker_codes": reasons,
            "waiting_on": waiting if state == "WAITING_ON_DEPENDENCY" else [],
            "source_refs": task["source_refs"] if not reasons else [],
        }
    ordered = sorted(results.values(), key=lambda task: (task["due_date"], task["task_id"]))
    dispatch, cards = [], []
    for specialist in sorted({route[0] for route in ROUTES.values()}):
        ready = [task["task_id"] for task in ordered
                 if task["state"] == "READY" and task["proposed_specialist"] == specialist]
        for offset in range(0, len(ready), 3):
            packets = []
            for key in ready[offset:offset + 3]:
                task, item = tasks[key], results[key]
                packets.append({"task_id": key, "specialist": specialist,
                                "responsible_human_role": item["proposed_human_owner_role"],
                                "approval_owner_role": item["proposed_approval_owner_role"],
                                "agency_alias": record["agency_alias"],
                                "engagement_alias": task["engagement_alias"],
                                "due_date": task["due_date"], "depends_on": task["depends_on"],
                                "source_refs": item["source_refs"], "requested_outcome": OUTCOMES[task["kind"]],
                                "allowed_actions": ["read_source", "draft_artifact"],
                                "source_read_authorization": "HOST_MUST_VERIFY_ACCESS_BEFORE_ANY_READ",
                                "approval_boundary": "HUMAN_REVIEW_BEFORE_ANY_DECISION_OR_EXTERNAL_ACTION",
                                "return_contract": {
                                    "contract_type": "WORKER_RETURN_DESCRIPTION_NOT_EXECUTION_EVIDENCE",
                                    "status_values": ["draft_ready", "blocked", "failed"],
                                    "required_fields": ["task_id", "agency_alias", "engagement_alias", "status",
                                                        "source_versions", "artifact_ref", "artifact_digest",
                                                        "unresolved_facts", "requested_human_decision",
                                                        "execution_receipt", "measured_duration_seconds", "measured_cost"],
                                    "field_rules": {
                                        "source_versions": "Exact source IDs and versions actually read; empty when none.",
                                        "artifact_ref": "Opaque versioned reference; required for draft_ready, otherwise null when absent.",
                                        "artifact_digest": "Verified digest when available; otherwise null.",
                                        "unresolved_facts": "Array of missing or conflicting facts.",
                                        "requested_human_decision": "Unresolved decision for the accountable human; null when none.",
                                        "execution_receipt": "Actual runtime/provider receipt; null when none exists.",
                                        "measured_duration_seconds": "Measured duration; null when unknown, never fabricated zero.",
                                        "measured_cost": "Measured amount and currency; null when unknown, never fabricated zero.",
                                    }}})
            dispatch.append({"proposed_specialist": specialist, "task_ids": ready[offset:offset + 3],
                             "handoff_packets": packets, "execution_state": "PROPOSED_ONLY"})
    for item in ordered:
        task = tasks[item["task_id"]]
        if item["state"] == "READY" and task["kind"] in DECISIONS:
            cards.append({"task_id": task["task_id"], "kind": task["kind"],
                          "decision_question": task["decision_question"], "due_date": task["due_date"],
                          "proposed_decision_owner_role": item["proposed_approval_owner_role"],
                          "source_refs": item["source_refs"],
                          "decision_state": "DRAFT_QUESTION_PREPARATION_REQUIRED",
                          "reviewable_artifact_verified": False})
    meetings, minutes, person_minutes = [], 0, 0
    for meeting in sorted(record["meetings"], key=lambda item: item["meeting_id"]):
        pre_read_ready = all(results[key]["state"] in {"READY", "COMPLETED"} for key in meeting["task_ids"])
        protected = meeting["purpose"] in LIVE_PURPOSES or meeting["requires_live"]
        if protected:
            recommendation = "KEEP_LIVE"
        elif not pre_read_ready:
            recommendation = "REPAIR_PRE_READ"
        elif meeting["async_ready"]:
            recommendation = ("ASYNC_DECISION_CANDIDATE" if meeting["purpose"] == "decision"
                              else "ASYNC_CANDIDATE")
        else:
            recommendation = "KEEP_LIVE"
        eligible = recommendation.startswith("ASYNC_")
        modeled_minutes = meeting["planned_minutes"] if eligible else 0
        modeled_person_minutes = modeled_minutes * meeting["attendee_count"]
        minutes += modeled_minutes
        person_minutes += modeled_person_minutes
        meetings.append({"meeting_id": meeting["meeting_id"], "purpose": meeting["purpose"],
                         "task_ids": meeting["task_ids"], "recommendation": recommendation,
                         "pre_read_state": ("REPAIR_REQUIRED" if not pre_read_ready else
                                            "DECLARED_READY" if meeting["async_ready"] else "READINESS_NOT_DECLARED"),
                         "pre_read_artifact_verified": False,
                         "organizer_authorization_required": True,
                         "modeled_meeting_minutes": modeled_minutes,
                         "modeled_person_minutes": modeled_person_minutes})
    return {"schema_version": VERSION, "agency_alias": record["agency_alias"], "as_of": record["as_of"],
            "status": "INTERNAL_PLANNING_DRAFT", "authenticated": False, "external_actions_allowed": False,
            "source_access_basis": "OPERATOR_DECLARATION_NOT_ACCESS_ENFORCEMENT",
            "host_max_concurrent_workers": 3, "host_concurrency_limit_state": "PROPOSED_RUNTIME_CEILING_ONLY",
            "dispatch_limit_per_group": 3, "dispatch_groups": dispatch, "tasks": ordered,
            "decision_cards": cards, "meetings": meetings,
            "meeting_opportunity": {"basis": "MODELED_GROSS_OPPORTUNITY_NOT_MEASURED_SAVINGS",
                                    "meeting_minutes": minutes, "person_minutes": person_minutes,
                                    "async_preparation_cost_included": False, "actual_saved_minutes": None}}


def safe_text(value):
    # Free text remains untrusted data, including when Markdown is rendered.
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("|", "\\|").replace("`", "\\`")


def render_markdown(plan):
    lines = ["# Agency control — internal planning draft", "",
             f"Agency alias: {plan['agency_alias']} · As of: {plan['as_of']}", "",
             "Authenticated: false. External actions allowed: false. No agents were launched.",
             "Proposed host concurrency ceiling: three workers. Dispatch groups are task bundles, not worker executions.",
             "Source access is an operator declaration; this planner does not enforce access permissions.", "",
             "## Proposed work", "", "| Task | State | Specialist | Preparer role | Approval role | Due | Blocker |",
             "| --- | --- | --- | --- | --- | --- | --- |"]
    for task in plan["tasks"]:
        blockers = ", ".join(task["blocker_codes"] + task["waiting_on"]) or "—"
        lines.append(f"| {task['task_id']} | {task['state']} | {task['proposed_specialist']} | "
                     f"{task['proposed_human_owner_role']} | {task['proposed_approval_owner_role']} | "
                     f"{task['due_date']} ({task['deadline_state']}) | {blockers} |")
    lines += ["", "## Proposed dispatch groups", "", "Each group contains at most three tasks; no worker execution is authorized."]
    for group in plan["dispatch_groups"]:
        lines.append(f"- {group['proposed_specialist']}: {', '.join(group['task_ids'])}")
        for packet in group["handoff_packets"]:
            refs = ", ".join(f"{ref['source_id']}@{ref['version']}" for ref in packet["source_refs"])
            lines.append(f"  - {packet['task_id']}: {packet['requested_outcome']} Due {packet['due_date']}; sources {refs}.")
    lines += ["", "## Draft decision questions", "",
              "Preparation is still required; no reviewable decision artifact has been verified.", ""]
    for card in plan["decision_cards"]:
        refs = ", ".join(f"{ref['source_id']}@{ref['version']}" for ref in card["source_refs"])
        lines += [f"- {card['task_id']}: {safe_text(card['decision_question'])}",
                  f"  Proposed owner: {card['proposed_decision_owner_role']}; due {card['due_date']}; sources: {refs}."]
    lines += ["", "## Meeting review", "", "All meeting changes require organizer authorization; nothing is canceled or scheduled. Pre-read readiness is declared, not artifact-verified."]
    for meeting in plan["meetings"]:
        lines.append(f"- {meeting['meeting_id']}: {meeting['recommendation']}; pre-read {meeting['pre_read_state']}.")
    opportunity = plan["meeting_opportunity"]
    lines += ["", f"Modeled gross opportunity: {opportunity['meeting_minutes']} meeting minutes; "
              f"{opportunity['person_minutes']} person-minutes. These are not measured savings.",
              "Async preparation cost is excluded. Actual saved time is unmeasured.", ""]
    return "\n".join(lines)


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "JSON contains a duplicate object key")
        result[key] = value
    return result


def reject_constant(_value):
    raise ContractError("JSON non-finite numbers are unsupported")


def write_fresh(path, content):
    path = Path(path)
    try:
        with os.fdopen(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "w", encoding="utf-8") as output:
            output.write(content)
    except FileExistsError:
        require(path.is_file() and not path.is_symlink()
                and path.read_text(encoding="utf-8") == content,
                "output already exists with different content; choose a fresh path")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("validate", "plan"):
        sub = commands.add_parser(command)
        sub.add_argument("record")
        if command == "plan":
            sub.add_argument("--out", help="Create an internal Markdown draft; refuse differing overwrite")
    args = parser.parse_args(argv)
    try:
        record = json.loads(Path(args.record).read_text(encoding="utf-8"),
                            object_pairs_hook=no_duplicate_keys, parse_constant=reject_constant)
        validate(record)
        if args.command == "validate":
            result = {"valid": True, "schema_version": VERSION,
                      "source_count": len(record["sources"]), "task_count": len(record["tasks"]),
                      "meeting_count": len(record["meetings"])}
        else:
            result = build_plan(record)
            if args.out:
                write_fresh(args.out, render_markdown(result))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, UnicodeError, RecursionError, OverflowError) as exc:
        # File-system and parser exceptions can include private input/path fragments.
        message = str(exc) if isinstance(exc, ContractError) else "unable to read valid input or write the requested draft"
        print("Invalid agency record: " + message, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
