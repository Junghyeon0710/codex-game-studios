#!/usr/bin/env python3
"""List inherited rule documents that apply to project-relative paths."""
from pathlib import Path
import fnmatch
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[2]

def expand(pattern):
    match = re.search(r'\{([^{}]+)\}', pattern)
    if not match:
        return [pattern]
    return [item for part in match[1].split(',') for item in expand(pattern[:match.start()] + part + pattern[match.end():])]

def matches(path, pattern):
    # **/ matches zero or more directory levels; fnmatch alone requires the slash.
    parts = pattern.split('**/')
    options = [parts[0]]
    for part in parts[1:]:
        options = [prefix + middle + part for prefix in options for middle in ('**/', '')]
    return any(fnmatch.fnmatchcase(path, item) for item in options)

def rules_for(paths, root=ROOT):
    result = []
    for rule in sorted((root / '.codex/rules').glob('*.md')):
        text = rule.read_text(encoding='utf-8')
        if not text.startswith('---\n'):
            continue
        data = yaml.safe_load(text.split('---', 2)[1]) or {}
        patterns = [item for pattern in data.get('paths', []) for item in expand(pattern)]
        if any(matches(str(path).replace('\\', '/'), pattern) for path in paths for pattern in patterns):
            result.append(str(rule.relative_to(root)).replace('\\', '/'))
    return result

if __name__ == '__main__':
    for rule in rules_for(sys.argv[1:]):
        print(rule)
