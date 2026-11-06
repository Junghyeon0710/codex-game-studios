# Codex Game Studios

Turn a Codex session into a coordinated game development studio.
49 specialist roles. 74 workflow skills. Godot, Unity, and Unreal.

An independent Codex adaptation of [Claude Code Game Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) by Donchitos, based on upstream v1.2.0. Original work is MIT licensed. Not affiliated with or endorsed by OpenAI or Anthropic. See [UPSTREAM.md](UPSTREAM.md).

[![Validate Codex port](https://github.com/Junghyeon0710/codex-game-studios/actions/workflows/validate.yml/badge.svg)](https://github.com/Junghyeon0710/codex-game-studios/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Initial port:** native configurations and helper contracts are tested separately
from game output. No end-to-end Codex game-generation benchmark is claimed.
Read [compatibility and validation](docs/CODEX-PORT.md) before adopting it.

---

## Why This Exists

Game development spans design, architecture, programming, art, QA, and release.
This template gives Codex explicit roles, reusable workflows, and evidence-based
handoffs across those disciplines. The original studio organization and document
format are preserved, with runtime integration adapted for Codex.

## Table of Contents

- [What's Included](#whats-included)
- [Studio Hierarchy](#studio-hierarchy)
- [Skills](#skills)
- [Does it produce games, or documents?](#does-it-produce-games-or-documents)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Upgrading](#upgrading)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Design Philosophy](#design-philosophy)
- [Customization](#customization)
- [Platform Support](#platform-support)
- [Community](#community)
- [Supporting This Project](#supporting-this-project)
- [License](#license)

## What's Included

| Category | Count | Description |
|---|---:|---|
| Agents | 49 | Editable role briefs plus generated native Codex TOML agents |
| Skills | 74 | Design, implementation, QA, production, and release workflows |
| Bash hook files | 18 | Inherited checks/helpers; supported events connected through a native adapter |
| Rules | 14 | Coding standards selected explicitly by path, not native automatic rules |
| Templates | 62 | GDDs, UX specs, ADRs, sprint plans, and QA documents |

## Studio Hierarchy


Agents are organized into three tiers, matching how real studios operate:

```
Tier 1 — Directors
  creative-director    technical-director    producer

Tier 2 — Department Leads
  game-designer        lead-programmer       art-director
  audio-director       narrative-director    qa-lead
  release-manager      localization-lead

Tier 3 — Specialists
  gameplay-programmer  engine-programmer     ai-programmer
  network-programmer   tools-programmer      ui-programmer
  systems-designer     level-designer        economy-designer
  technical-artist     sound-designer        writer
  world-builder        ux-designer           prototyper
  performance-analyst  devops-engineer       analytics-engineer
  security-engineer    qa-tester             accessibility-specialist
  live-ops-designer    community-manager
```

All 49 native agents inherit the parent model by default. Tiers describe responsibility, not a billing plan.

### Engine Specialists

The template includes agent sets for all three major engines. Use the set that matches your project:

| Engine | Lead Agent | Sub-Specialists |
|--------|-----------|-----------------|
| **Godot 4** | `godot-specialist` | GDScript, Shaders, GDExtension |
| **Unity** | `unity-specialist` | DOTS/ECS, Shaders/VFX, Addressables, UI Toolkit |
| **Unreal Engine 5** | `unreal-specialist` | GAS, Blueprints, Replication, UMG/CommonUI |


## Skills


Select a skill in Codex or invoke it with `$name`. All 74 workflows are retained:

**Onboarding & Navigation**
`$start` `$help` `$project-stage-detect` `$setup-engine` `$adopt` `$settings`

**Game Design**
`$brainstorm` `$map-systems` `$design-system` `$quick-design` `$review-all-gdds` `$propagate-design-change`

**Art & Assets**
`$art-bible` `$asset-spec` `$asset-audit`

**UX & Interface Design**
`$ux-design` `$ux-review`

**Architecture**
`$create-architecture` `$architecture-decision` `$architecture-review` `$create-control-manifest`

**Stories & Sprints**
`$create-epics` `$create-stories` `$dev-story` `$sprint-plan` `$sprint-status` `$story-readiness` `$story-done` `$estimate`

**Reviews & Analysis**
`$design-review` `$code-review` `$balance-check` `$content-audit` `$scope-check` `$perf-profile` `$tech-debt` `$gate-check` `$consistency-check` `$security-audit`

**QA & Testing**
`$qa-plan` `$smoke-check` `$soak-test` `$regression-suite` `$test-setup` `$test-helpers` `$test-evidence-review` `$test-flakiness` `$skill-test` `$skill-improve`

**Production**
`$milestone-review` `$retrospective` `$bug-report` `$bug-triage` `$reverse-document` `$playtest-report`

**Release**
`$release-checklist` `$launch-checklist` `$changelog` `$patch-notes` `$hotfix` `$day-one-patch`

**Creative & Content**
`$prototype` `$vertical-slice` `$onboard` `$localize`

**Team Orchestration** (coordinate multiple agents on a single feature)
`$team-combat` `$team-narrative` `$team-ui` `$team-release` `$team-polish` `$team-audio` `$team-level` `$team-live-ops` `$team-qa`


## Does it produce games, or documents?

The workflows cover both, but this port does not ship a finished game or claim a
runtime benchmark. Upstream's game comparison belongs to upstream, not this port.
Use `modes.rigor: minimal` for the shortest route to implementation, and increase
process only when the project benefits. Observable changes still require a real
run and retained screenshot; tests and code inspection do not prove visual output.

## Getting Started

### Prerequisites

- [Codex](https://learn.chatgpt.com/docs/cli), with repository skills and native agents/hooks for full integration.
- Git, Bash (Git for Windows on Windows), Python 3.11+.
- Your game engine and its build dependencies, installed separately.

### Setup

```bash
git clone https://github.com/Junghyeon0710/codex-game-studios.git my-game
cd my-game
python -m pip install -r requirements-dev.txt
python tools/studio.py doctor
python tools/studio.py check
codex
```

Start Codex at this root, review the project configuration and hook definitions
(`/hooks` in supported clients), then select **$start**. In the desktop app, open
the cloned folder and invoke the same skill. Hooks stay inactive until trusted.
Use the model available in your account; the template pins no model.

Already have a game? Merge `AGENTS.md`, `.agents/skills/`, `.codex/`, and the
framework's supporting files after reviewing conflicts, then run **$adopt**.
Preserve existing settings, game files, and user instructions.

## Configuration

`project.yaml` controls studio workflows. `project.local.yaml` holds supported
personal overrides and is gitignored. These are separate from Codex host settings.

| Rigor | Intended use |
|---|---|
| `minimal` (default) | Brief, small stories, lightweight documentation |
| `standard` | Structured design, broader QA, lean review |
| `full` | Full design sections, traceability, director review |

Automation is independent: `collaborative`, `guided`, or `autonomous`.
Current user authorization takes precedence over repeated template write prompts;
no automation setting bypasses host approvals. See `.codex/docs/automation-modes.md`.

```text
$settings
$settings modes.rigor=standard
$settings --local modes.review_mode=solo
```

Native agents live in `.codex/agents/*.toml`; native hooks in `.codex/hooks.json`.
The default agent configs inherit model and permission settings. See the
[runtime contract](.codex/docs/codex-runtime.md).

## Upgrading

See [UPGRADING.md](UPGRADING.md). Upstream and Codex port versions are independent.
Review framework changes, preserve game content, and re-review changed hooks.

## Project Structure

```text
AGENTS.md                       # Project instructions and runtime entry point
.agents/skills/                 # 74 Codex skills with supporting references
.codex/
  config.toml                   # Native project config, no model/permission override
  agents/                       # 49 generated native TOML agents
  roles/                        # 49 editable role briefs
  hooks.json                    # Native lifecycle configuration
  hooks/                        # Bash checks + Python Codex adapter
  rules/                        # 14 explicitly selected coding standards
  scripts/                      # Configuration, status, and inspection helpers
  docs/                         # Workflow references and document templates
design/                         # Game design and narrative records
docs/                           # Architecture and engine references
production/                     # Stories, QA evidence, release and session records
src/                            # Godot code root; Unity uses Assets/, Unreal Source/
tools/studio.py                 # Generate, validate, and diagnose the port
tests/                          # Executable Codex-port contract tests
studio-tests/                   # Inherited written skill/agent evaluation specs
```

### Testing your customizations

```bash
python tools/studio.py generate
python tools/studio.py check
python -m unittest discover -s tests -v
```

`$skill-test` and `$skill-improve` inspect workflow quality. Written specs do not
execute Codex or an engine. See [validation scope](docs/CODEX-PORT.md).

## How It Works

### Agent Coordination

Directors frame decisions, leads coordinate, and specialists perform bounded work.
Independent tasks can be delegated in parallel. The parent checks artifacts and
collects results before dependent phases. Shared editor and asset edits are serial.
If custom agents are unavailable, use a supported worker with the role brief; if
delegation is unavailable, proceed sequentially and disclose that fallback.

### Collaborative, Not Autonomous by Default

The user controls scope and publication. Workflow rigor and automation are separate.
Use existing authorization and avoid asking for the same edit repeatedly. Material
unresolved choices still need an answer. Native host permissions always apply.

### Automated Checks

The Codex adapter connects session context, shell commit checks, push reminders,
patch/registry checks, data validation, and agent audit logs to supported events.
It never grants approval. Unsupported patch forms and missing dependencies report
NOT VERIFIED. Read-size checks remain manual, and shell/MCP edits do not all pass
through patch guards. See [hook coverage](.codex/docs/hooks-reference.md).

### Path-Scoped Rules

Use `python .codex/scripts/rules_for.py <paths>` and read the matching rule files.
Godot, Unity, and Unreal paths are represented. These references guide Codex;
they are not automatically enforced by a native rules directory.

## Design Philosophy

- Preserve design intent through small, checkable tasks.
- Use data-driven game design and explicit acceptance criteria.
- Match documentation and review depth to project needs.
- Observe player-visible results and retain evidence.
- Report incomplete or unverified work honestly.

## Customization

Edit `.codex/roles/`, regenerate the native agents, and run the checks. Add or tune
skills and their references, engine commands, rules, and templates. Configure an
editor MCP integration separately when needed; no engine MCP server is bundled.
The inherited template is intended to be adapted to the project.

## Platform Support

| Platform | Runtime dependencies |
|---|---|
| Windows | Python 3.11+, Git Bash on PATH, Codex client |
| macOS | Python 3.11+, Bash, Git, Codex client |
| Linux | Python 3.11+, Bash, Git, Codex client |

CI exercises contract tests on all three platforms. See the Actions run for actual
results. Engine/editor integration must be validated in your installed environment;
CI passing does not mean a game was built or played.

## Community

Open issues and pull requests in [this repository](https://github.com/Junghyeon0710/codex-game-studios).
Include the Codex version, OS, engine version, reproduction, and actual logs.
See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md).

## Supporting This Project

Star the repository, contribute fixes and reproducible evaluations, and credit
the [original project](https://github.com/Donchitos/Claude-Code-Game-Studios).

## License

[MIT](LICENSE). Original work copyright (c) 2026 Donchitos.
Codex adaptation copyright (c) 2026 Junghyeon0710. See [UPSTREAM.md](UPSTREAM.md).
