import os, socket, subprocess, uuid
from pathlib import Path
app=Path('/home/vv/ccode/generate-prototype/apps/todolist_rust')
with socket.socket() as sock:
    sock.bind(('127.0.0.1',0)); port=sock.getsockname()[1]
name='todo-review-'+uuid.uuid4().hex[:12]
env=dict(os.environ,TODO_DB_PORT=str(port),DATABASE_URL=f'postgres://todo:todo@127.0.0.1:{port}/todo')
compose=['docker','compose','-p',name,'-f',str(app/'compose.yaml')]
def docker(*args):
    return subprocess.run(compose+list(args),env=env,check=True,text=True,capture_output=True).stdout
def sql(q):
    return docker('exec','-T','db','psql','-U','todo','-d','todo','-At','-v','ON_ERROR_STOP=1','-c',q)
try:
    print(docker('up','-d','--wait','db'))
    print(sql("CREATE TYPE task_status AS ENUM ('Completed','New','Deleted')"))
    print(sql('CREATE TABLE tasks (id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY, description text NOT NULL, added timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP, "update" timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP, status task_status NOT NULL DEFAULT \'Deleted\'); INSERT INTO tasks (description) VALUES (\'preserved\');'))
    for args in (['help'],['add','unexpected write']):
        p=subprocess.run([str(app/'target/debug/todolist_rust'),*args],env=env,capture_output=True,text=True,timeout=12)
        print('Command:',args,'exit:',p.returncode,'stdout:',repr(p.stdout),'stderr:',repr(p.stderr))
    print('Actual incompatible status type:',sql("SELECT data_type FROM information_schema.columns WHERE table_name='tasks' AND column_name='status'"))
    print('Rows after commands:',sql('SELECT id,description,status FROM tasks ORDER BY id'))
finally:
    print(docker('down','-v','--remove-orphans'))
    print('Cleaned owned fixture',name)
