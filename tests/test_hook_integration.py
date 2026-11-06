from pathlib import Path
import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('integration_adapter', ROOT / '.codex/hooks/codex_adapter.py')
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)

@unittest.skipUnless(shutil.which('bash') and shutil.which('git'), 'Bash and Git required')
class HookIntegrationTests(unittest.TestCase):
    def test_real_commit_hook_denies_invalid_staged_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(ROOT / '.codex/hooks', root / '.codex/hooks')
            shutil.copytree(ROOT / '.codex/scripts', root / '.codex/scripts')
            (root / 'project.yaml').write_text('engine:\n  name: godot\nupdates:\n  check: false\n', encoding='utf-8')
            data = root / 'assets/data/broken.json'
            data.parent.mkdir(parents=True)
            data.write_text('{invalid', encoding='utf-8')
            for args in (['git', 'init', '-q'], ['git', 'add', 'assets/data/broken.json']):
                subprocess.run(args, cwd=root, check=True, capture_output=True)
            result = adapter.dispatch('PreToolUse', {'tool_name': 'Bash', 'tool_input': {'command': 'git commit -m test'}}, root)
            self.assertEqual(result['hookSpecificOutput']['permissionDecision'], 'deny', result)
            data.write_text('{"valid":true}', encoding='utf-8')
            subprocess.run(['git', 'add', str(data)], cwd=root, check=True, capture_output=True)
            result = adapter.dispatch('PreToolUse', {'tool_name': 'Bash', 'tool_input': {'command': 'git commit -m test'}}, root)
            self.assertNotEqual(result.get('hookSpecificOutput', {}).get('permissionDecision'), 'deny', result)

    def test_session_adapter_outputs_json_and_orientation(self):
        payload = {'cwd': str(ROOT), 'session_id': 'contract-test', 'source': 'startup'}
        result = adapter.dispatch('SessionStart', payload)
        self.assertIn('systemMessage', result)
        self.assertIn('hookSpecificOutput', result)
        self.assertEqual(result['hookSpecificOutput']['hookEventName'], 'SessionStart')
        self.assertNotIn('NOT VERIFIED', result['systemMessage'])

if __name__ == '__main__':
    unittest.main()
