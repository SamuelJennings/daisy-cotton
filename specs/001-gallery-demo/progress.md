# Progress: 001-gallery-demo

- 2026-09-26: planning started on branch `001-gallery-demo` off main at the merged specification.

## 2026-09-26T00:00:00Z · Implementer US1 · T002

Did: wrote `tests/test_demo.py` — root redirect, raw-page head-partial assets,
no `EXTRA_CSS`/`EXTRA_JS` configured, and the five host-package apps absent
from `INSTALLED_APPS`.
Verified: `uv run pytest tests/test_demo.py -q` — 7 failed, 2 passed (django-mvp
still installed, gallery not yet mounted in test settings).
Next: T003.
Watch: nothing yet.

## 2026-09-26T00:05:00Z · Implementer US1 · T003

Did: rewrote `tests/settings.py` to stand alone — its own `INSTALLED_APPS`
(including the gallery, which the link test in US2 needs mounted), its own
middleware and context processors, no django-mvp import.
Verified: `uv run pytest tests/settings.py` isn't a test module; ran
`uv run pytest tests/test_demo.py -q` afterward with T004/T005 in place — see
that entry.
Next: T004.
Watch: the gallery's own "MOUNTED AND SERVING" startup notice now fires on
every test run since the gallery is unconditionally in `INSTALLED_APPS` here;
silenced via `filterwarnings` in `pyproject.toml` under T007, where the file
was already being touched.

## 2026-09-26T00:10:00Z · Implementer US1 · T004

Did: rewrote `demo/settings.py` — dropped `mvp`, `flex_menu`, `easy_icons`,
`crispy_forms`, `crispy_tailwind` from `INSTALLED_APPS`, their settings blocks
(`CRISPY_*`, `FLEX_MENUS`, `EASY_ICONS`, `MVP_CONFIG`) and the
`mvp.context_processors.mvp_config` context processor.
Verified: `uv run pytest tests/test_demo.py -q` — `ImportError` importing
`EASY_ICONS` from `demo.settings` in `tests/settings.py` (T003 not yet
resolved at that point in the loop — both landed in the same pass).
Next: T005.
Watch: the ten daisyUI themes that lived in `MVP_CONFIG` had nowhere left to
live; carried them into T006's switcher script instead.

## 2026-09-26T00:15:00Z · Implementer US1 · T005

Did: rewrote `demo/urls.py` — `/` redirects to `django_cotton_gallery:index`
via `RedirectView`, the gallery mounts under `DEBUG`, the custom error
handlers are gone. Deleted `demo/views.py`, `demo/templates/base.html`,
`demo/templates/demo/home.html`.
Verified: `uv run pytest tests/test_demo.py -q` — 8 passed, 1 failed (the raw
page test, since `_extra_head.html` did not exist yet).
Next: T006.
Watch: nothing yet.

## 2026-09-26T00:20:00Z · Implementer US1 · T006

Did: added `demo/templates/django_cotton_gallery/_extra_head.html` (preview
daisyUI 5, daisyUI themes, Tailwind browser 4, Alpine 3, theme bootstrap) and
`_extra_body.html` (theme `<select>` of the ten themes, built only in the
interface page; applies the choice to every preview iframe and persists it to
`localStorage`). Both partials detect "preview document" the same way: inside
an iframe (`window.top !== window`) or the raw page (path ends `/raw/`).
Verified: `uv run pytest tests/test_demo.py -q` — 9 passed. Also verified with
Playwright against the running dev server (not a committed test — browser
behaviour per the brief): interface page loads no daisyUI/Tailwind/Alpine and
shows the theme select; the raw page and every preview iframe load the full
stack and default to light; switching the select updates every iframe's
`data-theme`, persists to `localStorage`, and survives navigating to another
component's page.
Next: T007.
Watch: nothing yet.

## 2026-09-26T00:25:00Z · Implementer US1 · T007

Did: removed `django-mvp>=0.23.0` and its comment from the dev group in
`pyproject.toml`, ran `uv lock` (dropped 7 packages: `django-mvp`,
`django-flex-menus`, `django-easy-icons`, `django-crispy-forms`,
`crispy-tailwind`, `anytree`, `mergedeep`) and `uv sync`. Added
`tests/test_demo.py` and `tests/test_gallery_links.py` (US2, ahead of its own
task) to `[tool.forge.conformance] non-mirror-paths`. Added a `filterwarnings`
entry silencing the gallery's own "MOUNTED AND SERVING" `RuntimeWarning`,
which now fires in every test run per T003's watch note.
Verified: `uv tree` shows none of django-mvp, django-flex-menus,
django-easy-icons, django-crispy-forms or crispy-tailwind — only
`mvp-shared[dev, test]`. `uv run pytest -q` — 158 passed.
Next: story verify.
Watch: the conformance checker's `non-mirror-paths` parser reads both `"` and
`'` as string delimiters, so an apostrophe in a comment between list entries
silently truncates the declared list (my first draft lost both new paths this
way). Wrote the comments without apostrophes instead of filing this against
the kit — out of my story's scope to fix the checker itself; noted here for
the record.

## 2026-09-26T00:30:00Z · Implementer US2 · T009

Did: wrote `tests/test_gallery_links.py`. Collects sidebar links from the
rendered gallery index (`a[data-cg-component]`), fails loudly on an empty
collection, and classifies each link as a folder component by checking
`daisy_cotton/templates/cotton/<path>/index.html` exists while
`<path>.html` does not (spec's own Key Entities definition, mirroring
Cotton's own resolution order). A folder component whose page still 404s is
skipped naming issue #96 (T008); one that returns 200 falls through to the
same assertion as every flat component instead of staying skipped.
Verified: `uv run pytest tests/test_gallery_links.py -q -rs` — 16 passed, 6
skipped (avatar, breadcrumbs, card, dock, dropdown, mockup/code — exactly the
six named in spec.md and decisions.md). Probed the mechanism per craft-tdd
before calling this done: with `_is_folder_component` forced to always
return `False`, `card`'s case fails loudly instead of skipping (confirms the
skip is not silently swallowing a real 404); with a component client
response monkeypatched to 200 for `card`, its case passes without a skip
(confirms a fixed gallery release is not stuck skipped); the empty-collection
guard is a plain `assert`, correct by construction. `uv run pytest -q` — 174
passed, 6 skipped. Full verify green (`forge verify`): conformance, lint,
typecheck, test, build all passed.
Next: story complete.
Watch: nothing.
