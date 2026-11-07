"""Reproduce measurements for the explicit implementation sessions only (read-only sources)."""
import collections
import datetime
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
manifest = json.loads((HERE / 'sessions.json').read_text())
metadata = {s['id']: s for s in json.loads((HERE / 'source-metadata.json').read_text())}
bounded = {'version': 1, 'descendants': []}
all_tools = collections.Counter()
details = {'scope': 'Original implementation and descendant follow-ups; analysis turn excluded.', 'agents': {}}

def stamp(s):
    return datetime.datetime.fromisoformat(s.replace('Z', '+00:00')).timestamp()

def write(p, data):
    p.write_text(json.dumps(data, indent=2) + '\n')

for ref in [manifest['root']] + manifest['descendants']:
    sid = ref['session_id']
    events = [json.loads(line) for line in Path(ref['path']).open()]
    bounds = {}
    for event in events:
        payload = event.get('payload', {})
        turn = payload.get('turn_id')
        if event['type'] == 'event_msg' and turn in ref['turn_ids']:
            kind = payload.get('type')
            if kind in ('task_started', 'task_complete'):
                bounds.setdefault(turn, {})[kind] = event['timestamp']
    assert all('task_complete' in bounds[t] and 'task_started' in bounds[t] for t in ref['turn_ids'])
    norm = []
    calls, results, items, usage = {}, {}, {}, {}
    by_turn = {}
    for turn, b in bounds.items():
        by_turn[turn] = {'start': b['task_started'], 'end': b['task_complete'], 'duration_seconds': stamp(b['task_complete']) - stamp(b['task_started']), 'tokens': collections.Counter(), 'responses': 0}
        for value in b.values():
            norm.append({'type': 'boundary', 'session_id': sid, 'turn_id': turn, 'timestamp': value})
    for event in events:
        timestamp = event['timestamp']
        turn = next((t for t,b in bounds.items() if b['task_started'] <= timestamp <= b['task_complete']), None)
        if turn is None:
            continue
        payload = event.get('payload', {})
        kind = event['type']
        if kind == 'token_usage_record':
            assert payload['turn_id'] == turn
            response = payload['response_id']
            record = {'type':'usage', 'session_id':sid, 'turn_id':turn, 'timestamp':timestamp, 'response_id':response, 'usage':payload['usage']}
            if response not in usage:
                usage[response] = record
                norm.append(record)
                by_turn[turn]['tokens'].update(payload['usage'])
                by_turn[turn]['responses'] += 1
        if kind == 'response_item' and payload.get('type') in ('function_call', 'custom_tool_call'):
            cid = payload['call_id']
            if cid not in calls:
                calls[cid] = {'name':payload['name'], 'timestamp':timestamp, 'turn':turn, 'input':payload.get('arguments',payload.get('input',''))}
                norm.append({'type':'tool_call', 'session_id':sid, 'turn_id':turn, 'timestamp':timestamp, 'call_id':cid, 'name':payload['name']})
        if kind == 'response_item' and payload.get('type') in ('function_call_output','custom_tool_call_output'):
            results[payload['call_id']] = {'timestamp':timestamp, 'output':payload.get('output')}
        if kind == 'event_msg' and payload.get('type') == 'item_completed' and payload.get('turn_id') in ref['turn_ids']:
            item = payload['item']
            items[item['id']] = (item, payload)
    counts = collections.Counter(c['name'] for c in calls.values())
    all_tools.update(counts)
    waits = []
    for cid,call in calls.items():
        if call['name'] == 'wait_agent' and cid in results:
            output = results[cid]['output']
            if isinstance(output,str):
                output=json.loads(output)
            waits.append({'call_id':cid, 'duration_seconds':stamp(results[cid]['timestamp'])-stamp(call['timestamp']), 'timed_out':output.get('timed_out'), 'turn':call['turn']})
    command_items = [(item,payload) for item,payload in items.values() if item['type']=='CommandExecution']
    failures = []
    for item,payload in command_items:
        if item.get('exit_code',0):
            command=item.get('command',[])
            failures.append({'id':item['id'],'exit_code':item['exit_code'],'command_preview':str(command)[:280]})
    name=metadata[sid]['agent_path'] or '/root'
    details['agents'][name] = {'session_id':sid, 'turns':by_turn, 'tools':dict(counts), 'observed_shell_executions':len(command_items), 'observed_file_change_events':sum(item['type']=='FileChange' for item,p in items.values()), 'agent_message_events':sum(item['type']=='AgentMessage' for item,p in items.values()), 'waits':waits, 'wait_seconds':sum(w['duration_seconds'] for w in waits), 'timed_out_waits':sum(w['timed_out'] is True for w in waits), 'nonzero_shell_exits':failures}
    target=HERE/(sid+'.jsonl')
    target.write_text(''.join(json.dumps(e)+'\n' for e in sorted(norm,key=lambda x:x['timestamp'])))
    selected=dict(ref); selected['path']=str(target.relative_to(ROOT))
    if sid == manifest['root']['session_id']:
        bounded['root']=selected
    else:
        bounded['descendants'].append(selected)

