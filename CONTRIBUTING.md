# Contributing

Contributions should keep this project small, local-first, and public-safe.

## Guidelines

- Use synthetic examples only.
- Do not add external API calls, telemetry, account integrations, deployment flows, or network requirements.
- Do not add dependencies to the validation or rendering scripts.
- Do not include private WSL paths, local build artifacts, virtual environments, caches, dashboard internals, candidate records, customer data, credentials, or generated product-package exports.
- Keep copy sober, practical, and public-good oriented.
- Add or update tests when changing validation or rendering behavior.

## Local Checks

Run:

```bash
python3 scripts/validate_screen.py examples/service-team-workflow-screen.example.json
python3 scripts/render_screen_html.py examples/service-team-workflow-screen.example.json /tmp/ai-workflow-safety-screen-example.html
python3 -m unittest discover -s tests
git diff --check
```
