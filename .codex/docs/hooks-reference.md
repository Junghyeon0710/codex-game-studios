# Hook reference

`.codex/hooks.json` connects Codex lifecycle events through `hooks/codex_adapter.py`.
Review and trust the definitions before use. The adapter emits valid event JSON,
never grants permission, and propagates an inherited pre-tool check's exit 2 as a
denial on supported tool paths.

| Codex event | Checks |
|---|---|
| SessionStart | Session orientation, checkpoint, project gaps |
| PostCompact | Restore checkpoint context |
| PreToolUse: Bash | Commit validation and push/release reminders |
| PreToolUse: apply_patch | Effective text-write and registry checks; binary-asset guard |
| PostToolUse: apply_patch | Actual data JSON and skill-change checks |
| PermissionRequest | Optional platform notification; no approval decision |
| PreCompact | Compaction record |
| Stop | Session log/checkpoint archival |
| SubagentStart / SubagentStop | Invocation/completion audit and artifact reminder |

The 18 inherited Bash files include 15 original event checks, two helpers, and
one diagnostic. The read-size guard remains a manual helper because shell reads
have no universal Read hook. The original InstructionsLoaded diagnostic is not
wired to Codex. No idle notification or custom status bar is provided.
The adapter runs checks in sequence and aggregates their messages; it does not
launch a duplicate original hook independently.

Write/registry/push checks are mainly advisory. Patch parsing covers ordinary
add/update/delete/move operations with exact, unambiguous context. Unsupported
forms report NOT VERIFIED. Shell and editor/MCP writes are not covered by the
patch validators. Hook checks are not a complete security boundary.
See https://learn.chatgpt.com/docs/hooks and `docs/CODEX-PORT.md`.
