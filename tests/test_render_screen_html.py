from __future__ import annotations

import unittest

from scripts.render_screen_html import render_screen_html


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


class RenderScreenHtmlTests(unittest.TestCase):
    def test_render_includes_escaped_content(self) -> None:
        screen = valid_screen()
        screen["title"] = "Example <unsafe>"
        screen["notes"] = "Use <script>alert('x')</script> nowhere."
        output = render_screen_html(screen)
        self.assertIn("Example &lt;unsafe&gt;", output)
        self.assertIn("&lt;script&gt;alert(&#x27;x&#x27;)&lt;/script&gt;", output)
        self.assertNotIn("<script>alert", output)

    def test_render_shows_human_review_required(self) -> None:
        output = render_screen_html(valid_screen())
        self.assertIn("Human review: Required", output)
        self.assertIn("Human review before send.", output)


if __name__ == "__main__":
    unittest.main()
