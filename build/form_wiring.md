# Form wiring — demo → production (applied at launch, not in `site/`)

The demo forms in `site/` are intentionally inert (`onsubmit="return false"`,
`action="#"`). The production build step (`build.py` enhancement or a post-step)
rewrites them to POST real leads to the `/api/lead` Pages Function. **Do not edit
`site/` by hand** — these transforms are applied to build output only.

## Forms in scope
| Page | Selector | source value |
|------|----------|--------------|
| `site/index.html` (#contact) | `form.contact-form` | `contact` |
| `site/services/sell-my-house.html` (#home-value) | `form.contact-form` | `valuation` |

## Transform per form
1. Change the tag:
   - `method="post"` (already) and `action="/api/lead"` (was `#`)
   - **remove** `onsubmit="return false"`
2. Enable the submit button on the valuation form (drop `disabled`
   `aria-disabled="true"`; the index button text `Send (demo only)` → `Send`).
3. Add a **honeypot** field the Function checks (`body.company`). Visually and
   from AT it must be hidden and non-focusable:
   ```html
   <input type="text" name="company" tabindex="-1" autocomplete="off"
          class="hp" aria-hidden="true">
   <!-- .hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden} -->
   ```
4. Add a **hidden source** field so leads are attributable per page:
   ```html
   <input type="hidden" name="source" value="contact">   <!-- index -->
   <input type="hidden" name="source" value="valuation"> <!-- sell-my-house -->
   ```

## Success / error UX pattern
Progressive enhancement — the form still works without JS (full-page POST returns
JSON). With JS, intercept submit, POST via `fetch`, and swap in an inline status
region (no `alert`, no PII echo):
```js
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const btn = form.querySelector('[type=submit]');
  btn.disabled = true;
  const status = form.querySelector('.form-status'); // aria-live="polite" region
  try {
    const r = await fetch('/api/lead', { method:'POST', body:new FormData(form) });
    if (r.ok) { form.reset(); status.textContent = "Thanks — Carrie will be in touch shortly."; }
    else if (r.status === 429) status.textContent = "Please wait a moment and try again.";
    else status.textContent = "Something went wrong. Please call 337-258-5379.";
  } catch { status.textContent = "Network error. Please call 337-258-5379."; }
  finally { btn.disabled = false; }
});
```
- Add `<p class="form-status" role="status" aria-live="polite"></p>` after each form.
- On success, **replace** the "Demo form —" caption paragraph.

## Privacy notice (CR-007) — REQUIRED near each form
Add directly under the submit button, before `.form-status`:
```html
<p class="form-privacy"><small>By submitting, you agree to be contacted about
your inquiry. See our <a href="/privacy/">Privacy Policy</a>.</small></p>
```
The build must ensure `/privacy/` exists and is linked; launch gate blocks if the
privacy link 404s.
