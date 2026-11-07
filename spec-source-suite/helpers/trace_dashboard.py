"""Pure presentation of normalized accounting; no native reads or token arithmetic."""
from html import escape
from usage_report import format_settings

GROUPS = {
    'task': 'Task', 'agent_run': 'Agent run', 'role': 'Role', 'model': 'Model',
    'effort': 'Reasoning effort', 'model_effort': 'Model + effort',
    'task_model_effort': 'Task + model + effort', 'tool': 'Tool', 'task_tool': 'Task + tool',
}
MODEL_GROUPS = {'model', 'effort', 'model_effort', 'task_model_effort'}
TOOL_GROUPS = {'tool', 'task_tool'}


def text(value):
    return escape(str(value) if value is not None else 'Unavailable', quote=True)


def number(value):
    return f'{value:,}' if value is not None else 'Unavailable'


def measurement(metric):
    if metric['total'] is not None:
        return number(metric['total'])
    if metric['known_subtotal'] is not None:
        return f'{number(metric["known_subtotal"])} known · partial'
    return 'Unavailable'


def table(headers, rows, **attrs):
    attributes = ' '.join(f'{key}="{text(value)}"' for key, value in attrs.items())
    head = ''.join(f'<th scope="col">{text(h)}</th>' for h in headers)
    body = ''.join('<tr>' + ''.join(f'<td>{text(c)}</td>' for c in row) + '</tr>' for row in rows)
    if not rows:
        body = f'<tr><td colspan="{len(headers)}">No attributed observations in this selection.</td></tr>'
    return f'<div class="scroll"><table {attributes}><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def render(report, perfetto_url):
    summary = report['summary']
    parts = ['<!doctype html><html lang="en"><meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width,initial-scale=1">',
             '<title>Agent trace insights</title><style>', CSS, '</style><body><main>',
             '<header><div><p class="eyebrow">LOCAL EXECUTION EVIDENCE</p><h1>Agent trace insights</h1>',
             f'<p>{text(report["implementation_id"])}</p></div><nav>',
             f'<a class="button" id="perfetto" href="{text(perfetto_url)}" target="_blank" rel="noreferrer">Open timeline in Perfetto ↗</a>',
             '<a href="usage.json">Download report JSON</a></nav></header>',
             '<p class="notice">Scope: selected sessions and turns only. Rerun <code>make trace</code> to import new evidence. '
             'Known subtotals exclude missing measurements; unavailable is never zero.</p><div class="cards">']
    for label, key in [('Total tokens', 'total_tokens'), ('Input tokens', 'input_tokens'),
                       ('Cached input', 'cached_input_tokens'), ('Output tokens', 'output_tokens'),
                       ('Reasoning output', 'reasoning_output_tokens')]:
        metric = summary['tokens'][key]
        parts.append(f'<article><span>{label}</span><strong>{text(measurement(metric))}</strong>'
                     f'<small>{metric["measured_records"]} measured / {metric["missing_records"]} missing records</small></article>')
    parts += [f'<article><span>Observed tool calls</span><strong>{number(summary["observed_tool_calls"])}</strong>'
              f'<small>{summary["wrapper_calls"]} wrappers · {summary["observed_nested_operations"]} parented nested operations</small></article>',
              '</div><p class="hint">Input includes cache reads and writes; output includes reasoning. These are overlapping breakdowns, '
              'not values to add together. Model measurements represent native usage records, not necessarily all API requests.</p>',
              '<section aria-labelledby="group-title"><h2 id="group-title">Explore usage</h2><div class="controls">',
              '<label>Group by <select id="group">']
    parts += [f'<option value="{name}">{label}</option>' for name, label in GROUPS.items()]
    parts += ['</select></label><label>Find in this table <input id="search" type="search" placeholder="Task, model, tool…"></label>',
              '<span id="matches" aria-live="polite"></span></div>']
    for name, title in GROUPS.items():
        rows = report['groups'][name]
        fields = list(rows[0]['key']) if rows else []
        headers = [f.replace('_', ' ').title() for f in fields]
        values = []
        if name in TOOL_GROUPS:
            headers += ['Observed calls', 'Outcomes', 'Wrapper calls', 'Parented nested', 'Observed duration (s)', 'Timed / untimed']
            for row in rows:
                s = row['summary']
                duration = s['observed_operation_seconds']
                values.append([*row['key'].values(), number(s['observed_tool_calls']),
                               ', '.join(f'{k}: {v}' for k, v in s['outcomes'].items()) or 'Unavailable',
                               s['wrapper_calls'], s['observed_nested_operations'],
                               f'{duration:,.3f}' if duration is not None else 'Unavailable',
                               f'{s["timed_operations"]} / {s["untimed_operations"]}'])
        else:
            metrics = ('total_tokens', 'input_tokens', 'cached_input_tokens', 'uncached_input_tokens',
                       'output_tokens', 'reasoning_output_tokens')
            headers += ['Total tokens', 'Input', 'Cache read', 'Uncached input', 'Output', 'Reasoning', 'Model measurements']
            if name not in MODEL_GROUPS:
                headers += ['Observed tools']
            for row in rows:
                s = row['summary']
                values.append([*row['key'].values(), *(measurement(s['tokens'][m]) for m in metrics),
                               s['observed_model_measurements'],
                               *([] if name in MODEL_GROUPS else [s['observed_tool_calls']])])
        omitted = report['attribution_omissions'][name]
        parts += [f'<div class="group" id="group-{name}"{ " hidden" if name != "task" else ""}>',
                  f'<h3>By {title.lower()}</h3>', table(headers, values),
                  f'<p class="hint">Attribution omitted: {len(omitted["event_ids"])} events; '
                  f'{omitted["diagnostics_without_attribution"]} diagnostics lack this grouping. '
                  'Model/effort tables contain model measurements; tool tables contain tool observations.</p></div>']
    parts += ['<p class="hint">Tool durations sum observed endpoints and may overlap; they are not wall-clock time. '
              '“Returned” means a result was received, not confirmed success. Wrapper calls may contain operations not exposed '
              'by the native source; missing parent-call relationships cannot prove that no nested work occurred.</p></section>',
              '<section><h2>Agents and assignments</h2><p class="hint">Names come from native metadata or workflow bindings. '
              'When a purpose was not recorded, the role and task are shown explicitly as assignment context. '
              'A reused agent can have multiple assignments. Model / effort lists observed native settings; '
              'multiple pairs indicate settings changes, and unavailable values are not inferred from requests.</p>']
    assignments = report['assignments']
    parts.append(table(['Agent', 'Observed model / effort', 'Purpose / assignment', 'Task', 'Role', 'Run', 'Observed status', 'Native path'],
                       [[a['agent_name'], format_settings(a.get('observed_settings', [])),
                         a['purpose'] or f'Assignment: {a["role"] or "unavailable role"} / {a["task_id"] or "unavailable task"}',
                         a['task_id'], a['role'], a['agent_run_id'], ', '.join(a['outcomes']) or 'Unavailable',
                         a['native_agent_path']] for a in assignments], id='assignments'))
    names = {a['agent_id']: f'{a["agent_name"] or a["agent_id"]} [{a["agent_run_id"] or "unassigned"}]' for a in assignments}
    parts += ['<details><summary>Native lineage and identities</summary>',
              table(['Parent', 'Relationship', 'Child'],
                    [[names.get(e['parent'], e['parent']), e['relationship'], names.get(e['child'], e['child'])]
                     for e in report['spawn_tree']['edges']]),
              table(['Agent / run', 'Native identity'], [[name, aid] for aid, name in sorted(names.items())]),
              '</details></section><section><h2>Coverage and interpretation</h2>',
              table(['Diagnostic', 'Occurrences'], list(summary['coverage'].items())),
              '<p>Snapshot exclusions are deliberate deduplication, not missing counters. Other diagnostics may limit totals. '
              'The JSON report includes scoped diagnostics and attribution omissions.</p><ul>']
    parts += [f'<li>{text(limit)}</li>' for limit in report['limitations']]
    parts += ['</ul></section><footer>Perfetto needs internet and may request local-device access. '
              'This summary stays local. Stop its server with Ctrl+C in the owning terminal.</footer>',
              '</main><script>', SCRIPT, '</script></body></html>']
    return ''.join(parts)


