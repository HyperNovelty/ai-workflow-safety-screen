#!/usr/bin/env python3
from __future__ import annotations

import html
import sys
from pathlib import Path

try:
    from validate_screen import load_screen, validate_screen
except ModuleNotFoundError:
    from scripts.validate_screen import load_screen, validate_screen


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def render_list(items: list[str]) -> str:
    if not items:
        return "<p>None listed.</p>"
    body = "\n".join(f"          <li>{esc(item)}</li>" for item in items)
    return f"<ul>\n{body}\n        </ul>"


def render_screen_html(data: dict[str, object]) -> str:
    review = "Required" if data["human_review_required"] else "Not required by this screen"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(data["title"])} - AI Workflow Safety Screen</title>
  <style>
    body {{ font-family: Arial, Helvetica, sans-serif; line-height: 1.55; margin: 2rem auto; max-width: 980px; padding: 0 1rem; color: #1f2933; }}
    header {{ border-bottom: 1px solid #d8dee6; margin-bottom: 1.5rem; padding-bottom: 1rem; }}
    h1, h2 {{ line-height: 1.2; }}
    section {{ margin: 1.25rem 0; }}
    .meta {{ color: #52616f; }}
    .review {{ display: inline-block; border: 1px solid #8a4b08; background: #fff5e6; color: #4a2a04; padding: 0.35rem 0.55rem; border-radius: 4px; font-weight: bold; }}
    .boundary {{ border-left: 4px solid #52616f; background: #f4f7fa; padding: 0.8rem 1rem; }}
  </style>
</head>
<body>
  <header>
    <h1>{esc(data["title"])}</h1>
    <p class="meta">Screen ID: {esc(data["screen_id"])} | Date: {esc(data["date"])}</p>
    <p><span class="review">Human review: {esc(review)}</span></p>
  </header>

  <main>
    <section>
      <h2>Team Context</h2>
      <p>{esc(data["team_context"])}</p>
    </section>

    <section>
      <h2>Workflow Summary</h2>
      <p>{esc(data["workflow_summary"])}</p>
    </section>

    <section>
      <h2>AI Use Case</h2>
      <p>{esc(data["ai_use_case"])}</p>
    </section>

    <section>
      <h2>Risk Flags</h2>
      {render_list(data["risk_flags"])}
    </section>

    <section>
      <h2>Recommended Controls</h2>
      {render_list(data["recommended_controls"])}
    </section>

    <section>
      <h2>Not For</h2>
      {render_list(data["not_for"])}
    </section>

    <section>
      <h2>Notes</h2>
      <p>{esc(data["notes"])}</p>
    </section>

    <section class="boundary">
      <h2>Boundary</h2>
      <p>This screen is not legal, compliance, procurement, cybersecurity, medical, financial, employment, or production approval advice. It is a local review aid only.</p>
    </section>
  </main>
</body>
</html>
"""


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: render_screen_html.py SCREEN_JSON OUTPUT_HTML", file=sys.stderr)
        return 2

    try:
        data = load_screen(argv[1])
        errors = validate_screen(data)
        if errors:
            for error in errors:
                print(f"error: {error}", file=sys.stderr)
            return 1
        output = Path(argv[2])
        output.write_text(render_screen_html(data), encoding="utf-8")
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"wrote: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
