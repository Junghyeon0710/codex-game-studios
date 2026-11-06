# Model assignment in Codex

All generated agents inherit the parent model and reasoning settings. Studio
seniority is a responsibility, not a model tier or a cost guarantee.
Choose an available model in the Codex host. For an intentional per-role override,
edit the generator or native TOML and document it; generation normally replaces
native TOML from `.codex/roles`. The consistency checker flags manual drift.
Do not put Claude model aliases or skill-level model pins in this port.

Each additional agent consumes model work. Use the smallest useful team and
independent phases. No fixed dollar prices or token savings are promised.
See https://learn.chatgpt.com/docs/agent-configuration/subagents.
