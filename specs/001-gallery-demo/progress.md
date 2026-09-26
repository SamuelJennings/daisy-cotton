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

## 2026-09-26T00:35:00Z · Implementer US3 · T010

Did: rewrote README.md's intro, "More land as the need arises" status line,
the daisyUI requirement note and the Prior art paragraph so none names
another project as this package's host, source or consumer.
Verified: `grep -in "mvp\|daisy-cotton-blocks" README.md` — no matches.
Next: T011.
Watch: nothing.

## 2026-09-26T00:37:00Z · Implementer US3 · T011

Did: rewrote CONTEXT.md's Component and Block entries (no reference to a
sibling package), the Demo entry (now describes the gallery-only demo per
FR-012), and the "Component library" deliberately-not-used entry (no longer
names labb or django-mvp by name).
Verified: `grep -in "mvp\|daisy-cotton-blocks\|labb" CONTEXT.md` — no matches.
Next: T012.
Watch: nothing.

## 2026-09-26T00:39:00Z · Implementer US3 · T012

Did: AGENTS.md's Article XII line now says "any host project" rather than
naming django-mvp (its `django-mvp/shared` CI-toolchain reference stays, per
decisions.md). docs/brainstorm.md's "Why this package exists" and prior-art
sections restated without naming django-mvp or daisy-cotton-blocks as a
source or sibling. ADR 0001's "Why" section drops the django-mvp comparison;
django-easy-icons stays in both places purely as an example override.
Verified: `grep -in "mvp\|daisy-cotton-blocks" AGENTS.md docs/brainstorm.md
docs/adr/0001-icon-is-an-extension-point.md` — only AGENTS.md's toolchain
line.
Next: T013.
Watch: nothing.

## 2026-09-26T00:41:00Z · Implementer US3 · T013

Did: rewrote CHANGELOG.md's Unreleased section — dropped "migrated from
django-mvp's own Cotton component library" and the two components-that-
differ-from-django-mvp bullets, restated as plain facts about what this
package ships (`avatar`'s `src`/`placeholder` API, `dropdown`'s CSS-only
positioning, `breadcrumbs.item`'s hook class), dropped the "Removed" section
(nine components that were never in this package and never released), added
a line saying the demo is the component gallery alone.
Verified: `grep -in "mvp\|migrat" CHANGELOG.md` — no matches.
Next: T014.
Watch: merged two `### Changed` headings the edit would otherwise have left
duplicated.

## 2026-09-26T00:43:00Z · Implementer US3 · T014

Did: edited only what T014 authorised — the docstrings in
tests/test_class_attribute_merge.py and tests/test_breadcrumbs_href_attribute.py
(dropped "issue #121 (django-mvp)" / "issue #127" and the
`mvp/templates/cotton/breadcrumbs/item.html` path reference), and the sample
text in tests/test_mockup_code.py (`pip install django-mvp` → `pip install
requests`; no assertion in that test checks the text itself, only
`data-prefix`, so there was no matching assertion to change).
Verified: `uv run pytest tests/test_mockup_code.py
tests/test_breadcrumbs_href_attribute.py tests/test_class_attribute_merge.py
-q` — 16 passed.
Next: T015.
Watch: nothing.

## 2026-09-26T00:45:00Z · Implementer US3 · T015

Did: ran the SC-004 search:
`grep -rniE "mvp|daisy-cotton-blocks" README.md CONTEXT.md AGENTS.md docs/
CHANGELOG.md demo/ tests/ pyproject.toml`.
Result: six hits. Three are the allowed exception —
`AGENTS.md:43` and `pyproject.toml:40,49` name `django-mvp/shared` /
`mvp-shared`, the toolchain repository (decisions.md "What counts as naming
a host or consumer"). The other three are in `tests/test_demo.py` (written
in US1, T002): the class docstring "django-mvp and its chain are gone", the
method name `test_mvp_not_installed`, and the assertion
`"mvp" not in settings.INSTALLED_APPS`. That assertion checks the literal
Django app label of the package being proven absent (FR-004/FR-005/SC-001)
— there is no way to assert an app is not installed without the app's own
label appearing as a string somewhere in the test, and T002's own brief
acceptance criterion is written using that same label. SC-004's search is
mechanical and does not distinguish "naming a host" from "naming what was
removed to prove it's gone", so this does not clean up to a literal zero
outside the two allowed strings. Recorded as a concern rather than resolved
by renaming: renaming the test method/docstring would not remove the
`"mvp"` string literal the assertion itself needs, so it would not actually
satisfy SC-004's letter either, and would cost the test its own honesty
about what it checks for no gain.
Next: story complete.
Watch: see concerns in the completion report.

## 2026-09-26T00:50:00Z · Implementer US4 · T016

Did: added a line next to `<c-alert>` in README.md's Status section stating
`dismissible` and `delay` need Alpine.js on the page, that this package
doesn't ship or load it, and that without Alpine the alert still renders and
reads fine but the dismiss button does nothing and `delay` never fires.
Verified against `daisy_cotton/templates/cotton/alert.html`: `dismissible`
drives `x-data`/`x-show`/`x-transition`, `delay` drives an `x-init` with
`setTimeout` — both Alpine directives, confirming the README claim is
accurate.
Next: T018.
Watch: T017 (spec.md's FR-009 amendment) was already done by Forge before
this run started; confirmed it reads correctly (tracks the defect in this
repository, not upstream) rather than redoing it.

## 2026-09-26T00:52:00Z · Implementer US4 · T018

Did: ran the full verify.
Verified: `forge verify --repo .` — conformance passed, lint passed,
typecheck passed, test passed, build passed (docs skipped, needs --base).
`uv run pytest -q` — 174 passed, 6 skipped (the known folder-component
defect, US2). Worktree clean, nothing uncommitted.
Next: run complete.
Watch: nothing.
