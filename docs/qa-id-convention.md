# QA ID convention

A proposal for stable, dev-owned locator hooks in the concession-manager-web
frontend, so Playwright locators stop depending on CSS classes, Angular's
auto-generated `id`s, or visible text.

## Current state (verified 2026-07-19)

A full DOM attribute scan of the sign-in page (`https://concessions.roamstay.com`)
found **zero** elements with any `data-testid`, `data-qa*`, `data-cy`, or
similar hook. The only identifiers today are:

- `id="mat-input-ROAMSTAY_CONCESSIONS0"` — Angular Material's
  auto-generated id. **Not safe to rely on**: the number comes from a
  counter that increments globally for every `mat-form-field` instantiated
  in the SPA session, not per-page, so the same field can get a different
  id after navigating around rather than reloading.
- `formcontrolname="email"` — stable and dev-authored (Angular Reactive
  Forms), but only exists on form controls, not buttons/links/headings/etc.

This automation repo has no access to the frontend source, so the QA IDs
below are a **recommendation to hand to the frontend team**, not something
this repo can add itself. In the meantime, `pages/base_page.py`'s
`get_by_qa_id()` helper is already wired up to pick up either attribute the
instant it's added, with no test-code changes — see "How tests consume it"
below.

## Attribute

Recognize **both** `data-qa-id` and `data-testid`, preferring whichever a
given team/component already leans toward rather than mandating a rewrite:

- `data-qa-id` — use for anything new.
- `data-testid` — also honored, since it's the de facto standard for a lot
  of component libraries/tooling and may already be a convention in other
  parts of the app.

Don't add both to the same element — pick one per element to avoid drift
between two IDs that are supposed to mean the same thing.

## Naming convention

```
<page>-<component>-<element-type>
```

- kebab-case throughout.
- `<page>`: the route/screen, e.g. `sign-in`, `dashboard`, `order-history`.
- `<component>`: the specific widget within that page, when there's more
  than one of a kind (e.g. two dialogs on the same page) — omit if the page
  only has one of that element type.
- `<element-type>`: what it is — `input`, `button`, `select`, `heading`,
  `toggle`, `link`, `checkbox`, `radio`, `label`, `modal`, `row`, `tab`,
  `menu-item`, `icon`.

Examples: `sign-in-email-input`, `sign-in-submit-button`,
`order-history-row`, `checkout-modal-confirm-button`.

Keep IDs stable across text/copy changes and locale switches — they should
never be derived from (or duplicate) visible label text.

## Proposed IDs for the sign-in page

| Element | Proposed QA ID |
| --- | --- |
| "Sign In To Roam" heading | `sign-in-heading` |
| Email input | `sign-in-email-input` |
| Password input | `sign-in-password-input` |
| Password visibility toggle | `sign-in-password-visibility-toggle` |
| Language select | `sign-in-language-select` |
| Submit button | `sign-in-submit-button` |

## How tests consume it

`pages/base_page.py` exposes `get_by_qa_id(qa_id, fallback=None)`:

```python
self.email_input = self.get_by_qa_id(
    "sign-in-email-input", fallback=page.locator('[formcontrolname="email"]')
)
```

It matches `[data-qa-id="..."]` or `[data-testid="..."]`, OR'd with the
fallback locator via Playwright's `Locator.or_()`. Today, since neither
attribute exists, every locator resolves through its fallback. Once the
frontend adds `data-qa-id="sign-in-email-input"` (or `data-testid=`) to that
input, the same test code starts matching the real attribute automatically —
no page-object change required. Once every element on a page has its real
QA ID, the fallback can be deleted.

## Rolling this out to new pages

1. Scan the page's DOM for existing `data-qa-id`/`data-testid` attributes
   before writing a new page object (a quick devtools/console check for any
   attribute matching `/(data-)?(qa|test)[-_a-z]*/i` across all elements).
2. Write every locator through `get_by_qa_id()`, using the naming
   convention above for the id even if it doesn't exist in the DOM yet, with
   a CSS/role-based fallback.
3. File the missing QA IDs for that page as a hand-off item to the frontend
   team (this doc's table is the running record — add a section per page).
