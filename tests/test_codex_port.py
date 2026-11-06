"""Contract tests for native files, hook translation, and legacy helper integration."""
from pathlib import Path
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import contextlib
import io

ROOT = Path(__file__).resolve().parents[1]

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

adapter = load('adapter', ROOT / '.codex/hooks/codex_adapter.py')
studio = load('studio', ROOT / 'tools/studio.py')
rules = load('rules', ROOT / '.codex/scripts/rules_for.py')

class PortTests(unittest.TestCase):
    def test_native_sources_match_manifest(self):
        self.assertEqual(studio.check(), 0)

    def test_patch_add_update_move_delete(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'old.txt').write_text('one\ntwo\nthree\n', encoding='utf-8')
            patch = '*** Begin Patch\n*** Update File: old.txt\n*** Move to: moved.txt\n@@\n one\n-two\n+second\n three\n*** Add File: new.txt\n+hello\n*** Delete File: gone.txt\n*** End Patch'
            changes = adapter.patch_changes(patch, root)
            self.assertEqual(changes[0]['content'], 'one\nsecond\nthree\n')
            self.assertEqual(Path(changes[0]['file_path']).name, 'moved.txt')
            self.assertEqual(changes[1]['operation'], 'delete')
            self.assertEqual(changes[2]['content'], 'hello\n')
            self.assertEqual(changes[3]['operation'], 'delete')
            self.assertEqual((root / 'old.txt').read_text(), 'one\ntwo\nthree\n')
            self.assertFalse((root / 'moved.txt').exists())

    def test_binary_patch_is_denied(self):
        result = adapter.dispatch('PreToolUse', {'tool_name': 'apply_patch', 'tool_input': {'command': '*** Begin Patch\n*** Add File: Content/Test.uasset\n+x\n*** End Patch'}})
        self.assertEqual(result['hookSpecificOutput']['permissionDecision'], 'deny')

    def test_path_escape_not_silently_checked(self):
        result = adapter.dispatch('PreToolUse', {'tool_name': 'apply_patch', 'tool_input': {'command': '*** Begin Patch\n*** Add File: ../outside.txt\n+x\n*** End Patch'}})
        self.assertIn('NOT VERIFIED', result['systemMessage'])

    def test_ambiguous_patch_context_reports_unverified(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'a.txt').write_text('same\nsame\n', encoding='utf-8')
            result = adapter.dispatch('PreToolUse', {'tool_name': 'apply_patch', 'tool_input': {'command': '*** Begin Patch\n*** Update File: a.txt\n@@\n-same\n+other\n*** End Patch'}}, root)
            self.assertIn('NOT VERIFIED', result['systemMessage'])

    def test_shell_adapter_preserves_command_and_denial(self):
        calls = []
        def runner(script, payload, root):
            calls.append((script, payload))
            return (2, ['invalid JSON'])
        result = adapter.dispatch('PreToolUse', {'tool_name': 'exec_command', 'tool_input': {'cmd': 'git commit -m test'}}, runner=runner)
        self.assertEqual(calls[0][1]['tool_input']['command'], 'git commit -m test')
        self.assertEqual(result['hookSpecificOutput']['permissionDecision'], 'deny')

    def test_warnings_never_grant_permission(self):
        result = adapter.dispatch('PreToolUse', {'tool_name': 'Bash', 'tool_input': {'command': 'git push'}}, runner=lambda *args: (0, ['Review push']))
        self.assertNotIn('permissionDecision', result['hookSpecificOutput'])

    def test_post_patch_uses_written_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'data.json').write_text('{"now":2}', encoding='utf-8')
            calls = []
            def runner(script, payload, root):
                calls.append(payload['tool_input']['content'])
                return 0, []
            adapter.dispatch('PostToolUse', {'tool_name': 'apply_patch', 'tool_input': {'command': '*** Begin Patch\n*** Update File: data.json\n@@\n-old\n+new\n*** End Patch'}}, root, runner)
            self.assertEqual(calls, ['{"now":2}', '{"now":2}'])

    def test_rule_matching_all_engines(self):
        for path in ('src/gameplay/player.gd', 'Assets/Gameplay/Player.cs', 'Source/Game/Private/Gameplay/Player.cpp'):
            self.assertIn('.codex/rules/gameplay-code.md', rules.rules_for([path]))

    @unittest.skipUnless(shutil.which('bash'), 'Git Bash/bash required')
    def test_config_resolution_executes(self):
        result = subprocess.run([shutil.which('bash'), '.codex/hooks/yaml-helper.sh', 'resolve_config', '--keys', 'workflow,automation,qa.level'], cwd=ROOT, text=True, encoding='utf-8', capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('minimal', result.stdout)
        self.assertIn('collaborative', result.stdout)

    @unittest.skipUnless(shutil.which('bash'), 'Git Bash/bash required')
    def test_skill_linter_reads_every_skill(self):
        result = subprocess.run([shutil.which('bash'), '.codex/scripts/skill-lint.sh', 'all'], cwd=ROOT, text=True, encoding='utf-8', capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout.splitlines()[-1], 'checked\t74 of 74')
        self.assertNotIn('missing=name', result.stdout)

    def test_changed_generated_agent_fails_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(ROOT / '.codex', root / '.codex')
            shutil.copytree(ROOT / '.agents', root / '.agents')
            shutil.copy(ROOT / 'LICENSE', root / 'LICENSE')
            agent = root / '.codex/agents/producer.toml'
            agent.write_text(agent.read_text(encoding='utf-8').replace('name = "producer"', 'name = "wrong"'), encoding='utf-8')
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(studio.check(root), 1)

if __name__ == '__main__':
    unittest.main()
