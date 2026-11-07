import os, socket, subprocess, uuid
from pathlib import Path
app=Path('/home/vv/ccode/generate-prototype/apps/todolist_rust')
with socket.socket() as s:
    s.bind(('127.0.0.1',0)); port=s.getsockname()[1]
name='todo-validation-'+uuid.uuid4().hex[:12]
env=dict(os.environ, COMPOSE_PROJECT_NAME=name, TODO_DB_PORT=str(port), DATABASE_URL=f'postgres://todo:todo@127.0.0.1:{port}/todo')
print('Documented isolated configuration:',name,port,flush=True)
def run(args):
    print('$ '+' '.join(args),flush=True)
    p=subprocess.run(args,cwd=app,env=env,text=True,capture_output=True,timeout=120)
    print(p.stdout,end='',flush=True); print(p.stderr,end='',flush=True)
    assert p.returncode==0,(args,p.returncode)
    return p.stdout
try:
    run(['docker','compose','up','-d','--wait','db'])
    run(['docker','compose','ps'])
    assert 'TODO commands' in run(['cargo','run','--','help'])
    assert '1' in run(['cargo','run','--','add','Buy milk'])
    assert run(['cargo','run','--','list'])=='1 [ ] Buy milk\n'
    run(['cargo','run','--','complete','1'])
    run(['cargo','run','--','delete','1'])
    sql=['docker','compose','exec','-T','db','psql','-U','todo','-d','todo','-At','-v','ON_ERROR_STOP=1','-c']
    snapshot=run(sql+['SELECT row_to_json(t) FROM tasks t ORDER BY id'])
    assert 'Deleted' in snapshot
    run(['docker','compose','down'])
    run(['docker','compose','up','-d','--wait','db'])
    assert run(sql+['SELECT row_to_json(t) FROM tasks t ORDER BY id'])==snapshot
    assert run(['cargo','run','--','list'])=='No tasks.\n'
    assert run(['cargo','run','--','add','After down/up'])=='Added task 2\n'
    run(sql+['SELECT id, description, added, "update", status FROM tasks ORDER BY id'])
    print('PASS: exact documented startup/help/CRUD/down/up commands, retained row and next ID',flush=True)
finally:
    run(['docker','compose','down','-v'])
    print('Cleaned only owned project '+name,flush=True)
