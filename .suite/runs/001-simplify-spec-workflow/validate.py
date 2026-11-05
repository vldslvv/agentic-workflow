"""Structural validation for AC-9; procedural behavior is reviewed separately.

Public boundaries: usable local links, parseable template metadata, unchanged
approved artifacts/index, and a complete checksum inventory. Broken links,
metadata drift, accidental acceptance edits, and stale hashes must fail here.
This is task-local validation, not a workflow runner or an app-generation test.
"""
import argparse
import hashlib
import json
import re
import subprocess
from datetime import date
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[3]
SUITE = ROOT / 'spec-source-suite'
TASK = ROOT / '.agents/tasks/001-simplify-spec-workflow'
parser = argparse.ArgumentParser()
parser.add_argument('--refresh-package', action='store_true')
parser.add_argument('--index-sha256', help='Explicit current index baseline after an authorized staging/relocation change; original approval record stays unchanged.')
args = parser.parse_args()
checks = {}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

class UniqueLoader(yaml.SafeLoader):
    pass

def mapping(loader, node, deep=False):
    pairs = loader.construct_pairs(node, deep=deep)
    result = {}
    for key, value in pairs:
        assert key not in result, f'Duplicate YAML key: {key}'
        result[key] = value
    return result

UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
files = sorted(p for p in SUITE.rglob('*') if p.is_file())
sources = [p for p in files if p.suffix in ('.md', '.yaml')]
extras = [ROOT/'AGENTS.md', ROOT/'.agents/skills/acceptance-spec/SKILL.md']
links = yaml_count = 0
for p in sources + extras:
    s = p.read_text(encoding='utf-8')
    assert s.endswith('\n'), f'Missing final newline: {p}'
    if p.suffix == '.yaml':
        yaml.load(s, Loader=UniqueLoader)
        yaml_count += 1
    if s.startswith('---\n'):
        metadata = yaml.load(s.split('---', 2)[1], Loader=UniqueLoader)
        yaml_count += 1
        assert isinstance(metadata, dict), p
        if p.name == 'SKILL.md':
            assert metadata['name'] and metadata['description'], p
        if p.name == 'SPEC.md':
            assert set(('id','version','status','title','depends_on','shared_contracts')) <= metadata.keys()
            assert metadata['status'] == 'draft' and metadata['depends_on'] == []
    assert len(re.findall(r'^```', s, re.M)) % 2 == 0, f'Unbalanced fences: {p}'
    for dest in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', s):
        if re.match(r'[a-z]+://|mailto:|#', dest):
            continue
        target = dest.split('#', 1)[0].strip('<>')
        assert (p.parent/target).exists(), f'Broken link: {p} -> {dest}'
        links += 1
checks['utf8_and_final_newlines'] = 'PASS'
checks['local_markdown_links'] = {'result':'PASS', 'count':links}
checks['yaml_and_frontmatter'] = {'result':'PASS','count':yaml_count}
checks['code_fences'] = 'PASS'
for p in SUITE.glob('.agents/skills/*/agents/openai.yaml'):
    d = yaml.load(p.read_text(), Loader=UniqueLoader)
    assert d['policy']['allow_implicit_invocation'] is False
    assert ('$'+p.parents[1].name) in d['interface']['default_prompt']
checks['explicit_skill_metadata'] = {'result':'PASS','count':3}
manifest = yaml.safe_load((SUITE/'templates/project.yaml').read_text())
assert manifest['specifications'] == [] and manifest['targets'] == {} and manifest['default_target'] is None
assert manifest['run_policy']['max_repair_attempts'] == 2
assert manifest['run_policy']['isolation_requested'] == 'procedural'
assert manifest['verification']['plan'] is None and 'frozen_inventory' in manifest['verification']
checks['blank_manifest_and_policy_metadata'] = 'PASS'
acceptance = (TASK/'acceptance.md').read_text()
ids = re.findall(r'^\| (AC-\d+) \|', acceptance, re.M)
assert ids == [f'AC-{i}' for i in range(1,10)]
for row in re.findall(r'^\| AC-\d+ \|.*$', acceptance, re.M):
    assert all(cell.strip() for cell in row.split('|')[1:-1])
ids = re.findall(r'^\| (SUITE-\d+) \|', (SUITE/'docs/BUILD_THE_SUITE.md').read_text(), re.M)
assert len(ids) == len(set(ids)) == 18
spec = (SUITE/'templates/SPEC.md').read_text()
assert '<SPEC-ID>-R001' in spec and '<CHECK-ID;' in spec
checks['requirement_tables_and_template_mapping'] = {'result':'PASS','note':'Structural presence/uniqueness; semantic coverage is independently reviewed.'}
approval = json.loads((TASK/'approval.json').read_text())
assert subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT).decode().strip() == approval['baseline_commit']
for name, expected in approval['documents'].items():
    assert digest(TASK/name) == expected, f'Approved document modified: {name}'
assert hashlib.sha256(subprocess.check_output(['git','diff','--cached','--binary'], cwd=ROOT)).hexdigest() == (args.index_sha256 or approval['preexisting_index_sha256'])
checks['approved_artifacts_and_staged_index_integrity'] = 'PASS'
package = {
 'package':'Spec Source Suite','version':'0.2-draft','checked_date':date.today().isoformat(),
 'status':'STRUCTURAL_CHECKS_PASSED','source_document_count':len(sources),'checks':checks,
 'scope':'Instruction-only guidance. Structural checks include repository routing and task artifact integrity; walkthroughs are procedural validation, not app generation.',
 'evidence':'../.suite/runs/001-simplify-spec-workflow/',
 'not_tested':['Installed skill invocation','Automated supervisor or CLI','Actual app generation or regeneration','Sandbox enforcement','Future app acceptance checks']}
if args.refresh_package:
    (SUITE/'PACKAGE_CHECKS.json').write_text(json.dumps(package, indent=2)+'\n')
    inventory = [p for p in files if p.name != 'SHA256SUMS']
    (SUITE/'SHA256SUMS').write_text(''.join(f'{digest(p)}  {p.relative_to(SUITE)}\n' for p in inventory))
else:
    assert json.loads((SUITE/'PACKAGE_CHECKS.json').read_text()) == package, 'Package record stale'
expected_paths = set()
for line in (SUITE/'SHA256SUMS').read_text().splitlines():
    expected, name = line.split('  ',1)
    assert name not in expected_paths, 'Duplicate checksum entry'
    expected_paths.add(name)
    assert digest(SUITE/name) == expected, f'Stale checksum: {name}'
assert expected_paths == {str(p.relative_to(SUITE)) for p in files if p.name != 'SHA256SUMS'}
checks['package_checksums_and_inventory'] = {'result':'PASS','count':len(expected_paths)}
print(json.dumps({'checks':checks,'source_document_count':len(sources)}, indent=2))
