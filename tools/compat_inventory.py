#!/usr/bin/env python3
"""Inventory residual client-specific syntax in active Codex instructions."""
from pathlib import Path
import argparse
import re
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--skill')
parser.add_argument('--agent')
parser.add_argument('root', nargs='?', type=Path, default=Path(__file__).resolve().parents[1])
args = parser.parse_args()
root = args.root.resolve()
if args.skill and args.agent:
    parser.error('choose --skill or --agent, not both')
if args.skill:
    if args.skill != Path(args.skill).name or args.skill.startswith('.'):
        parser.error('invalid skill name')
    files = sorted((root / '.agents/skills' / args.skill).rglob('*.md'))
elif args.agent:
    if args.agent != Path(args.agent).name or args.agent.startswith('.'):
        parser.error('invalid role name')
    files = [root / '.codex/roles' / (args.agent + '.md')]
else:
    files = [root / 'AGENTS.md']
    for folder in ('.agents/skills', '.codex/roles', '.codex/docs', '.codex/rules'):
        files.extend(sorted((root / folder).rglob('*.md')))
patterns = {
    'dynamic-prelude': re.compile(r'^!`'),
    'implicit-import': re.compile(r'^@\S'),
    'legacy-environment': re.compile(r'\$\{?CLAUDE_[A-Z_]+'),
    'legacy-question-tool': re.compile(r'\bAskUserQuestion\b'),
    'legacy-cli': re.compile(r'@anthropic-ai/claude-code|claude --permission-mode|claude --worktree'),
}
hits = 0
if not files:
    print('NOT_READ: no matching instruction files'); sys.exit(1)
for path in files:
    if not path.is_file():
        print('NOT_READ: ' + str(path)); hits += 1
        continue
    for n, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        for name, pattern in patterns.items():
            if pattern.search(line):
                print(f'FOUND: {name} {path.relative_to(root)}:{n}')
                hits += 1
print(f'FILES: {len(files)} RESIDUAL_LINES: {hits}')
sys.exit(1 if hits else 0)
