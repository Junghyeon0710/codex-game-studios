# Codex port: compatibility and validation

## Source baseline

Upstream v1.2.0, commit `05ad7c8a5b8aa2aa86bbd3439ae7cf7295cac418`.
All 49 role briefs and 74 skill folders are retained. `.codex/port-manifest.json`
is the exact inventory. Original structure, document templates, and workflow
categories are preserved; runtime integration is adapted, not mechanically renamed.

| Upstream mechanism | Codex equivalent / limitation |
|---|---|
| CLAUDE.md | AGENTS.md, explicit references rather than @ imports |
| Agent Markdown + Claude model aliases | Editable role Markdown + generated native TOML; inherit model |
| Slash workflow commands | `$skill-name` and normal skill selection |
| Dynamic shell prelude | Explicit command execution at skill start |
| Read / Write / Edit / Glob / Grep | Available host file tools and shell; names in prose are operations |
| AskUserQuestion | Available question tool, otherwise a plain-text question |
| Agent tool | Native subagents; custom role or explicit role brief fallback |
| Path-scoped rule injection | Explicit rule lookup plus patch-hook reminders |
| hooks.json permissions | Host-managed Codex permissions; no copied deny-list claims |
| Hook payloads | Python adapter normalizes supported shell and patch events |
| Read hook / InstructionsLoaded | Manual helper / unwired diagnostic |
| Status line | Not ported; `$sprint-status` and checkpoint files remain |
| Experimental Agent Teams | Native subagents; no experimental environment switch |

## Supported dependencies

Python >=3.11, PyYAML >=6,<7, Bash, Git, and a current local Codex client.
Native agent and hook schemas follow official documentation reviewed 2026-11-06.
The local CLI version inspected during development was 0.146.0; version inspection
is not a claim of end-to-end skill execution. Clients without native hooks can
use skills and manual checks, but automatic checks must be described as unavailable.

A read-only CLI smoke run selected the project `$help` skill, inspected the
template, identified the Concept stage, and recommended `$start`. Its Bash
helper was blocked by the host's read-only command policy, and it reported that
configuration remained unverified. The helper itself is exercised by the direct
contract tests. This smoke run does not validate delegation or trusted hook loading.

## Validation layers

`python tools/studio.py check` checks all skills, generated TOML, hook config,
inventory, and copyright. `python -m unittest discover -s tests -v` checks patch
translation, denial propagation, actual post-write content, rule matching,
configuration resolution, and full skill enumeration. CI runs on Windows,
Ubuntu, and macOS; consult the workflow run for current results.

These tests do not invoke Codex or a game engine. The 123 inherited behavioral
specifications in `studio-tests/` are review specifications, not recorded runtime
passes. No end-to-end Codex game-generation benchmark or Unity/Unreal/Godot
playtest is claimed for this initial port. Engine reference documents retain their
upstream provenance and must be checked against the installed engine.

## Known limitations

- Hook trust and project trust are host-controlled and must be reviewed by users.
- Exact-context patch normalization may report NOT VERIFIED for fuzzy/ambiguous
  edits that the editor accepts. This is visible, not a silent pass.
- Shell writes, MCP/editor writes, and reads do not all pass through patch guards.
- A reviewer role is a behavioral boundary, not an independent sandbox.
- Shared editor and checkpoint writes require serialized coordination.
- Upstream template QA modes and formulas remain project choices, not evidence.

See `UPSTREAM.md` and `LICENSE` for attribution.
