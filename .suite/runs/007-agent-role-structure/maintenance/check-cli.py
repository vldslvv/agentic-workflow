"""Exercise the public checker CLI against an isolated, real Git repository."""
from pathlib import Path
import json
import shutil
import subprocess
import tempfile

source = Path('spec-source-suite').resolve()
results = []
with tempfile.TemporaryDirectory(prefix='suite-maintenance-') as temp:
    repo = Path(temp)
    suite = repo / 'spec-source-suite'
    shutil.copytree(source, suite, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    subprocess.run(['git', 'init', '-q', str(repo)], check=True)
    subprocess.run(['git', '-C', str(repo), 'add', '.'], check=True)
    subprocess.run(['git', '-C', str(repo), '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'fixture baseline'], check=True)
    command = ['python', str(suite/'helpers/check_package.py'), '--base', 'HEAD']

    def run(label, expected_code, expected_error=None):
        proc = subprocess.run(command, text=True, capture_output=True)
        assert proc.returncode == expected_code, (label, proc.stdout, proc.stderr)
        report = json.loads(proc.stdout)
        if expected_error:
            assert any(expected_error in error for error in report['errors']), (label, report)
        results.append({'scenario': label, 'exit_code': proc.returncode, 'result': 'PASS'})
        return report

    report = run('Valid package', 0)
    assert report['delta']['instruction_words'] == 0 and not report['review_signals']
    rogue = suite/'supporting-procedure.md'
    rogue.write_text('# Extra procedure\n')
    run('New supporting file is rejected', 1, 'Unexpected package file: supporting-procedure.md')
    rogue.unlink()
    reviewer = suite/'REVIEWER.md'
    original = reviewer.read_text()
    reviewer.unlink()
    run('Missing role is rejected', 1, 'Missing package file: REVIEWER.md')
    reviewer.write_text(original + '\n[Broken](absent.md)\n')
    run('Broken local link is rejected', 1, 'Broken link in REVIEWER.md')
    reviewer.write_text(original + '\n[Broken](AGENTS.md#absent-anchor)\n')
    run('Missing anchor is rejected', 1, 'Missing anchor in REVIEWER.md')
    reviewer.write_text(original.replace('](AGENTS.md)', '](PLANNER.md)'))
    run('Wrong shared-rules entry point is rejected', 1, 'Missing shared-rules entry point in REVIEWER')
    reviewer.write_text(original)
    policy = suite/'.agents/skills/spec-planner/agents/openai.yaml'
    original_policy = policy.read_text()
    policy.write_text(original_policy.replace('allow_implicit_invocation: false', 'allow_implicit_invocation: true'))
    run('Implicit invocation is rejected', 1, 'Invalid invocation policy: spec-planner')
    policy.write_text(original_policy)
    reviewer.write_text(original + '\nAdditional review guidance.\n')
    report = run('Word growth signals review without failing', 0)
    assert report['delta']['instruction_words'] == 3
    assert report['delta']['shared_plus_role_words']['REVIEWER'] == 3
    assert report['review_signals']
    command[-1] = 'missing-baseline'
    proc = subprocess.run(command, text=True, capture_output=True)
    assert proc.returncode == 2 and 'could not complete' in proc.stderr
    results.append({'scenario': 'Unavailable baseline cannot claim PASS', 'exit_code': 2, 'result': 'PASS'})
print(json.dumps(results, indent=2))
