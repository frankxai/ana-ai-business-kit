#!/usr/bin/env python3
"""Dependency-free tests for Ana render document utilities."""

from __future__ import annotations

from render_documents import bullets, line_items, context

def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)

# Test bullets
require(bullets(["item 1", "item 2"]) == "- item 1\n- item 2", "bullets must format lists correctly.")
require(bullets([]) == "- [Complete before approval]", "Empty bullets must return placeholder.")
require(bullets(None) == "- [Complete before approval]", "None bullets must return placeholder.")

# Test line_items
items = [
    {"description": "Consulting", "quantity": 10, "unit_price": 100.5, "amount": 1005.0},
    {"description": "Travel", "quantity": 1, "unit_price": 200.0, "amount": 200.0},
]
rendered_items = line_items(items, "USD")
require("| Description | Quantity | Unit price | Amount |" in rendered_items, "line_items must include header.")
require("| Consulting | 10 | USD 100.50 | USD 1005.00 |" in rendered_items, "line_items must format first row currency correctly.")
require("| Travel | 1 | USD 200.00 | USD 200.00 |" in rendered_items, "line_items must format second row currency correctly.")

# Test context with empty record to verify placeholders
empty_record = {
    "engagement_id": "ENG-001",
    "client": {
        "legal_name": "Test Client",
        "contact_name": "Test Contact"
    },
    "kickoff": {
        "company_context": "Test Context"
    }
}

ctx = context(empty_record)

require(ctx["engagement_id"] == "ENG-001", "Context must preserve engagement_id.")
require(ctx["client_name"] == "Test Client", "Context must preserve client legal_name.")
require(ctx["contact_name"] == "Test Contact", "Context must preserve client contact_name.")
require(ctx["company_context"] == "Test Context", "Context must preserve kickoff company_context.")
require(ctx["billing_name"] == "[Billing name]", "Context must apply placeholder for missing billing_name.")
require(ctx["currency"] == "EUR", "Context must default currency to EUR.")
require(ctx["offer_subtotal"] == "0.00", "Context must format missing money amounts as 0.00.")
require(ctx["kickoff_outcomes"] == "- [Complete before approval]", "Context must apply bullets placeholder for missing lists.")

print("Ana Render Documents utility tests passed.")
