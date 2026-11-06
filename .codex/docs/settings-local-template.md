# Personal settings

Use gitignored `project.local.yaml` for supported personal studio workflow values:

```yaml
modes:
  automation: guided
  review_mode: solo
```

Use your Codex client/user configuration for model, permissions, and MCP settings.
There is no studio settings-local JSON or automatic `AGENTS.local.md` import.
Project `.codex/config.toml` is shared configuration; never commit credentials.
The `$settings --local` workflow edits studio preferences, not host permissions.
