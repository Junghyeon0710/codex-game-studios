# Multi-agent workflows in Codex

Use native subagents from a studio orchestration skill. Custom role configurations
are `.codex/agents/*.toml`. No experimental Claude environment variable is used.
Independent work may run in parallel; collect results before dependent steps.
Respect host limits, parent permissions, file ownership, and shared editor state.
For isolated checkouts, use the host's supported worktree mechanism or an explicit
Git worktree, and report its path. No fixed worktree directory is assumed.
When native delegation is unavailable, run sequentially and disclose that fallback.
See `codex-runtime.md` and the official subagent documentation.
