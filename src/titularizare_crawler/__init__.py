from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index():
        return (
            """
            <!doctype html>
            <html lang="en">
            <head>
              <meta charset="utf-8" />
              <meta name="viewport" content="width=device-width, initial-scale=1" />
              <title>titularizare.edu.ro crawler</title>
              <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%23007DD7'/%3E%3Ctext x='32' y='40' font-size='28' text-anchor='middle' fill='white' font-family='Arial,Roboto,sans-serif'%3ET%3C/text%3E%3C/svg%3E">
              <link rel="preconnect" href="https://fonts.googleapis.com">
              <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
              <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
              <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" rel="stylesheet" />
              <script type="module">
                import 'https://esm.sh/@material/web@1.4.1/all.js';
              </script>
              <style>
                :root {
                  color-scheme: dark;
                  --md-sys-color-primary: #8AB4F8;
                  --md-sys-color-surface: #121212;
                  --md-sys-color-surface-variant: #1E1E1E;
                  --md-sys-color-on-surface: #E4E4E7;
                  --md-sys-color-outline: #3F3F46;
                }
                body { font-family: Roboto, system-ui, -apple-system, Segoe UI, Arial, sans-serif; margin: 0; background: var(--md-sys-color-surface); color: var(--md-sys-color-on-surface); }
                .container { max-width: 720px; margin: 12vh auto; padding: 0 16px; }
                .title { font-size: 28px; font-weight: 700; margin-bottom: 24px; letter-spacing: .2px; }
                .card { border-radius: 16px; padding: 20px; border: 1px solid var(--md-sys-color-outline); background: var(--md-sys-color-surface-variant); }
                .helper { color: #9CA3AF; font-size: 14px; margin: 6px 0 14px; display: block; }
                md-menu-anchor { display: inline-block; position: relative; }
                .combo { position: relative; width: 440px; }
                .chips-infield { position: absolute; top: 10px; left: 12px; right: 42px; display: flex; gap: 6px; flex-wrap: wrap; pointer-events: auto; }
                .match { background: rgba(138,180,248,.2); padding: 0 2px; border-radius: 3px; }
                md-menu:not(:defined), md-menu-item:not(:defined) { display: none; }
              </style>
            </head>
            <body>
              <main class="container">
                <div class="title">titularizare.edu.ro crawler</div>
                <div class="card">
                  <span class="helper">Selectează județele (multi-select)</span>
                  <md-menu-anchor id="judeteAnchor">
                    <div class="combo">
                      <md-outlined-text-field id="judeteField" label="Județe" aria-haspopup="listbox" aria-expanded="false" aria-controls="judeteMenu" style="width: 100%;">
                        <md-icon slot="trailing-icon">expand_more</md-icon>
                      </md-outlined-text-field>
                      <div id="chipsInField" class="chips-infield"></div>
                    </div>
                    <md-menu id="judeteMenu"></md-menu>
                  </md-menu-anchor>
                </div>
              </main>
              <script>
                const field = document.getElementById('judeteField');
                const menu = document.getElementById('judeteMenu');
                const anchorEl = document.getElementById('judeteAnchor');
                const chips = document.getElementById('chipsInField');
                let loaded = false;
                let options = [];
                const selected = new Set();

                function formatSummary(maxShown = 3) {
                  const arr = [...selected];
                  if (arr.length === 0) return 'Județe';
                  const shown = arr.slice(0, maxShown).join(', ');
                  const remaining = arr.length - maxShown;
                  return remaining > 0 ? `${shown} +${remaining}` : shown;
                }

                function updateFieldLabel() {
                  field.label = formatSummary(3);
                }

                function renderChips() {
                  chips.innerHTML = '';
                  const maxVisible = 3;
                  const arr = [...selected];
                  arr.slice(0, maxVisible).forEach(code => {
                    const chip = document.createElement('md-input-chip');
                    chip.setAttribute('label', code);
                    chip.removable = true;
                    chip.addEventListener('remove', () => {
                      selected.delete(code);
                      const item = menu.querySelector(`[data-code="${code}"]`);
                      if (item) item.selected = false;
                      renderChips();
                      updateFieldLabel();
                    });
                    chips.appendChild(chip);
                  });
                  const remaining = arr.length - maxVisible;
                  if (remaining > 0) {
                    const more = document.createElement('md-assist-chip');
                    more.setAttribute('label', `+${remaining}`);
                    chips.appendChild(more);
                  }
                  updateFieldLabel();
                }

                function populateMenu(values) {
                  menu.innerHTML = '';
                  // Action items at top as proper menu entries
                  const actionSelectAll = document.createElement('md-menu-item');
                  actionSelectAll.setAttribute('data-action', 'select-all');
                  let actionLabel = document.createElement('div');
                  actionLabel.slot = 'headline';
                  actionLabel.textContent = 'Selectează toate';
                  actionSelectAll.appendChild(actionLabel);
                  actionSelectAll.addEventListener('click', (e) => {
                    e.preventDefault(); e.stopPropagation();
                    values.forEach(code => selected.add(code));
                    menu.querySelectorAll('md-menu-item').forEach(it => { if (it.hasAttribute('data-code')) it.selected = true; });
                    renderChips();
                    // keep open
                    requestAnimationFrame(() => { menu.open = true; });
                  });
                  const actionClear = document.createElement('md-menu-item');
                  actionClear.setAttribute('data-action', 'clear');
                  actionLabel = document.createElement('div');
                  actionLabel.slot = 'headline';
                  actionLabel.textContent = 'Golește selecția';
                  actionClear.appendChild(actionLabel);
                  actionClear.addEventListener('click', (e) => {
                    e.preventDefault(); e.stopPropagation();
                    selected.clear();
                    menu.querySelectorAll('md-menu-item').forEach(it => { if (it.hasAttribute('data-code')) it.selected = false; });
                    renderChips();
                    requestAnimationFrame(() => { menu.open = true; });
                  });
                  menu.appendChild(actionSelectAll);
                  menu.appendChild(actionClear);

                  values.forEach(code => {
                    const item = document.createElement('md-menu-item');
                    item.type = 'checkbox';
                    item.setAttribute('data-code', code);
                    const label = document.createElement('div');
                    label.slot = 'headline';
                    label.textContent = code;
                    label.setAttribute('data-text', code);
                    item.appendChild(label);
                    item.addEventListener('click', (ev) => {
                      ev.preventDefault();
                      ev.stopPropagation();
                      item.selected = !item.selected;
                      if (item.selected) {
                        selected.add(code);
                      } else {
                        selected.delete(code);
                      }
                      renderChips();
                      // keep open (closeOnSelect is disabled below)
                    });
                    menu.appendChild(item);
                  });
                }

                function filterMenu(query) {
                  const q = (query || '').trim().toUpperCase();
                  const items = menu.querySelectorAll('md-menu-item');
                  items.forEach(it => {
                    const code = (it.getAttribute('data-code') || '').toUpperCase();
                    const show = q ? code.includes(q) : true;
                    it.style.display = show ? '' : 'none';
                    const label = it.querySelector('[slot="headline"]');
                    if (label) {
                      const original = label.getAttribute('data-text') || label.textContent || '';
                      if (!q) {
                        label.textContent = original;
                      } else {
                        const idx = original.toUpperCase().indexOf(q);
                        if (idx >= 0) {
                          label.innerHTML = `${original.slice(0, idx)}<span class=\"match\">${original.slice(idx, idx+q.length)}</span>${original.slice(idx+q.length)}`;
                        } else {
                          label.textContent = original;
                        }
                      }
                    }
                  });
                }

                async function ensureLoaded() {
                  if (loaded) return;
                  loaded = true;
                  try {
                    const res = await fetch('/api/judete');
                    if (!res.ok) throw new Error('Network');
                    const data = await res.json();
                    options = data.values || [];
                    populateMenu(options);
                  } catch (e) {
                    loaded = false;
                    console.error(e);
                  }
                }

                (async function initUI(){
                  ensureLoaded();
                  await customElements.whenDefined('md-menu');
                  // Anchor to the text field to avoid surface positioning issues
                  menu.anchorElement = field;
                  try { menu.closeOnSelect = false; } catch(e) {}
                  // Positioning and scroll
                  menu.style.maxHeight = '320px';
                  menu.style.overflowY = 'auto';
                  field.addEventListener('focus', () => {
                    menu.open = true;
                    field.setAttribute('aria-expanded', 'true');
                  });
                  field.addEventListener('click', () => {
                    menu.open = true;
                    field.setAttribute('aria-expanded', 'true');
                  });
                  field.addEventListener('keydown', (e) => {
                    // Open and focus first/last item via keyboard
                    if (e.key === 'ArrowDown' || e.key === 'Enter' || e.key === ' ') {
                      e.preventDefault();
                      menu.open = true;
                      field.setAttribute('aria-expanded', 'true');
                      requestAnimationFrame(() => {
                        const items = Array.from(menu.querySelectorAll('md-menu-item')).filter(it => it.style.display !== 'none');
                        const target = e.key === 'ArrowDown' ? items[0] : items[0];
                        if (target) target.focus();
                      });
                    } else if (e.key === 'ArrowUp') {
                      e.preventDefault();
                      menu.open = true;
                      field.setAttribute('aria-expanded', 'true');
                      requestAnimationFrame(() => {
                        const items = Array.from(menu.querySelectorAll('md-menu-item')).filter(it => it.style.display !== 'none');
                        const target = items[items.length - 1];
                        if (target) target.focus();
                      });
                    }
                  });
                  let filterTimer;
                  field.addEventListener('input', (e) => {
                    const val = e.target.value || '';
                    clearTimeout(filterTimer);
                    filterTimer = setTimeout(() => filterMenu(val), 120);
                  });

                  // Keyboard handling inside menu
                  menu.addEventListener('keydown', (e) => {
                    const activeItem = e.target && e.target.closest ? e.target.closest('md-menu-item') : null;
                    if (e.key === 'Escape') {
                      e.preventDefault();
                      menu.open = false;
                      field.setAttribute('aria-expanded', 'false');
                      field.focus();
                    } else if (e.key === ' ' || e.key === 'Enter') {
                      if (activeItem) {
                        e.preventDefault();
                        const code = activeItem.getAttribute('data-code');
                        activeItem.selected = !activeItem.selected;
                        if (activeItem.selected) {
                          selected.add(code);
                        } else {
                          selected.delete(code);
                        }
                        renderChips();
                      }
                    }
                  });
                  updateFieldLabel();
                })();
              </script>
            </body>
            </html>
            """,
            200,
            {"Content-Type": "text/html; charset=utf-8"},
        )

    @app.get("/api/judete")
    def api_judete():
        from .main import fetch_url  # reuse existing fetch
        from bs4 import BeautifulSoup
        import re

        fallback = [
            "AB","AG","AR","B","BC","BH","BN","BR","BT","BV","BZ","CJ","CL","CS","CT","CV",
            "DB","DJ","GJ","GL","GR","HD","HR","IF","IL","IS","MH","MM","MS","NT","OT",
            "PH","SB","SJ","SM","SV","TL","TM","TR","VL","VN","VS",
        ]

        try:
            html = fetch_url("https://titularizare.edu.ro/2025/generated/files/j/judete.html")
            soup = BeautifulSoup(html, "html.parser")

            hrefs = []
            for tag in soup.select('area[href$="/index.html"], a[href$="/index.html"]'):
                href = (tag.get("href") or "").strip()
                if href:
                    hrefs.append(href)

            codes: list[str] = []
            pattern = re.compile(r"^([A-Z]{1,2})/index\.html$", re.IGNORECASE)
            for href in hrefs:
                m = pattern.match(href)
                if not m:
                    continue
                code = m.group(1).upper()
                if code not in codes:
                    codes.append(code)

            if not codes:
                codes = fallback

            return {"values": codes}
        except Exception as exc:  # noqa: BLE001
            return {"error": str(exc), "values": fallback}, 200

    return app


__all__ = ["create_app"]


