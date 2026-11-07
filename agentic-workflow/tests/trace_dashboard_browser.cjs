// Real Chromium boundary check, invoked by test_trace_view.py when configured.
const { chromium } = require(process.env.PLAYWRIGHT_MODULE);
const assert = require('node:assert/strict');
const fs = require('node:fs');

(async () => {
  const browser = await chromium.launch({headless: true});
  try {
    const page = await browser.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(process.argv[2]);
    await page.locator('#group').selectOption('tool');
    await page.locator('#search').fill('exec_command');
    await page.locator('#native-lineage').evaluate(node => { node.open = true; });
    assert.equal(await page.locator('#group-tool tbody tr:visible').count(), 1);
    await page.locator('#event-kind').selectOption('message');
    await page.locator('#event-agent').selectOption('codex:supervisor');
    await page.locator('#event-task').selectOption('work');
    await page.locator('#event-search').fill('print("snow")');
    await page.waitForFunction(() => document.querySelectorAll('#event-list button').length === 60);
    await page.locator('#event-search').fill('Unicode 雪');
    await page.waitForFunction(() => document.querySelectorAll('#event-list button').length === 60);
    await page.locator('#event-list button').first().click();
    assert.match(await page.locator('#event-detail').textContent(), /Unicode 雪\nprint\("snow"\)\n<\/script><script>globalThis.injected=true<\/script>/);
    assert.equal(await page.evaluate(() => globalThis.injected), undefined);
    const selected = await page.locator('#event-list button[aria-pressed="true"]').getAttribute('data-event-id');
    await page.locator('#event-search').focus();
    await page.evaluate(() => {
      document.querySelector('#event-list').scrollTop = 130;
      document.querySelector('#event-detail').scrollTop = 150;
    });
    fs.appendFileSync(process.argv[3], JSON.stringify({timestamp: 1793959262, type: 'response_item',
      payload: {type: 'message', id: 'browser-refresh', turn_id: 'turn-2', role: 'assistant', content: 'Refresh arrived'}}) + '\n');
    await page.waitForFunction(() => JSON.parse(document.querySelector('#event-data').textContent).events.some(
      event => event.native_record?.id === 'browser-refresh'));
    assert.equal(await page.locator('#group').inputValue(), 'tool');
    assert.equal(await page.locator('#search').inputValue(), 'exec_command');
    assert.equal(await page.locator('#native-lineage').evaluate(node => node.open), true);
    assert.equal(await page.locator('#event-search').inputValue(), 'Unicode 雪');
    assert.equal(await page.locator('#event-kind').inputValue(), 'message');
    assert.equal(await page.locator('#event-agent').inputValue(), 'codex:supervisor');
    assert.equal(await page.locator('#event-task').inputValue(), 'work');
    assert.equal(await page.locator('#event-list button[aria-pressed="true"]').getAttribute('data-event-id'), selected);
    assert.deepEqual(await page.evaluate(() => [document.querySelector('#event-list').scrollTop,
      document.querySelector('#event-detail').scrollTop]), [130, 150]);
    assert.equal(await page.evaluate(() => document.activeElement.id), 'event-search');
    await page.locator('#event-search').fill('Refresh arrived');
    assert.equal(await page.locator('#event-list button').count(), 1);
    await page.locator('#event-list button').click();
    assert.match(await page.locator('#event-detail').textContent(), /Refresh arrived/);
    await page.locator('#event-search').fill('');
    await page.locator('#event-kind').selectOption('tool');
    await page.locator('#event-tool').selectOption('exec_command');
    assert.equal(await page.locator('#event-list button').count(), 1);
    await page.locator('#event-list button').click();
    assert.match(await page.locator('#event-detail').textContent(), /PRIVATE_ARGUMENTS/);
    assert.match(await page.locator('#event-detail').textContent(), /PRIVATE_OUTPUT/);
    assert.deepEqual(errors, []);
    console.log('PASS: content search, filters, selection, refresh, scrolling, focus and inert text');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
