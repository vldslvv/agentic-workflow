"""AC-2: role input integrity, selection accounting, and reviewer boundary."""
import hashlib
import copy
import importlib.util
from pathlib import Path
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1] / 'helpers' / 'role_context.py'
spec = importlib.util.spec_from_file_location('role_context', MODULE)
context = importlib.util.module_from_spec(spec)
spec.loader.exec_module(context)


class RoleContextTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.paths = ['AGENTS.md', 'spec-source-suite/AGENTS.md',
                      'spec-source-suite/docs/SUITE_CONTRACT.md',
                      'spec-source-suite/prompts/REVIEWER.md',
                      'spec-source-suite/prompts/VERIFIER.md', 'specs/task.md']
        self.reads = []
        for path in self.paths:
            dest = self.root / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text('# Required\nRule café.\n## Child\nKeep this.\n# Other\nOmit.\n')
            self.reads.append({'path': path, 'sha256': hashlib.sha256(dest.read_bytes()).hexdigest()})
        self.manifest = {'version': 1, 'role': 'reviewer', 'reads': self.reads, 'owned_paths': ['results/review.json']}

    def test_sections_count_utf8_bytes_and_keep_canonical_references(self):
        self.reads[-1]['section'] = 'Required'
        result = context.build_context(self.manifest, self.root)
        selected = '# Required\nRule café.\n## Child\nKeep this.\n'.encode()
        self.assertEqual(result['reads'][-1]['selected_bytes'], len(selected))
        self.assertEqual(result['suite_controlled_selected_bytes'], 5 * len((self.root / 'AGENTS.md').read_bytes()))
        self.assertEqual(result['selected_bytes'], result['suite_controlled_selected_bytes'] + len(selected))

    def test_invalid_references_fail_explicitly(self):
        for mutation, message in [
            (lambda m: m['reads'].pop(0), 'canonical'),
            (lambda m: m['reads'][0].update(sha256='bad'), 'digest mismatch'),
            (lambda m: m['reads'][-1].update(section='Missing'), 'section missing'),
            (lambda m: m['reads'][3].update(section='Other'), 'canonical instructions require full file'),
            (lambda m: m['reads'][-1].update(path='missing.md'), 'missing referenced'),
        ]:
            import copy
            with self.subTest(message=message):
                manifest = copy.deepcopy(self.manifest)
                mutation(manifest)
                with self.assertRaisesRegex(ValueError, message):
                    context.build_context(manifest, self.root)

    def test_reviewer_cannot_receive_excluded_references_in_metadata_or_symlinks(self):
        (self.root / 'plan.md').write_text('Excluded plan')
        (self.root / 'innocent.md').symlink_to('plan.md')
        import copy
        for injected in [
            {'metadata': {'reference': 'plan.md'}},
            {'metadata': {'category': 'conversation'}},
            {'metadata': {'reference': 'innocent.md'}},
            {'reads': self.reads + [{'path': 'innocent.md', 'sha256': hashlib.sha256(b'Excluded plan').hexdigest()}]},
        ]:
            manifest = copy.deepcopy(self.manifest)
            manifest.update(injected)
            with self.subTest(injected=injected), self.assertRaisesRegex(ValueError, 'reviewer'):
                context.build_context(manifest, self.root)

    def test_explicit_forbidden_alias_is_rejected(self):
        self.manifest['forbidden_paths'] = ['specs/task.md']
        with self.assertRaisesRegex(ValueError, 'reviewer'):
            context.build_context(self.manifest, self.root)

    def test_memory_exclusion_and_regeneration_forbidden_paths(self):
        """AC-3: real files, directory aliases, retained copies and metadata."""
        memory = self.root / '.agents/memory'
        memory.mkdir(parents=True)
        (memory / 'index.md').write_text('Curated advice')
        (self.root / 'alias.md').symlink_to(memory / 'index.md')
        (self.root / 'alias\n.md').symlink_to(memory / 'index.md')
        (self.root / 'alias-dir').symlink_to(memory, target_is_directory=True)
        retained = self.root / 'records/memory-inputs'
        retained.mkdir(parents=True)
        (retained / 'note.md').write_text('Retained advice')
        (self.root / 'neutral.md').write_text('Categorized advice')
        for role in ('reviewer', 'implementer', 'planner', 'supervisor'):
            for path in context.ROLES[role]:
                dest = self.root / 'spec-source-suite' / path
                dest.parent.mkdir(parents=True, exist_ok=True)
                if not dest.exists():
                    dest.write_text('# Required\n')
            required = list(context.COMMON) + [
                'spec-source-suite/' + p for p in context.ROLES[role]]
            base = {'version': 1, 'role': role, 'owned_paths': [], 'reads': [
                {'path': p, 'sha256': hashlib.sha256((self.root / p).read_bytes()).hexdigest()}
                for p in required]}
            if role != 'reviewer':
                base['forbidden_paths'] = ['.agents/memory', 'records/memory-inputs', 'neutral.md']
            context.build_context(base, self.root)  # valid negative control
            for path in ('.agents/memory/index.md', 'alias.md', 'alias\n.md', 'alias-dir/index.md',
                         'records/memory-inputs/note.md', 'neutral.md'):
                for location in ('reads', 'metadata'):
                    job = copy.deepcopy(base)
                    item = {'path': path, 'category': 'project-memory' if path == 'neutral.md' else 'reference',
                            'sha256': hashlib.sha256((self.root / path).read_bytes()).hexdigest()}
                    if location == 'reads':
                        job['reads'].append(item)
                    else:
                        job['metadata'] = item
                    with self.subTest(role=role, path=path, location=location):
                        with self.assertRaisesRegex(ValueError, 'forbidden|excludes'):
                            context.build_context(job, self.root)

    def test_memory_writes_are_separate_from_candidate_and_retained_inputs(self):
        memory = self.root / '.agents/memory'
        memory.mkdir(parents=True)
        (memory / 'index.md').write_text('Advice')
        path = 'spec-source-suite/docs/IMPLEMENT.md'
        (self.root / path).write_text('# Implement\n')
        job = {'version': 1, 'role': 'implementer', 'owned_paths': ['app'],
               'memory_write_paths': ['.agents/memory'], 'reads': [
                   {'path': p, 'sha256': hashlib.sha256((self.root / p).read_bytes()).hexdigest()}
                   for p in (*context.COMMON, path)]}
        self.assertEqual(context.build_context(job, self.root)['memory_write_paths'], ['.agents/memory'])
        for update in ({'owned_paths': ['.agents']},
                       {'memory_write_paths': ['spec-source-suite/docs']},
                       {'forbidden_paths': ['.agents/memory']},
                       {'memory_write_paths': '.agents/memory'}):
            with self.subTest(update=update), self.assertRaisesRegex(ValueError, 'memory|forbidden'):
                context.build_context(dict(job, **update), self.root)


if __name__ == '__main__':
    unittest.main()