details['tools']=dict(all_tools)
details['wall_clock_seconds']=sum(t['duration_seconds'] for t in details['agents']['/root']['turns'].values())
details['observed_shell_executions']=sum(a['observed_shell_executions'] for a in details['agents'].values())
details['observed_file_change_events']=sum(a['observed_file_change_events'] for a in details['agents'].values())
details['timed_out_waits']=sum(a['timed_out_waits'] for a in details['agents'].values())
details['supervisor_wait_seconds']=details['agents']['/root']['wait_seconds']
checks=[]
for path in HERE.parent.rglob('summary.json'):
    if HERE in path.parents: continue
    summary=json.loads(path.read_text())
    for step in summary.get('steps',[]):
        if step.get('executed'):
            checks.append({'evidence':str(path.relative_to(ROOT)), 'id':step['id'], 'duration_seconds':step['duration_seconds'], 'status':step['status']})
for step in json.loads((HERE.parent/'attempt-0/execution.json').read_text()):
    checks.append({'evidence':'.suite/runs/001-01_business_logic/attempt-0/execution.json', 'id':step['id'], 'duration_seconds':step['elapsed_seconds'], 'status':step['status']})
details['verification_steps']=checks
details['verification_step_count']=len(checks)
details['verification_step_seconds']=sum(c['duration_seconds'] for c in checks)
details['notes']=['Token totals deduplicated by session/response ID; tools by session/call ID.', 'Normalized logs contain only usage, tool identity and turn boundary events from the original sources. No prompt/tool argument content copied.', 'Original helper selected-event spans can include events arriving between task completion and the next task-start. These normalized inputs enforce task_started/task_complete boundaries.', 'Shell and file-change counts come from distinct item_completed UI events; not inferred from executable source text. They occur inside execution batches and must not be added as additional model-facing tool calls.', 'Wait durations overlap child work; neither agent spans nor waits may be summed as overall wall time.', 'Verification step duration includes subprocess setup where that step performs it; nested CLI processes are not additionally added.', 'No billing ledger or actual dollar charge is available. No price estimate made.', 'No external outer-driver session was identified; analysis turn is excluded.']
write(HERE/'bounded-sessions.json',bounded)
write(HERE/'details.json',details)
print(json.dumps({k:v for k,v in details.items() if k not in ('agents','verification_steps','notes')},indent=2))
for name,a in details['agents'].items():
    print(name,'turns',[(round(t['duration_seconds'],3),t['tokens']['total_tokens']) for t in a['turns'].values()],'wait_s',round(a['wait_seconds'],3),'timeouts',a['timed_out_waits'],'shell',a['observed_shell_executions'],'nonzero',a['nonzero_shell_exits'])