CSS = '''
:root{color-scheme:light;font-family:system-ui,sans-serif;color:#203044;background:#f3f6f9}
*{box-sizing:border-box}body{margin:0}main{max-width:1680px;margin:auto;padding:32px}
header{display:flex;justify-content:space-between;gap:24px;align-items:center}h1{margin:0;font-size:30px;letter-spacing:-.7px}
h2{font-size:21px}h3{font-size:16px}.eyebrow{font-size:11px;letter-spacing:2px;color:#45717d;font-weight:700}
nav{display:flex;align-items:center;gap:20px;flex-wrap:wrap}a{color:#096577}.button{background:#126574;color:white;padding:12px 18px;border-radius:6px;text-decoration:none}
.notice{border-left:3px solid #569aac;padding:12px 16px;background:#e7f1f4;font-size:14px}.hint,small,footer{color:#58697a;font-size:13px;line-height:1.6}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(195px,1fr));gap:12px;margin:24px 0 12px}
article,section{background:white;border:1px solid #dbe2e9;border-radius:8px}article{padding:18px}article span,article strong,article small{display:block}article span{font-size:13px}article strong{font-size:24px;margin:8px 0;font-variant-numeric:tabular-nums}
section{padding:22px;margin:24px 0}.controls{display:flex;gap:20px;align-items:end;flex-wrap:wrap;margin-bottom:20px}label{display:grid;gap:7px;font-size:13px;font-weight:600}input,select{padding:9px 12px;border:1px solid #aebdca;border-radius:5px;background:white;color:inherit;font:inherit;min-width:220px}
.scroll{overflow:auto}table{border-collapse:collapse;width:100%;font-size:13px;text-align:left}th{background:#edf2f6;font-weight:600;white-space:nowrap}th,td{padding:12px;border-bottom:1px solid #e1e7ed;vertical-align:top}td{font-variant-numeric:tabular-nums;overflow-wrap:anywhere}tbody tr:hover{background:#f7fafc}summary{cursor:pointer;padding:16px 0;color:#096577}footer{padding-bottom:20px}#matches{font-size:13px;color:#58697a}[hidden]{display:none!important}@media(max-width:720px){main{padding:16px}header{align-items:start;flex-direction:column}section{padding:14px}}
'''

SCRIPT = '''
const group = document.querySelector('#group'), search = document.querySelector('#search');
function update() {
  let shown = 0, total = 0;
  document.querySelectorAll('.group').forEach(panel => {
    panel.hidden = panel.id !== 'group-' + group.value;
    if (!panel.hidden) panel.querySelectorAll('tbody tr').forEach(row => {
      total++;
      row.hidden = !row.textContent.toLowerCase().includes(search.value.toLowerCase());
      if (!row.hidden) shown++;
    });
  });
  document.querySelector('#matches').textContent = shown + ' of ' + total + ' rows';
}
group.addEventListener('change', () => { search.value = ''; update(); });
search.addEventListener('input', update);
update();
'''
