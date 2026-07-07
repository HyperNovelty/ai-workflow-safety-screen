from __future__ import annotations

import unittest

from scripts.validate_screen import validate_screen


def valid_screen() -> dict[str, object]:
    return {
        "screen_id": "example_v1",
        "title": "Example",
        "date": "2026-07-06",
        "team_context": "Synthetic team context.",
        "workflow_summary": "Synthetic workflow summary.",
        "ai_use_case": "Synthetic AI use case.",
        "risk_flags": ["customer_data"],
        "human_review_required": True,
        "recommended_controls": ["Human review before send."],
        "not_for": ["Autonomous send."],
        "notes": "Synthetic notes.",
    }


class ValidateScreenTests(unittest.TestCase):
    def test_valid_screen_passes(self) -> None:
        self.assertEqual(validate_screen(valid_screen()), [])

    def test_required_human_review_flag_enforced(self) -> None:
        screen = valid_screen()
        screen["human_review_required"] = False
        errors = validate_screen(screen)
        self.assertTrue(any("human_review_required must be true" in item for item in errors))

    def test_array_items_must_be_strings(self) -> None:
        screen = valid_screen()
        screen["recommended_controls"] = ["ok", 42]
        errors = validate_screen(screen)
        self.assertIn("recommended_controls[1] must be a string", errors)

    def test_unexpected_field_fails(self) -> None:
        screen = valid_screen()
        screen["private_path"] = "/home/example/private"
        errors = validate_screen(screen)
        self.assertIn("unexpected field: private_path", errors)


if __name__ == "__main__":
    unittest.main()
