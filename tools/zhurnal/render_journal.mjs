import { chromium } from 'playwright';
const [,, dir, ...names] = process.argv;
const b = await chromium.launch({ headless: true });
const pg = await b.newPage();
for (const n of names) {
  await pg.goto('file://' + dir + '/' + n + '.html');
  await pg.evaluate(() => document.fonts.ready);
  await pg.evaluate(() => {
    const mm = 96 / 25.4;
    document.querySelectorAll('table.fill').forEach(t => {
      const p = t.closest('.pg'); const ft = p.querySelector('.ft');
      const rh = parseFloat(t.dataset.rh || '9');
      const tb = t.tBodies[0] || t;
      const ncols = [...t.rows[0].cells].reduce((a, c) => a + (c.colSpan || 1), 0);
      let num = t.dataset.num ? t.rows.length - 1 + 1 : null;
      for (let k = 0; k < 60; k++) {
        const nextEl = t.nextElementSibling; // may be footer or chart
        const room = (nextEl === ft ? ft.getBoundingClientRect().top - 2.5 * mm : ft.getBoundingClientRect().top - 2.5*mm - (()=>{let h=0,e=nextEl;while(e&&e!==ft){const cs=getComputedStyle(e);h+=e.getBoundingClientRect().height+parseFloat(cs.marginTop)+parseFloat(cs.marginBottom);e=e.nextElementSibling}return h})()) - t.getBoundingClientRect().bottom;
        if (room < rh * mm + 1) break;
        const tr = document.createElement('tr'); tr.className = 'rowh';
        for (let i = 0; i < ncols; i++) { const td = document.createElement('td'); if (i === 0) td.style.height = rh + 'mm'; if (i === 0 && num) { td.textContent = String(num); td.className = 'c'; } tr.appendChild(td); }
        if (num) num++;
        tb.appendChild(tr);
      }
    });
  });
  const over = await pg.evaluate(() => [...document.querySelectorAll('.pg')].map((p, i) => {
    const ft = p.querySelector('.ft'); const prev = ft.previousElementSibling;
    const pr = prev.getBoundingClientRect(), fr = ft.getBoundingClientRect(), r = p.getBoundingClientRect();
    return [i + 1, Math.round(fr.top - pr.bottom), p.scrollHeight - p.clientHeight];
  }));
  console.log(n, JSON.stringify(over));
  await pg.pdf({ path: dir + '/' + n + '.pdf', preferCSSPageSize: true, printBackground: true });
}
await b.close();
