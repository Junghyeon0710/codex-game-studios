# Codex runtime contract

Read this once when starting a studio skill or specialist role. This document
defines the port's runtime behavior and takes precedence over inherited runtime
examples. Current user instructions and host policies always take precedence.

## Skills and tools

- Invoke a skill as `$name` or select it in the host. Slash-prefixed engine paths
  are paths; they are not skill invocations.
- Run configuration commands shown at the beginning of a skill explicitly.
  Codex does not execute Markdown command fences or inject their output for you.
- Interpret Read/Glob/Grep as file reading and search using available tools;
  prefer `rg`. Interpret Write/Edit as the host's file-editing tools, normally
  `apply_patch`. Those inherited operation names are not promised Codex tool IDs.
- `request_user_input` is available only in some modes. If absent, use the
  available asynchronous question tool or ask a concise plain-text question.
  Never invent a tool, treat a dismissed question as consent, or repeatedly ask
  for authorization the user already supplied.
- A code fence describing a helper is an instruction to run it when needed,
  not evidence it has run. Capture actual exit codes and outputs.

## Delegation

The studio's orchestration skills request delegation for independent work.
Use the host's native subagent mechanism and `.codex/agents/<role>.toml` where
custom roles are supported. The editable role briefs live in `.codex/roles/`;
run `python tools/studio.py generate` after editing them.
If custom types are unavailable, pass the role brief to a supported worker.
If delegation itself is unavailable, perform the phases sequentially and say so.
Subagents report questions to their parent. Collect results before dependent work,
verify claimed artifacts, and surface incomplete or failed work immediately.
Partition writable files; serialize changes to shared editor sessions and assets.
All agents inherit the parent model and permissions by default. Role prose does
not grant tools, bypass approval, or create a separate read-only sandbox.

## Settings and rules

`project.yaml` and optional `project.local.yaml` are studio workflow settings.
They are not native Codex configuration. Resolve with the documented Bash helper.
Native configuration is `.codex/config.toml`; hooks are `.codex/hooks.json`.
There is no Claude-style settings JSON, automatic `@file` import, dynamic skill
preprocessor, or studio status-line integration in this port.
Before editing, read matching `.codex/rules/*.md`; use
`python .codex/scripts/rules_for.py <relative-path> ...` to list matching rules.
Their YAML paths are references for our helper, not native Codex path-scoped rules.
Rules requiring tests are scoped by the effective `qa.level`; never silently
claim waived tests ran. Keep visual checks for observable changes.
The stage/checkpoint markers remain supported by helpers, but are not a status bar.

## Collaboration and evidence

Honor the resolved automation mode. Existing authorization covers necessary
implementation; do not turn every file edit into a new permission question.
Ask when a material design choice is unresolved or an action is outside scope.
Publication, pushes, destructive actions, and other external mutations require
the user's authorization; neither a role nor a workflow grants that itself.
Project modes cannot weaken the host's sandbox or approval settings.
Use the user's requested rigor; minimal is the upstream default.
Never mark implementation complete when an agent was interrupted or artifacts
are missing. A test file is not a passing test. A screenshot proves only what is
visible. Missing engine/tool access is NOT VERIFIED, not a pass.

## Hooks and limits

Start Codex at this template's root. Review/trust `.codex/hooks.json` in the host
before expecting automatic checks. Run `python tools/studio.py doctor` first.
`codex_adapter.py` translates supported shell and patch events to Bash checks.
Direct text patches to `.uasset`/`.umap` are blocked on that supported path.
Shell/editor/MCP writes are not universally intercepted by patch validators.
Whole-file read guarding remains an explicit helper: Codex shell reads do not
have a universal Read event. Hooks are guardrails, not an OS security boundary.
Missing dependencies, unrecognized patch forms, or failed helpers are reported
as NOT VERIFIED. Never describe these as successful checks.

## Official references

- https://learn.chatgpt.com/docs/build-skills
- https://learn.chatgpt.com/docs/agent-configuration/subagents
- https://learn.chatgpt.com/docs/agent-configuration/agents-md
- https://learn.chatgpt.com/docs/hooks

Port baseline reviewed 2026-11-06. Runtime availability varies by client/version;
see `docs/CODEX-PORT.md` for the scope of validation actually performed.
