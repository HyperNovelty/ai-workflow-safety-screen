# Field Guide

The AI Workflow Safety Screen is a short review artifact. It is designed to help a team decide whether a proposed AI-assisted workflow needs human review before use.

## Fields

- `screen_id`: Stable identifier for this screen.
- `title`: Plain-language name of the proposed workflow.
- `date`: Review date in `YYYY-MM-DD` form.
- `team_context`: Synthetic or public-safe description of the team and setting.
- `workflow_summary`: Short description of what happens in the workflow.
- `ai_use_case`: What the AI system is expected to do.
- `risk_flags`: Short labels for risks the team can recognize.
- `human_review_required`: Whether a named human review step is required before use.
- `recommended_controls`: Practical controls the team should apply before piloting.
- `not_for`: Explicitly excluded uses.
- `notes`: Additional public-safe review notes.

## Review Posture

Treat this screen as an early stop-and-think checkpoint. It is useful when a workflow is still being shaped, before a team normalizes AI output as part of operations.

The built-in validator requires human review when any of these flags appear:

- `customer_data`
- `payment`
- `legal`
- `medical`
- `employment`
- `public_posting`
- `security`

The absence of these flags does not prove low risk. Teams should still require human review when outputs affect people, money, access, rights, reputation, public communication, safety, security, or operational continuity.

## Recommended Controls

Controls should be concrete enough for a team to follow. Prefer statements such as "named human reviews final response before sending" over vague statements such as "be careful."

Useful controls often include:

- human review before external use,
- explicit escalation owner,
- source checking for factual claims,
- no autonomous send or publish,
- redaction of sensitive details,
- pilot stop conditions,
- review log or decision note.

## Good Example Boundaries

Examples should be synthetic, minimal, and public-safe. Do not include real customer conversations, employee cases, private documents, internal credentials, account identifiers, or sensitive incidents.
