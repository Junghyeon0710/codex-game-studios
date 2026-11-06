# Setup Requirements

## Required

- A current local Codex client with repository skills. For native custom roles and
  lifecycle hooks, use a client supporting the schemas linked in `codex-runtime.md`.
- Git; Bash (Git for Windows includes it); Python 3.11 or newer.
- `python -m pip install -r requirements-dev.txt` for source validation and rule lookup.
- The chosen game engine and its build tools, installed separately.

Install Codex using the official instructions: https://learn.chatgpt.com/docs/cli.
If using the npm distribution, the package is `@openai/codex`.
Start at the directory containing `AGENTS.md` and `project.yaml`.
Run `python tools/studio.py doctor`, then `python tools/studio.py check`.
In the Codex host, review and trust the project and its hook definitions with
`/hooks` where supported. Restart after configuration changes if needed.

## Windows

Put Git's Bash and Python on PATH. `command_windows` selects the Python launcher
for hooks. Run the same doctor in the terminal/environment that launches Codex.
Engine launches through Bash need the path-conversion precautions documented in
`run-and-observe.md`. Do not assume WSL can launch a native editor correctly.

## Permissions and capabilities

This template inherits host permissions. It does not disable approval, install
global credentials, or auto-trust hooks. Project settings cannot bypass the host.
Missing hooks or editor integrations reduce available automation; state that
limitation and use the documented manual helper/check when possible.
