#!/usr/bin/env python3
"""Adapt Codex hook events to the inherited, independently testable Bash checks.

Never emits permissionDecision=allow and never changes host permission settings.
Unsupported patch forms are reported, not silently certified as checked.
"""
from pathlib import Path
import json
import importlib.util
import os
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]

def patch_changes(command, root):
    """Return effective writes for Codex apply_patch; do not write any files."""
    lines = command.splitlines()
    if not lines or lines[0] != '*** Begin Patch' or lines[-1] != '*** End Patch':
        raise ValueError('Unknown apply_patch format')
    changes = []
    i = 1
    while i < len(lines) - 1:
        header = lines[i]
        i += 1
        kind, sep, name = header.partition(': ')
        if not sep or kind not in ('*** Add File', '*** Update File', '*** Delete File'):
            raise ValueError('Unknown patch operation: ' + header)
        path = (root / name).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ValueError('Patch path outside studio root: ' + name)
        if path.suffix.lower() in ('.uasset', '.umap'):
            raise PermissionError('Binary Unreal assets must be changed through editor tools: ' + name)
        destination = path
        if i < len(lines) and lines[i].startswith('*** Move to: '):
            destination = (root / lines[i][13:]).resolve()
            if not destination.is_relative_to(root.resolve()):
                raise ValueError('Move destination outside studio root')
            if destination.suffix.lower() in ('.uasset', '.umap'):
                raise PermissionError('Cannot move a text patch to a binary Unreal asset')
            i += 1
        body = []
        while i < len(lines) - 1 and not lines[i].startswith(('*** Add File:', '*** Update File:', '*** Delete File:')):
            body.append(lines[i])
            i += 1
        if kind == '*** Delete File':
            changes.append({'file_path': str(path), 'content': '', 'operation': 'delete'})
            continue
        if kind == '*** Add File':
            if any(not line.startswith('+') for line in body):
                raise ValueError('Invalid Add File line')
            content = '\n'.join(line[1:] for line in body) + '\n'
        else:
            old = path.read_text(encoding='utf-8').splitlines()
            cursor = 0
            result = []
            hunks = []
            before, after = [], []
            anchor = ''
            for line in body + ['@@']:
                if line.startswith('@@'):
                    if before or after:
                        hunks.append((anchor, before, after))
                    anchor, before, after = line[2:].strip(), [], []
                elif line == '*** End of File':
                    continue
                elif line.startswith(' '):
                    before.append(line[1:]); after.append(line[1:])
                elif line.startswith('-'):
                    before.append(line[1:])
                elif line.startswith('+'):
                    after.append(line[1:])
                else:
                    raise ValueError('Unsupported patch hunk line')
            for anchor, before, after in hunks:
                start = cursor
                if anchor:
                    positions = [n for n in range(cursor, len(old)) if old[n] == anchor]
                    if not positions:
                        raise ValueError('Patch anchor not found')
                    start = positions[0] + 1
                matches = [n for n in range(start, len(old) - len(before) + 1) if old[n:n+len(before)] == before]
                if len(matches) != 1:
                    raise ValueError('Ambiguous/unmatched patch context; write guards not evaluated')
                at = matches[0]
                result += old[cursor:at] + after
                cursor = at + len(before)
            content = '\n'.join(result + old[cursor:]) + '\n'
        changes.append({'file_path': str(destination), 'content': content, 'operation': 'write'})
        if destination != path:
            changes.append({'file_path': str(path), 'content': '', 'operation': 'delete'})
    return changes

def invoke(script, payload, root=ROOT):
    bash = shutil.which('bash')
    if not bash:
        return 0, ['Bash is unavailable; studio hook check NOT VERIFIED: ' + script]
    env = os.environ.copy()
    env['CODEX_STUDIO_ROOT'] = str(root)
    env['PYTHONUTF8'] = '1'
    env['PATH'] = str(Path(sys.executable).parent) + os.pathsep + env.get('PATH', '')
    try:
        result = subprocess.run([bash, str(root / '.codex/hooks' / script)], input=json.dumps(payload),
                                text=True, encoding='utf-8', errors='replace', capture_output=True,
                                cwd=root, env=env, timeout=20)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 0, ['Studio hook NOT VERIFIED: ' + str(exc)]
    messages = []
    for output in (result.stdout, result.stderr):
        for line in output.splitlines():
            try:
                data = json.loads(line)
            except ValueError:
                if line.strip():
                    messages.append(line)
                continue
            if isinstance(data, dict):
                message = data.get('systemMessage') or data.get('hookSpecificOutput', {}).get('additionalContext')
                if message:
                    messages.append(message)
    if result.returncode not in (0, 2):
        messages.append(f'{script}: check NOT VERIFIED (exit {result.returncode})')
    return result.returncode, messages

