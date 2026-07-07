# AI Workflow Safety Screen

A local-only screening kit for teams deciding whether an AI-assisted workflow should require human review before use.

This repository is a public candidate carved from ideas in a local AI Workflow Safety Engine prototype. It is intentionally reduced: one plain JSON screen format, one synthetic example, one validator, one HTML renderer, and short field guidance.

## What It Is

The safety screen is a lightweight intake artifact for proposed AI workflow use. It asks a team to describe the workflow, name risk flags, state whether human review is required, and record recommended controls before the workflow is piloted or reused.

It helps small teams, service teams, nonprofits, civic groups, learning programs, and internal operators slow down before AI output reaches customers, staff, public channels, regulated contexts, or security-sensitive decisions.

## What It Does

- Provides a public-safe JSON schema for a workflow safety screen.
- Validates required fields and basic field types.
- Requires `human_review_required: true` when high-consequence risk flags are present.
- Renders a Windows-openable HTML review page using Python standard library only.
- Includes a synthetic service-team example with no customer, account, credential, or private data.

## What It Does Not Do

This kit is not legal advice, compliance advice, procurement advice, cybersecurity advice, medical advice, financial advice, insurance advice, employment advice, or a substitute for qualified review.

It is not an approval mechanism. A passing validation result only means the JSON file follows this screen format and the built-in human-review rule. It does not mean a workflow is safe, lawful, compliant, accurate, secure, or ready for production.

Do not use this repository to capture sensitive data. Keep screens synthetic, redacted, or public-safe. Do not put customer records, employee records, credentials, incident details, health information, financial records, legal matter details, or account data into examples.

The scripts do not call external APIs, deploy services, phone home, or require network access.

## Quick Start

Validate the example:

```bash
python3 scripts/validate_screen.py examples/service-team-workflow-screen.example.json
```

Render the example to a local HTML file:

```bash
python3 scripts/render_screen_html.py examples/service-team-workflow-screen.example.json /tmp/ai-workflow-safety-screen-example.html
```

Run tests:

```bash
python3 -m unittest discover -s tests
```

## Human Review Rule

If `risk_flags` contains any of these values, `human_review_required` must be `true`:

- `customer_data`
- `payment`
- `legal`
- `medical`
- `employment`
- `public_posting`
- `security`

Teams may still require human review for other reasons. This rule is a floor, not a full risk model.

## Files

- `schemas/workflow-safety-screen.schema.json` describes the screen shape.
- `examples/service-team-workflow-screen.example.json` is a synthetic example.
- `scripts/validate_screen.py` validates a screen file.
- `scripts/render_screen_html.py` renders a local review page.
- `docs/field-guide.md` explains the fields and suggested review posture.
- `docs/public-safety-boundary.md` lists public-release boundaries.

## Provenance

This public candidate is inspired by a local AWSE prototype, but it is not a copy of the full prototype. It excludes local dashboards, product-package exports, build artifacts, private candidate data, caches, virtual environments, account tooling, and prototype internals. The included example is synthetic and reduced for public-good educational use.
