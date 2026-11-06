#!/usr/bin/env bash
# Native compatibility inventory. Options: --skill NAME, --agent NAME, [root].
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
for candidate in python python3 py; do
    if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' >/dev/null 2>&1; then
        exec "$candidate" "$ROOT/tools/compat_inventory.py" "$@"
    fi
done
echo 'compat-inventory: Python 3.11+ required; NOT VERIFIED' >&2
exit 1
