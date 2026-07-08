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
        return '<p class="empty">None listed.</p>'
    body = "\n".join(f"          <li>{esc(item)}</li>" for item in items)
    return f'<ul class="check-list">\n{body}\n        </ul>'


def render_screen_html(data: dict[str, object]) -> str:
    review = "Required" if data["human_review_required"] else "Not required by this screen"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(data["title"])} - AI Workflow Safety Screen</title>
  <style>
    :root {{ color-scheme: dark; --ink: #f7ead7; --muted: #d7c2a2; --paper: #fff7e8; --paper-ink: #261b12; --line: #6f5840; --accent: #f2b66d; --warn: #ffd08a; }}
    * {{ box-sizing: border-box; }}
    body {{ color: var(--ink); font-family: Georgia, "Times New Roman", serif; line-height: 1.6; margin: 0; background: #20150f; }}
    body::before {{ content: ""; position: fixed; inset: 0; pointer-events: none; background: radial-gradient(circle at top left, rgba(242, 182, 109, 0.16), transparent 34rem); }}
    .page {{ max-width: 1080px; margin: 0 auto; padding: 32px 18px 44px; position: relative; }}
    header {{ border: 1px solid var(--line); border-radius: 8px; margin-bottom: 18px; padding: 24px; background: linear-gradient(135deg, #3a2617, #251810); box-shadow: 0 18px 50px rgba(0,0,0,0.25); }}
    h1 {{ color: var(--ink); font-size: clamp(2rem, 5vw, 4rem); line-height: 0.98; margin: 10px 0 14px; letter-spacing: 0; }}
    h2 {{ color: var(--paper-ink); font-size: 1.02rem; line-height: 1.2; margin: 0 0 10px; }}
    p {{ margin: 0; }}
    section, .meta-card {{ background: var(--paper); border: 1px solid #dfcaa8; border-radius: 8px; color: var(--paper-ink); padding: 18px; }}
    .eyebrow {{ color: var(--accent); font-family: Arial, Helvetica, sans-serif; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }}
    .chips {{ display: flex; flex-wrap: wrap; gap: 8px; }}
    .chip, .review {{ border: 1px solid rgba(255,255,255,0.28); border-radius: 999px; color: var(--ink); display: inline-flex; font-family: Arial, Helvetica, sans-serif; font-size: 0.78rem; font-weight: 700; padding: 6px 10px; }}
    .review {{ background: rgba(255, 208, 138, 0.18); color: #ffe2ac; }}
    .chip {{ background: rgba(255,255,255,0.08); }}
    .meta-grid {{ display: grid; gap: 12px; grid-template-columns: repeat(2, minmax(0, 1fr)); margin: 18px 0; }}
    .meta-card dt {{ color: #735230; font-family: Arial, Helvetica, sans-serif; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; }}
    .meta-card dd {{ margin: 4px 0 0; font-weight: 700; }}
    main {{ display: grid; gap: 14px; grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    main section.wide {{ grid-column: 1 / -1; }}
    .check-list {{ margin: 0; padding-left: 1.2rem; }}
    .check-list li {{ margin: 0.45rem 0; padding-left: 0.15rem; }}
    .boundary {{ background: #302117; border-color: var(--line); color: var(--ink); }}
    .boundary h2 {{ color: var(--accent); }}
    .empty {{ color: #7a6a55; font-style: italic; }}
    footer {{ color: var(--muted); font-family: Arial, Helvetica, sans-serif; font-size: 0.9rem; margin-top: 18px; }}
    @media (max-width: 760px) {{ .meta-grid, main {{ grid-template-columns: 1fr; }} header {{ padding: 20px; }} }}
    @media print {{ body {{ background: #fff; color: #000; }} body::before {{ display: none; }} .page {{ max-width: none; padding: 0; }} header, section, .meta-card {{ box-shadow: none; break-inside: avoid; }} .boundary {{ color: #000; background: #fff; }} }}
  </style>
</head>
<body>
  <div class="page">
    <header>
      <p class="eyebrow">Hypernovelty Open Lab / AI Workflow Safety Screen</p>
      <h1>{esc(data["title"])}</h1>
      <div class="chips" aria-label="Screen status">
        <span class="review">Human review: {esc(review)}</span>
        <span class="chip">Synthetic example</span>
        <span class="chip">Local review aid</span>
      </div>
    </header>

    <dl class="meta-grid" aria-label="Screen metadata">
      <div class="meta-card"><dt>Screen ID</dt><dd>{esc(data["screen_id"])}</dd></div>
      <div class="meta-card"><dt>Date</dt><dd>{esc(data["date"])}</dd></div>
    </dl>

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

    <section class="wide">
      <h2>Notes</h2>
      <p>{esc(data["notes"])}</p>
    </section>

    <section class="boundary wide">
      <h2>Boundary</h2>
      <p>This screen is a local synthetic review aid only. It is not legal, compliance, procurement, cybersecurity, medical, financial, employment, or production approval advice, and it does not approve deployment.</p>
    </section>
  </main>
  <footer>Rendered without external assets, tracking, or network calls.</footer>
  </div>
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
