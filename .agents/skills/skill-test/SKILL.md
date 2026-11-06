---
name: skill-test
description: Validate studio skills and roles using structural checks, written behavioral specifications, category rubrics, or coverage inventory.
---

Read `.codex/docs/codex-runtime.md` before using this workflow.
Arguments: `static [name|all] | spec [name] | category [name|all] | audit`.

# Skill Test

## Phase 1: Select scope

Use `.codex/port-manifest.json` and `studio-tests/catalog.yaml` to resolve the name.
Read the chosen skill and its references, or the role brief and generated TOML.
No mode invokes a model automatically; runtime evaluation must be separately
requested and run against a disposable project.

## Phase 2: Validate

- `static`: run `python tools/studio.py check`. For workflow observations also run
  `bash .codex/scripts/skill-lint.sh <name|all>`. Review name/description, useful
  phases, clear outcomes, authorization consistent with the current request,
  next-step routing, native tool compatibility, and argument instructions.
  Native skill frontmatter requires name and description; do not require Claude
  tool grants, model pins, invocation flags, or fork-context fields.
- `spec`: read the matching inherited specification and evaluate each applicable
  assertion against the instructions. Mark obsolete Claude-specific assertions
  NOT APPLICABLE and explain the Codex replacement. Do not call this a runtime pass.
- `category`: read the category rubric and assess the selected skills/roles;
  distinguish framework structure from actual observed behavior.
- `audit`: enumerate every role/skill, specification coverage, and any recorded
  evaluation dates. Missing results are NOT TESTED, never pass.

## Phase 3: Report

Report scope, executed commands and exit codes, structural defects, unassessed
cases, and one of COMPLIANT / WARNINGS / NON-COMPLIANT / NOT ASSESSED.
A structural pass proves only structural compatibility. A written spec review
proves only instruction coverage. Runtime success requires executing the workflow.
Do not update catalog results without authorization for that write.
Next: `$skill-improve [name]` for a concrete defect, or run a disposable runtime
evaluation when the user asks to test behavior.