def dispatch(event, payload, root=ROOT, runner=invoke):
    jobs = []
    messages = []
    tool = payload.get('tool_name', '')
    tool_input = payload.get('tool_input') or {}
    command = tool_input.get('command', tool_input.get('cmd', '')) if isinstance(tool_input, dict) else str(tool_input)
    common = dict(payload)
    common['cwd'] = str(root)
    simple = {
        'SessionStart': ['session-start.sh', 'detect-gaps.sh'],
        'PostCompact': ['session-start.sh'],
        'PreCompact': ['pre-compact.sh'],
        'Stop': ['session-stop.sh'],
        'SubagentStart': ['log-agent.sh'],
        'SubagentStop': ['log-agent-stop.sh', 'validate-agent-artifact.sh'],
        'PermissionRequest': ['notify.sh'],
    }
    for script in simple.get(event, []):
        jobs.append((script, common))
    if event == 'PreToolUse' and tool in ('Bash', 'exec_command', 'PowerShell'):
        shell_payload = dict(common, tool_name='Bash', tool_input={'command': command})
        jobs += [(s, shell_payload) for s in ('validate-commit.sh', 'validate-push.sh')]
    if tool == 'apply_patch' and event in ('PreToolUse', 'PostToolUse'):
        try:
            if event == 'PreToolUse':
                changes = patch_changes(command, root)
                rule_module = root / '.codex/scripts/rules_for.py'
                if rule_module.is_file():
                    try:
                        spec = importlib.util.spec_from_file_location('studio_rules', rule_module)
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        paths = [str(Path(change['file_path']).relative_to(root)) for change in changes]
                        matched = module.rules_for(paths, root)
                        if matched:
                            messages.append('Read applicable studio rules before editing: ' + ', '.join(matched))
                    except (ImportError, ValueError) as exc:
                        messages.append('Rule lookup NOT VERIFIED: ' + str(exc))
            else:
                # After edits, inspect actual files; replaying old hunks would be wrong.
                changes = []
                for line in command.splitlines():
                    if line.startswith(('*** Add File: ', '*** Update File: ', '*** Move to: ')):
                        path = (root / line.split(': ', 1)[1]).resolve()
                        if path.is_relative_to(root.resolve()) and path.is_file() and path.suffix.lower() not in ('.uasset', '.umap'):
                            changes.append({'file_path': str(path), 'content': path.read_text(encoding='utf-8')})
            scripts = ['validate-write.sh', 'validate-registry.sh'] if event == 'PreToolUse' else ['validate-assets.sh', 'validate-skill-change.sh']
            for change in changes:
                translated = dict(common, tool_name='Write', tool_input=change)
                jobs += [(s, translated) for s in scripts]
        except PermissionError as exc:
            return {'hookSpecificOutput': {'hookEventName': event, 'permissionDecision': 'deny', 'permissionDecisionReason': str(exc)}}
        except (ValueError, OSError, UnicodeError) as exc:
            messages.append('Patch checks NOT VERIFIED: ' + str(exc))
    for script, job in jobs:
        code, output = runner(script, job, root)
        messages.extend(output)
        if code == 2 and event == 'PreToolUse':
            return {'hookSpecificOutput': {'hookEventName': event, 'permissionDecision': 'deny',
                    'permissionDecisionReason': '\n'.join(messages)[-6000:] or script + ' blocked the operation'}}
    text = '\n'.join(dict.fromkeys(messages))[-10000:]
    if not text:
        return {}
    result = {'systemMessage': text}
    if event in ('SessionStart', 'PostCompact', 'PreToolUse', 'PostToolUse'):
        result['hookSpecificOutput'] = {'hookEventName': event, 'additionalContext': text}
    return result

if __name__ == '__main__':
    try:
        payload = json.load(sys.stdin)
        print(json.dumps(dispatch(sys.argv[1], payload)))
    except Exception as exc:
        print(json.dumps({'systemMessage': 'Studio hook NOT VERIFIED: ' + str(exc)}))
