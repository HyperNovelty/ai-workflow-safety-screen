#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = (
    "screen_id",
    "title",
    "date",
    "team_context",
    "workflow_summary",
    "ai_use_case",
    "risk_flags",
    "human_review_required",
    "recommended_controls",
    "not_for",
    "notes",
)

STRING_FIELDS = (
    "screen_id",
    "title",
    "date",
    "team_context",
    "workflow_summary",
    "ai_use_case",
    "notes",
)

ARRAY_FIELDS = ("risk_flags", "recommended_controls", "not_for")

HUMAN_REVIEW_FLAGS = {
    "customer_data",
    "payment",
    "legal",
    "medical",
    "employment",
    "public_posting",
    "security",
}


def load_screen(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("screen must be a JSON object")
    return data


def validate_screen(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"missing required field: {field}")

    extra_fields = sorted(set(data) - set(REQUIRED_FIELDS))
    for field in extra_fields:
        errors.append(f"unexpected field: {field}")

    for field in STRING_FIELDS:
        if field in data and not isinstance(data[field], str):
            errors.append(f"{field} must be a string")

    for field in ARRAY_FIELDS:
        if field not in data:
            continue
        value = data[field]
        if not isinstance(value, list):
            errors.append(f"{field} must be an array of strings")
            continue
        for index, item in enumerate(value):
            if not isinstance(item, str):
                errors.append(f"{field}[{index}] must be a string")

    if "human_review_required" in data and not isinstance(data["human_review_required"], bool):
        errors.append("human_review_required must be a boolean")

    risk_flags = data.get("risk_flags")
    if isinstance(risk_flags, list):
        matched_flags = HUMAN_REVIEW_FLAGS.intersection(risk_flags)
        if matched_flags and data.get("human_review_required") is not True:
            joined = ", ".join(sorted(matched_flags))
            errors.append(
                "human_review_required must be true when risk_flags include: "
                f"{joined}"
            )

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_screen.py SCREEN_JSON", file=sys.stderr)
        return 2

    try:
        data = load_screen(argv[1])
        errors = validate_screen(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"ok: {argv[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
