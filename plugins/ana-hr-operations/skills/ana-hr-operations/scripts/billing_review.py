#!/usr/bin/env python3
"""Local invoice review evidence only. No authentication, issuance, or sending.

The private SQLite file must be access-controlled and backed up by its operator.
Hashes detect content mismatch; a person able to edit this database can edit its
history. Source/reviewer references are unverified manual evidence references.
One event reserves one invoice number for its whole subtotal in this ledger.
There is no cross-ledger uniqueness, budget aggregation, or partial billing.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import sys
import uuid

from render_documents import render
from validate_engagement import SUPPORTED_CURRENCIES, money


VERSION = 1
TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
HASH = re.compile(r"[0-9a-f]{64}\Z")
EVENT_FIELDS = {
    "schema_version", "agency_alias", "event_id", "engagement_id",
    "source_reference", "source_sha256", "source_review_reference",
    "evidence_reference", "currency", "billable_subtotal",
    "finance_destination_reference", "policy_version",
}
STRING_SECTIONS = {
    "administration": "client_alias record_owner current_stage next_action next_owner next_due_date last_reviewed_at risk_level",
    "client": "legal_name contact_name contact_email billing_name billing_address billing_email",
    "privacy": "client_system candidate_system retention_owner deletion_rule incident_contact",
    "kickoff": "company_context hiring_need timeline scope communication_cadence selection_process",
    "role": "title location employment_type reporting_to mission compensation recruitment_process",
    "offer": "service_name timeline currency payment_terms valid_until",
    "invoice": "invoice_number issue_date due_date currency payment_terms payment_details_reference",
    "recruiting": "ats_reference requisition_status scorecard_reference structured_process pipeline_snapshot_at next_client_update",
    "handoff": "artifact_type artifact_reference artifact_revision",
    "team": "manager_approver engagement_coordinator research_recruiting_operator document_client_experience_operator",
    "template": "registry_reference google_doc_url comparable_doc_url",
}
LIST_SECTIONS = {
    "administration": "blockers", "kickoff": "success_outcomes decision_makers",
    "role": "outcomes responsibilities must_have nice_to_have",
    "offer": "deliverables exclusions", "recruiting": "change_requests",
}
MONEY_FIELDS = {"subtotal", "tax_rate", "tax_amount", "total"}
APPROVALS = {"kickoff", "job_description", "recruiting_launch", "price", "offer", "invoice", "send"}
ROUTES = {"kickoff", "job-description", "offer", "invoice", "recruiting-status"}


class LedgerError(ValueError):
    pass


def token(value, label: str) -> str:
    if not isinstance(value, str) or not TOKEN.fullmatch(value):
        raise LedgerError(f"{label} must be a 1–128 character token (letters, digits, . _ : -).")
    return value


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def hash_value(value, label: str) -> str:
    if not isinstance(value, str) or not HASH.fullmatch(value):
        raise LedgerError(f"{label} must be a lowercase SHA256 digest.")
    return value


def canonical(value, depth: int = 0) -> str:
    """Deterministic semantic JSON, preserving exact numeric values and types."""
    if depth > 20:
        raise LedgerError("JSON nesting exceeds the local ledger limit.")
    if isinstance(value, dict):
        if len(value) > 1000 or any(not isinstance(k, str) for k in value):
            raise LedgerError("JSON objects require string keys and at most 1000 fields.")
        return "{" + ",".join(json.dumps(k, ensure_ascii=True) + ":" + canonical(value[k], depth + 1) for k in sorted(value)) + "}"
    if isinstance(value, list):
        if len(value) > 1000:
            raise LedgerError("JSON arrays exceed the local ledger limit.")
        return "[" + ",".join(canonical(v, depth + 1) for v in value) + "]"
    if value is None or isinstance(value, bool):
        return json.dumps(value)
    if isinstance(value, (int, float, Decimal)):
        number = Decimal(str(value))
        if not number.is_finite() or len(number.as_tuple().digits) > 128 or abs(number.as_tuple().exponent) > 128:
            raise LedgerError("JSON numbers must be finite and within 128 digits/places.")
        text = format(number, "f")
        return (text.rstrip("0").rstrip(".") if "." in text else text) if number else "0"
    if isinstance(value, str) and len(value) <= 10000:
        return json.dumps(value, ensure_ascii=True)
    raise LedgerError("Unsupported JSON value or string longer than 10000 characters.")


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise LedgerError(f"Duplicate JSON key: {key}.")
        result[key] = value
    return result


def _nonfinite(value):
    raise LedgerError("Nonfinite JSON numbers are not supported.")


def decode(text: str):
    value = json.loads(text, parse_float=Decimal, parse_constant=_nonfinite, object_pairs_hook=_pairs)
    canonical(value)
    return value


def read_json(path: Path):
    if path.stat().st_size > 1_000_000:
        raise LedgerError("JSON input exceeds the 1 MB local ledger limit.")
    return decode(path.read_text(encoding="utf-8"))


def keys(value, allowed, label: str, *, exact=False):
    if not isinstance(value, dict):
        raise LedgerError(f"{label} must be an object.")
    extra = set(value) - set(allowed)
    missing = set(allowed) - set(value) if exact else set()
    if extra or missing:
        raise LedgerError(f"{label} has unknown fields {sorted(extra)} or missing fields {sorted(missing)}.")


def strings(value, fields, label):
    for field in set(fields) & set(value):
        if not isinstance(value[field], str):
            raise LedgerError(f"{label}.{field} must be a string.")


def validate_record(record):
    """Fail closed on the supported engagement shape before the existing gate."""
    canonical(record)
    keys(record, set(STRING_SECTIONS) | {"demo_only", "engagement_id", "status", "approvals"}, "engagement")
    if "demo_only" in record and not isinstance(record["demo_only"], bool):
        raise LedgerError("demo_only must be boolean.")
    strings(record, {"status", "engagement_id"}, "engagement")
    token(record.get("engagement_id"), "engagement_id")
    for section, text_fields in STRING_SECTIONS.items():
        if section not in record:
            continue
        block = record[section]
        text_fields = set(text_fields.split())
        lists = set(LIST_SECTIONS.get(section, "").split())
        extras = MONEY_FIELDS if section in {"offer", "invoice"} else set()
        extras = extras | ({"line_items"} if section == "invoice" else set())
        extras = extras | ({"pipeline_counts"} if section == "recruiting" else set())
        extras = extras | ({"document_routes"} if section == "template" else set())
        keys(block, text_fields | lists | extras, section)
        strings(block, text_fields, section)
        for name in lists & set(block):
            if not isinstance(block[name], list) or any(not isinstance(v, str) for v in block[name]):
                raise LedgerError(f"{section}.{name} must be a list of strings.")
    approvals = record.get("approvals", {})
    keys(approvals, APPROVALS, "approvals")
    for name, value in approvals.items():
        allowed = {"approved_by", "approved_at"} | ({"channel", "recipient"} if name == "send" else set())
        keys(value, allowed, f"approvals.{name}")
        strings(value, allowed, f"approvals.{name}")
    items = record.get("invoice", {}).get("line_items", [])
    if not isinstance(items, list):
        raise LedgerError("invoice.line_items must be a list.")
    for item in items:
        keys(item, {"description", "quantity", "unit_price", "amount"}, "invoice line", exact=True)
    counts = record.get("recruiting", {}).get("pipeline_counts", {})
    keys(counts, {"sourced", "contacted", "responded", "screened", "client_review", "interview", "reference", "offer", "placed"}, "pipeline_counts")
    if any(not isinstance(v, int) or isinstance(v, bool) or v < 0 for v in counts.values()):
        raise LedgerError("pipeline_counts must contain non-negative integers.")
    routes = record.get("template", {}).get("document_routes", {})
    keys(routes, ROUTES, "document_routes")
    for route in routes.values():
        keys(route, {"template_id", "platform", "status", "visual_check_required"}, "document route", exact=True)
        strings(route, {"template_id", "platform", "status"}, "document route")
    artifact = render(record, "invoice").encode("utf-8")
    token(record["invoice"]["invoice_number"], "invoice_number")
    token(record["invoice"]["payment_details_reference"], "payment_details_reference")
    recipient = record["client"]["billing_email"]
    if not recipient.strip() or len(recipient) > 254 or any(ord(c) < 32 or ord(c) == 127 for c in recipient):
        raise LedgerError("billing_email must be a nonempty, single-line recipient of at most 254 characters.")
    return artifact


def validate_event(event, agency: str, source: Path):
    canonical(event)
    keys(event, EVENT_FIELDS, "billing event", exact=True)
    if event["schema_version"] != "billing-event/v1":
        raise LedgerError("Unsupported billing event schema_version.")
    for name in EVENT_FIELDS - {"schema_version", "source_sha256", "currency", "billable_subtotal"}:
        token(event[name], name)
    if event["agency_alias"] != agency:
        raise LedgerError("Event agency does not match ledger agency.")
    if not isinstance(event["currency"], str) or event["currency"] not in SUPPORTED_CURRENCIES:
        raise LedgerError("Event currency must be a supported two-decimal currency.")
    errors = []
    subtotal = money(event["billable_subtotal"], "billable_subtotal", errors)
    if errors or subtotal is None or subtotal <= 0:
        raise LedgerError("billable_subtotal must be positive, bounded, two-decimal money.")
    expected = hash_value(event["source_sha256"], "source_sha256")
    hasher = hashlib.sha256()
    with source.open("rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            hasher.update(block)
    if hasher.hexdigest() != expected:
        raise LedgerError("Source file SHA256 does not match the event.")
    return dict(event, billable_subtotal=format(subtotal, ".2f"))


def now():
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def connect(path: Path, agency: str, *, write=False):
    token(agency, "agency")
    db = sqlite3.connect(path.resolve().as_uri() + "?mode=rw", uri=True, timeout=15, isolation_level=None)
    db.row_factory = sqlite3.Row
    try:
        db.execute("PRAGMA foreign_keys=ON")
        db.execute("BEGIN IMMEDIATE" if write else "BEGIN")
        if db.execute("PRAGMA user_version").fetchone()[0] != VERSION:
            raise LedgerError("Unsupported database format version.")
        metadata = dict(db.execute("SELECT key, value FROM metadata"))
        if metadata != {"format": "billing-review/v1", "agency_alias": agency}:
            raise LedgerError("Ledger agency or format metadata does not match.")
        yield db
        db.commit()
    except BaseException:
        db.rollback()
        raise
    finally:
        db.close()


def initialize(path: Path, agency: str):
    token(agency, "agency")
    try:
        descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        with connect(path, agency):
            return {"state": "LOCAL_LEDGER_READY", "agency_alias": agency, "created": False, "authenticated": False, "external_send_allowed": False}
    os.close(descriptor)
    db = sqlite3.connect(path, isolation_level=None)
    try:
        db.executescript("""
        BEGIN IMMEDIATE;
        PRAGMA user_version=1;
        CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        CREATE TABLE events (event_id TEXT PRIMARY KEY, event_json TEXT NOT NULL, created_at TEXT NOT NULL);
        CREATE TABLE invoices (invoice_number TEXT PRIMARY KEY, event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id), current_revision TEXT);
        CREATE TABLE revisions (
            revision_id TEXT PRIMARY KEY,
            invoice_number TEXT NOT NULL REFERENCES invoices(invoice_number),
            event_id TEXT NOT NULL REFERENCES events(event_id),
            receipt_json TEXT NOT NULL, receipt_sha256 TEXT NOT NULL UNIQUE,
            content_fingerprint TEXT NOT NULL, artifact BLOB NOT NULL,
            created_at TEXT NOT NULL, reviewer_alias TEXT,
            review_reference TEXT, reviewed_at TEXT);
        """)
        db.executemany("INSERT INTO metadata VALUES (?, ?)", [("format", "billing-review/v1"), ("agency_alias", agency)])
        db.commit()
    except Exception as exc:
        db.rollback()
        raise LedgerError(f"Initialization failed; the incomplete local ledger at {path} was retained for operator inspection/recovery: {exc}") from exc
    finally:
        db.close()
    return {"state": "LOCAL_LEDGER_READY", "agency_alias": agency, "created": True, "authenticated": False, "external_send_allowed": False}


def record_event(path: Path, agency: str, event, source: Path):
    event = validate_event(event, agency, source)
    text = canonical(event)
    with connect(path, agency, write=True) as db:
        prior = db.execute("SELECT event_json FROM events WHERE event_id=?", (event["event_id"],)).fetchone()
        if prior and prior[0] != text:
            raise LedgerError("Immutable event ID already exists with different content.")
        if not prior:
            db.execute("INSERT INTO events VALUES (?, ?, ?)", (event["event_id"], text, now()))
    return {"state": "LOCAL_EVENT_RECORDED", "event_id": event["event_id"], "event_sha256": digest(text.encode()), "created": not bool(prior), "source_review_verified": False, "authenticated": False, "external_send_allowed": False}


def receipt_content(event, record, artifact: bytes):
    invoice = record["invoice"]
    if record["engagement_id"] != event["engagement_id"]:
        raise LedgerError("Invoice engagement does not match the billable event.")
    if invoice["currency"] != event["currency"] or Decimal(str(invoice["subtotal"])) != Decimal(event["billable_subtotal"]):
        raise LedgerError("Invoice currency/subtotal must match the entire billable event.")
    return {
        "schema_version": "billing-review-receipt/v1", "agency_alias": event["agency_alias"],
        "event_id": event["event_id"], "event_sha256": digest(canonical(event).encode()),
        "source_sha256": event["source_sha256"], "engagement_id": record["engagement_id"],
        "engagement_sha256": digest(canonical(record).encode()), "artifact_sha256": digest(artifact),
        "invoice_number": invoice["invoice_number"], "recipient": record["client"]["billing_email"],
        "finance_destination_reference": event["finance_destination_reference"],
        "payment_details_reference": invoice["payment_details_reference"],
        "policy_version": event["policy_version"],
    }


def summary(row):
    return {
        "revision_id": row["revision_id"], "invoice_number": row["invoice_number"], "event_id": row["event_id"],
        "receipt_sha256": row["receipt_sha256"], "receipt": decode(row["receipt_json"]),
        "state": "LOCAL_REVIEW_ACKNOWLEDGED" if row["reviewed_at"] else "HUMAN_REVIEW_REQUIRED",
        "reviewer_alias": row["reviewer_alias"], "review_reference": row["review_reference"],
        "reviewed_at": row["reviewed_at"], "authenticated": False, "external_send_allowed": False,
    }


def prepare(path: Path, agency: str, event_id: str, record):
    token(event_id, "event_id")
    artifact = validate_record(record)
    number = record["invoice"]["invoice_number"]
    with connect(path, agency, write=True) as db:
        event_row = db.execute("SELECT event_json FROM events WHERE event_id=?", (event_id,)).fetchone()
        if not event_row:
            raise LedgerError("Billable event has not been recorded.")
        event = decode(event_row[0])
        content = receipt_content(event, record, artifact)
        fingerprint = digest(canonical(content).encode())
        reservation = db.execute("SELECT * FROM invoices WHERE event_id=? OR invoice_number=?", (event_id, number)).fetchall()
        if reservation and (len(reservation) != 1 or reservation[0]["event_id"] != event_id or reservation[0]["invoice_number"] != number):
            raise LedgerError("Invoice number or event is already reserved; no second invoice or renumbering is supported.")
        if reservation:
            current = db.execute("SELECT * FROM revisions WHERE revision_id=?", (reservation[0]["current_revision"],)).fetchone()
            if current and current["content_fingerprint"] == fingerprint:
                return dict(summary(current), created=False)
        else:
            db.execute("INSERT INTO invoices VALUES (?, ?, NULL)", (number, event_id))
        revision = str(uuid.uuid4())
        receipt = canonical(dict(content, revision_id=revision))
        db.execute("INSERT INTO revisions (revision_id, invoice_number, event_id, receipt_json, receipt_sha256, content_fingerprint, artifact, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (revision, number, event_id, receipt, digest(receipt.encode()), fingerprint, artifact, now()))
        db.execute("UPDATE invoices SET current_revision=? WHERE invoice_number=?", (revision, number))
        row = db.execute("SELECT * FROM revisions WHERE revision_id=?", (revision,)).fetchone()
        return dict(summary(row), created=True)


def current_revision(db, revision: str, expected_receipt: str):
    token(revision, "revision")
    hash_value(expected_receipt, "receipt")
    row = db.execute("SELECT r.* FROM revisions r JOIN invoices i ON i.current_revision=r.revision_id WHERE r.revision_id=?", (revision,)).fetchone()
    if not row:
        raise LedgerError("Revision is missing or superseded; prepare/review the current revision.")
    if row["receipt_sha256"] != expected_receipt or digest(row["receipt_json"].encode()) != expected_receipt:
        raise LedgerError("Expected receipt SHA256 does not match the current revision.")
    receipt = decode(row["receipt_json"])
    if receipt["revision_id"] != revision or digest(bytes(row["artifact"])) != receipt["artifact_sha256"]:
        raise LedgerError("Stored revision content does not match its receipt.")
    return row


def verify_inputs(db, revision, expected_receipt, record, artifact):
    rendered = validate_record(record)
    row = current_revision(db, revision, expected_receipt)
    event = decode(db.execute("SELECT event_json FROM events WHERE event_id=?", (row["event_id"],)).fetchone()[0])
    expected = canonical(dict(receipt_content(event, record, rendered), revision_id=revision))
    if expected != row["receipt_json"] or artifact != bytes(row["artifact"]):
        raise LedgerError("Current engagement or exported artifact differs from this revision; prepare and review again.")
    return row


def review(path: Path, agency: str, revision: str, expected_receipt: str, record, artifact: bytes, reviewer: str, review_reference: str):
    token(reviewer, "reviewer")
    token(review_reference, "review_reference")
    with connect(path, agency, write=True) as db:
        row = verify_inputs(db, revision, expected_receipt, record, artifact)
        if row["reviewed_at"] and (row["reviewer_alias"] != reviewer or row["review_reference"] != review_reference):
            raise LedgerError("This revision already has an immutable manual review acknowledgement.")
        if not row["reviewed_at"]:
            db.execute("UPDATE revisions SET reviewer_alias=?, review_reference=?, reviewed_at=? WHERE revision_id=?", (reviewer, review_reference, now(), revision))
        return summary(db.execute("SELECT * FROM revisions WHERE revision_id=?", (revision,)).fetchone())


def check(path: Path, agency: str, revision: str, expected_receipt: str, record, artifact: bytes):
    with connect(path, agency) as db:
        return summary(verify_inputs(db, revision, expected_receipt, record, artifact))


def export(path: Path, agency: str, revision: str, expected_receipt: str, out: Path):
    with connect(path, agency) as db:
        row = current_revision(db, revision, expected_receipt)
        artifact = bytes(row["artifact"])
    # Export is deliberately separate: a failed file write never discards a revision.
    try:
        descriptor = os.open(out, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(artifact)
    except FileExistsError:
        if out.is_symlink() or not out.is_file() or out.read_bytes() != artifact:
            raise LedgerError("Export destination exists with different content; choose a new file.") from None
    return dict(summary(row), exported_path=str(out), artifact_sha256=digest(artifact))


def status(path: Path, agency: str, event_id: str | None = None):
    if event_id is not None:
        token(event_id, "event_id")
    with connect(path, agency) as db:
        query = "SELECT r.*, i.current_revision FROM revisions r JOIN invoices i ON i.invoice_number=r.invoice_number"
        rows = db.execute(query + (" WHERE r.event_id=?" if event_id else "") + " ORDER BY r.created_at, r.revision_id", (event_id,) if event_id else ()).fetchall()
        return {"agency_alias": agency, "format": "billing-review/v1", "revisions": [dict(summary(row), current=row["revision_id"] == row["current_revision"]) for row in rows], "authenticated": False, "external_send_allowed": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("init", "record-event", "prepare", "export", "review", "check", "status"):
        child = commands.add_parser(command)
        child.add_argument("--ledger", type=Path, required=True)
        child.add_argument("--agency", required=True)
        if command == "record-event":
            child.add_argument("--event", type=Path, required=True)
            child.add_argument("--source", type=Path, required=True)
        if command in {"prepare", "status"}:
            child.add_argument("--event-id", required=command == "prepare")
        if command in {"prepare", "review", "check"}:
            child.add_argument("--record", type=Path, required=True)
        if command in {"export", "review", "check"}:
            child.add_argument("--revision", required=True)
            child.add_argument("--receipt", required=True)
        if command in {"review", "check"}:
            child.add_argument("--artifact", type=Path, required=True)
        if command == "export":
            child.add_argument("--out", type=Path, required=True)
        if command == "review":
            child.add_argument("--reviewer", required=True)
            child.add_argument("--review-reference", required=True)
    args = parser.parse_args()
    try:
        token(args.agency, "agency")
        record = read_json(args.record) if hasattr(args, "record") else None
        if args.command == "init":
            result = initialize(args.ledger, args.agency)
        elif args.command == "record-event":
            result = record_event(args.ledger, args.agency, read_json(args.event), args.source)
        elif args.command == "prepare":
            result = prepare(args.ledger, args.agency, args.event_id, record)
        elif args.command == "export":
            result = export(args.ledger, args.agency, args.revision, args.receipt, args.out)
        elif args.command in {"review", "check"}:
            common = (args.ledger, args.agency, args.revision, args.receipt, record, args.artifact.read_bytes())
            result = review(*common, args.reviewer, args.review_reference) if args.command == "review" else check(*common)
        else:
            result = status(args.ledger, args.agency, args.event_id)
        print(canonical(result))
        return 0
    except (ValueError, OSError, sqlite3.Error, RecursionError) as exc:
        print(json.dumps({"error": str(exc), "authenticated": False, "external_send_allowed": False}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
