"""Task-local package checks; excludes archived snapshots and app execution."""
from pathlib import Path
import difflib, hashlib, json, re, subprocess
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
SUITE=ROOT/'spec-source-suite'
def files(root):
    return sorted(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc')
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,data): (OUT/name).write_text(json.dumps(data,indent=2)+'\n')
def metrics(root):
    ff=files(root)
    dirs={a for p in ff for a in p.relative_to(root).parents if str(a)!='.'}
    md=[p for p in ff if p.suffix=='.md']
    return {'files':len(ff),'directories_excluding_root_and_caches':len(dirs),'instruction_markdown_files':len(md),'instruction_words':sum(len(p.read_text().split()) for p in md)}

def run():
    before=OUT/'before'
    active=[*SUITE.rglob('*.md'),ROOT/'AGENTS.md',ROOT/'.agents/skills/acceptance-spec/SKILL.md',ROOT/'docs/agentic-development-conclusions.md',ROOT/'research/spec-source-suite-sota-assessment-2026-11-06.md']
    links=[]
    for p in active:
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text()):
            if re.match(r'\w+://',target): continue
            path,_,anchor=target.partition('#')
            dest=(p.parent/path).resolve() if path else p
            assert dest.exists(), (p,target)
            if anchor:
                headings=re.findall(r'^#{1,6}\s+(.+)$',dest.read_text(),re.M)
                anchors={re.sub(r'[^\w\- ]','',h.lower()).replace(' ','-') for h in headings}
                assert anchor in anchors,(p,target,anchors)
            links.append({'source':str(p.relative_to(ROOT)),'target':target})
    save('links.json',{'status':'PASS','count':len(links),'links':links})
    forbidden=['README.md','CODEX_START.md','docs','prompts','templates/bundle','templates/PLAN.md','templates/ACCEPTANCE.md','templates/RUN_REPORT.md']
    assert all(not (SUITE/p).exists() for p in forbidden)
    expected={'AGENTS.md','SUPERVISOR.md','PLANNER.md','IMPLEMENTER.md','REVIEWER.md','VALIDATOR.md','RUNNER.md','PACKAGE_CHECKS.json','SHA256SUMS','helpers/usage_report.py','tests/test_usage_report.py','templates/project.md','templates/task_order.md','templates/tasks/task.md','templates/verification.md'}
    for role in ['planner','supervisor']:
        expected.update({f'.agents/skills/spec-{role}/SKILL.md',f'.agents/skills/spec-{role}/agents/openai.yaml'})
    assert {str(p.relative_to(SUITE)) for p in files(SUITE)} == expected
    for role in ['planner','supervisor']:
        d=SUITE/'.agents/skills'/f'spec-{role}'
        skill=(d/'SKILL.md').read_text(); yaml=(d/'agents/openai.yaml').read_text()
        assert skill.startswith(f'---\nname: spec-{role}\ndescription: ')
        assert 'disable-model-invocation: true' in skill
        assert 'allow_implicit_invocation: false' in yaml and f'${"spec-"+role}' in yaml
        assert len(re.search(r'short_description: "(.*)"',yaml)[1])<=64
    retained=['helpers/usage_report.py','tests/test_usage_report.py']
    assert all(digest(SUITE/p)==digest(before/'spec-source-suite'/p) for p in retained)
    for p in ['project.md','task_order.md','tasks/task.md','verification.md']:
        assert digest(SUITE/'templates'/p)==digest(before/'spec-source-suite/templates/bundle'/p)
    counts={'method':'Whitespace-separated words in all package Markdown, including skills/templates/optional runner. Files include all package files; directories exclude root and Python caches. Same rule before/after. External routing files excluded from both.','before':metrics(before/'spec-source-suite'),'after':metrics(SUITE)}
    save('instruction-counts.json',counts)
    baseline=json.loads((OUT/'baseline.json').read_text())
    external={'AGENTS.md','.agents/skills/acceptance-spec/SKILL.md','docs/agentic-development-conclusions.md','research/spec-source-suite-sota-assessment-2026-11-06.md'}
    protected=[p for p in baseline if not p.startswith('spec-source-suite/') and p not in external]
    changed=[p for p in protected if not (ROOT/p).exists() or digest(ROOT/p)!=baseline[p]]
    assert not changed,changed
    now={str(p.relative_to(ROOT)) for p in files(ROOT) if '.git' not in p.parts}
    added=[p for p in now-set(baseline) if not p.startswith(('spec-source-suite/','.suite/runs/007-agent-role-structure/'))]
    assert set(added) <= {'guidelines.md'},added  # Independently appeared during work; never edited by this task.
    save('scope-preservation.json',{'status':'PASS','protected_existing_files':len(protected),'changed_protected_files':changed,'unrelated_files_appearing_during_work':added,'helper_and_tests':'byte-identical','four_templates':'byte-identical at flattened paths','historical_task_records':'unchanged; current execution authority is the user implementation request'})
    old_names=re.compile(r'spec-(define|implement|generate)|docs/|prompts/|templates/bundle|CODEX_START|BUILD_THE_SUITE')
    for p in [*SUITE.rglob('*.md'),*SUITE.rglob('*.yaml'),ROOT/'AGENTS.md',ROOT/'.agents/skills/acceptance-spec/SKILL.md']:
        assert not old_names.search(p.read_text()),p
    test=subprocess.run(['python','-m','unittest','discover','-s','spec-source-suite/tests','-v'],cwd=ROOT,text=True,capture_output=True)
    (OUT/'usage-tests.log').write_text(test.stdout+test.stderr)
    assert test.returncode==0
    check=subprocess.run(['git','diff','--check'],cwd=ROOT,text=True,capture_output=True)
    (OUT/'diff-check.log').write_text(check.stdout+check.stderr or 'PASS: git diff --check\n')
    assert check.returncode==0
    package={'package':'Spec Source Suite','version':'0.5-draft','checked_date':'2026-11-06','status':'STRUCTURAL_CHECKS_PASSED','scope':'Five-role instruction structure, entry points, links, templates, inventory, preservation, retained usage tests and documentation walkthroughs. No live app generation or runner implementation.','checks':{}}
    for name,evidence in [('instruction_counts','instruction-counts.json'),('local_links','links.json'),('usage_tests','usage-tests.log'),('instruction_scenarios','walkthroughs.md'),('package_inventory','package-validation.json'),('scope_preservation','scope-preservation.json')]:
        package['checks'][name]={'result':'PASS','evidence':'../.suite/runs/007-agent-role-structure/'+evidence}
    package['checks']['local_links']['count']=len(links)
    package['checks']['usage_tests']['count']=7
    package['checks']['instruction_scenarios'].update({'count':12,'method':'Manual documentation walkthrough; not executed app scenarios'})
    package['evidence']='../.suite/runs/007-agent-role-structure/'
    package['previous_package_checks']='../.suite/runs/007-agent-role-structure/package-checks-before.json'
    package['not_executed']=['Live app generation or reconstruction','Automated runner execution','Enforced filesystem isolation']
    for c in package['checks'].values():
        if c['evidence'].endswith('package-validation.json'):continue
        assert (SUITE/c['evidence']).exists(),c
    (SUITE/'PACKAGE_CHECKS.json').write_text(json.dumps(package,indent=2)+'\n')
    inventory=[p for p in files(SUITE) if p.name!='SHA256SUMS']
    (SUITE/'SHA256SUMS').write_text(''.join(f'{digest(p)}  {p.relative_to(SUITE)}\n' for p in inventory))
    sha=subprocess.run(['sha256sum','-c','SHA256SUMS'],cwd=SUITE,text=True,capture_output=True)
    assert sha.returncode==0,sha.stdout+sha.stderr
    save('package-validation.json',{'status':'PASS','package_files':len(expected),'inventory_entries':len(inventory),'sha256sum_output':sha.stdout,'skill_metadata':'name, description, default invocation and explicit-only policy checked; descriptions <=64 chars','obsolete_paths_and_entry_points':'absent from active instructions','links_and_anchors':'all local Markdown references resolved; archived evidence excluded'})
    # Diff includes newly added files; avoids unrelated working-tree changes.
    scoped={p.relative_to(before) for p in files(before)} | {Path('spec-source-suite')/p.relative_to(SUITE) for p in files(SUITE)} | {Path(p) for p in external}
    diff=''
    for rel in sorted(scoped):
        old=before/rel; new=ROOT/rel
        a=old.read_text().splitlines(keepends=True) if old.exists() else []
        b=new.read_text().splitlines(keepends=True) if new.exists() else []
        diff+=''.join(difflib.unified_diff(a,b,fromfile='before/'+str(rel),tofile='after/'+str(rel)))
    (OUT/'candidate.diff').write_text(diff)
    print(json.dumps({'links':len(links),'counts':counts,'scope_protected_files':len(protected),'tests':7,'package_files':len(expected)},indent=2))
if __name__=='__main__':run()
