# Codex Game Studios — Game Studio Agent Architecture

An independent Codex adaptation of Donchitos' MIT-licensed Claude Code Game Studios.
49 specialist roles and 74 workflows for Godot, Unity, and Unreal projects.
Read `.codex/docs/codex-runtime.md` before the first studio workflow in a session.

## Technology and project context

The game engine, language, version, naming conventions, performance budgets, and
workflow settings belong to `project.yaml`; personal workflow overrides belong
to gitignored `project.local.yaml`. Run `$start` for an unconfigured project.
Read `.codex/docs/directory-structure.md` and resolve the code root before edits.
Godot uses `src/`, Unity uses `Assets/`, and Unreal uses `Source/<Module>/` plus
project plugins. Existing projects may have different roots; inspect, don't guess.
Read the chosen engine's `docs/engine-reference/<engine>/VERSION.md` and verify
against the installed engine before relying on version-specific APIs. Bundled
references are inherited snapshots, not a promise that every claim is current.

## Coordination

Read `.codex/docs/coordination-rules.md` when delegating. Orchestration workflows
request native subagents for independent specialist work. Use the smallest team
that fits the task and the host's concurrency limit. Keep dependent work sequential.
Native agents are `.codex/agents/*.toml`; editable briefs are `.codex/roles/*.md`.
No global model pin is shipped: use the user's available model and account.
Never conceal a blocked subagent or accept an artifact that does not exist.

## Collaboration and permissions

The user controls scope and external actions. Honor existing authorization;
necessary edits in an authorized implementation do not need repeated permission.
Resolve automation modes via `.codex/docs/automation-modes.md`; current user
instructions override the template defaults. Ask about unresolved material choices.
Never interpret an empty/skipped answer as consent. Subagent questions return to
the parent. Publishing, pushing, deleting, or changing external services requires
authorization for that action. Host sandbox and approval settings always apply.

## Coding and verification

Read `.codex/docs/coding-standards.md` and applicable `.codex/rules/` references.
Use `python .codex/scripts/rules_for.py <paths>` to find path-matched rules.
Read the matching references; these are not automatically loaded Codex rules.
Keep design decisions and tuning data explicit, but honor the selected rigor.
For observable changes, run and inspect the game according to
`.codex/docs/run-and-observe.md`. Build success is not gameplay verification.
Do not edit Unreal binary assets as text. Use an available editor integration.
Report test commands, outcomes, retained evidence, and unverified conditions.

## Context management

`production/session-state/active.md` is the working checkpoint. Read it when
resuming, then check its branch and task still match. Read
`.codex/docs/context-management.md` for checkpoint conventions.
Helpers emit facts; an absent check or dependency is NOT VERIFIED, never clean.
Do not confuse framework tests (`tests/` and `studio-tests/`) with game validation.

## Framework development

After changing role briefs: `python tools/studio.py generate`.
Validate with `python tools/studio.py check` and
`python -m unittest discover -s tests -v`. No model or engine is invoked by these.
Preserve upstream attribution and license notices. See `UPSTREAM.md`.
