# Config Resolution

## Explicit execution

Run this command from the project root when a skill requests effective settings:

```bash
bash .codex/hooks/yaml-helper.sh resolve_config --keys automation,workflow,qa.level
```

Read the actual output. Codex does not preprocess Markdown commands or replace
them with stdout. Shell authorization comes from the host, never skill YAML.
For system-specific overrides, pass the system name as documented by the helper.

## Settings sources

The inherited resolver combines `project.yaml`, the supported personal overrides
in `project.local.yaml`, rigor expansion, and documented defaults. See
`effects-map.md` by relevant section for the complete setting behavior.
The six individual knobs can override the rigor preset; do not seed all six in
a fresh project because doing so shadows preset changes.
Native Codex settings live separately in `.codex/config.toml` or user config.

## Missing dependencies

Python 3 and Bash must work in the same environment. Run the doctor first.
If the resolver fails, report that settings were not resolved. Do not silently
present defaults as the user's choices. A skill may use explicitly documented
defaults only after stating that fallback and checking it fits the task.
