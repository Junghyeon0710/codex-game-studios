# Contributing

Thanks for contributing to Codex Game Studios. This is an independent MIT-licensed
adaptation of Donchitos' Claude Code Game Studios; preserve attribution.

## Development

Use Python 3.11+, Git and Bash. Install `requirements-dev.txt`.
Edit role briefs in `.codex/roles`, then run `python tools/studio.py generate`.
Run `python tools/studio.py check` and `python -m unittest discover -s tests -v`.
Do not commit personal config, transcripts, credentials, or private game assets.

## Pull requests

Explain the behavior changed, the relevant workflow, and actual validation.
Keep native code and generated agents consistent. Include a regression test for
runtime adapter/parser changes. Treat written spec reviews and real agent/engine
executions as different evidence. Report engine tests only when actually run.
Add new workflow names to the manifest and specs, then update counts in README.

## Compatibility

Follow official Codex schemas, and document required capabilities and fallbacks.
Do not add global model pins, bypass hook trust, or silently weaken host permissions.
Report bugs in the port here; do not automatically post into upstream repositories.
