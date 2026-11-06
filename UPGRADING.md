# Upgrading Codex Game Studios

This is the first Codex port (0.1.0). Upstream CCGS version numbers are independent.
Back up your project and review the diff before replacing framework files.
Preserve your `project.yaml`, `project.local.yaml`, game code, assets, design docs,
and production records. Merge existing `AGENTS.md` and `.codex/config.toml` manually.
Never replace a project's config or agent instructions without reviewing the changes.
After updating, run `python tools/studio.py check` and `python tools/studio.py doctor`,
then review changed hooks in Codex with `/hooks`. Do not bypass hook trust.
See `UPSTREAM.md` for the source baseline and `docs/CODEX-PORT.md` for differences.
