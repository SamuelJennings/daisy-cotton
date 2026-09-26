# Decisions: FS-002

Ambiguities in issue #11 resolved while writing the spec, with the reasoning behind each choice.

## What "passes the gallery lint" means

**Ambiguous:** whether the rule is only the linter's exit status, or all of Article XVI.

**Chosen:** two checks in the test suite. The first runs the gallery's linter and fails on errors and warnings, not hints. The second covers the parts of Article XVI the linter does not read: exactly one `@description`, a `@slot` wherever the default slot is rendered, and no `{#` comment that spans lines. Every later component group meets both.

**Why:** the linter only compares `@prop` annotations with `<c-vars>`. A template with every prop documented and no description passes it, and so does one whose annotation wraps onto a second line and renders as page text. The issue asks that a component breaking "the documentation contract" fails CI. That contract is Article XVI, so checking only what the linter checks would leave half of it unenforced. Named slots and `@trigger` are left to review: telling a named slot apart from any other undeclared variable is guesswork, and only `modal` needs a trigger today.

## Hints never fail

**Chosen:** hints pass, and no rule is silenced by configuration.

**Why:** Article XVI says so directly. Some hints can't be avoided. `form.field` declares `help-text` and reads `help_text`, and the linter flags the underscore form as undeclared.

## Annotate what exists, change nothing else

**Chosen:** annotations describe each component's attributes as they are on main, internal-looking ones included (`avatar`'s `size_options`, `avatar.group`'s `space_options`). No attribute is renamed, removed or re-typed.

**Why:** bringing each component in line with Article XIV is the job of its group's feature (FS-003 to FS-010). Changing attributes here would leave those features working against a moving target, and it would make this feature's diff a breaking change.

## `form.field`'s attribute-or-slot names

**Chosen:** `label`, `help-text` and `errors` are documented once, as `@prop`, and each description says a named slot of the same name also works. No separate `@slot:name` is added for them.

**Why:** they are declared in `<c-vars>`, so the linter requires a `@prop`. A second annotation under the same name would describe one input twice, and the gallery's reference doesn't say how it treats a prop and a slot that share a name.

## The `form.field` lint error

**Chosen:** reword the comment so it no longer mentions `<c-form.render>`.

**Why:** the linter reads the mention as a call to a component that doesn't exist. The sentence also pointed readers at a form-rendering component in another package, which Article XII rules out. Suppressing the rule would hide the same error in real markup later.

## Where the contributor docs go

**Chosen:** a new `CONTRIBUTING.md` at the repository root, linked from the README.

**Why:** the repository has no contributor guide. The README is written for adopters, and GitHub surfaces `CONTRIBUTING.md` to anyone opening an issue or pull request.

## Boundary with issue #10

**Chosen:** this feature does not touch the demo project. Making the demo the gallery alone and fixing gallery links that return 404 belong to #10.

**Why:** the linter reads the package's templates, not the demo's pages, so this feature needs nothing from #10 and can land in either order.

## D1 — Annotations land before the checks

**Decision:** the annotation stories (US3, US2, US4, US5, US6) are built first and the two suite checks (US7, US1) after them.

**Why:** both checks run over every template. Landed first, they would be red until the last template was annotated, and no story boundary before that could leave the suite green. Landed last, they arrive green, and each proves it can fail through its own tests against scratch templates. Until then the linter's own output is the proof for each annotation story.

**Revisit if:** a later feature adds a check that can be scoped per component from the start.

**ADR:** none — ordering inside this feature, nothing downstream inherits it.

## D2 — The lint check reuses the gallery's scanner and linter functions

**Decision:** `tests/test_gallery_lint.py` discovers components with `django_cotton_gallery.core.catalog.scanner.scan` and lints them with `django_cotton_gallery.core.linter.lint_catalog`, rather than calling the `cotton_lint` command or walking the directory itself.

**Why:** calling the command would need the gallery installed as an app in the test settings, which prints its start-up notice into every run, and its output would have to be parsed back. A hand-written walk would restate the gallery's rule for naming `<dir>/index.html` components. The two functions are pure, need no settings, and lint exactly what `cotton_lint` lints.

**Revisit if:** a gallery release moves or renames either function. The pin is `>=1.0.0,<2`, so that arrives as a deliberate dependency bump.

**ADR:** none — a test-suite implementation choice, recorded here and in the test module.

## D3 — "Rendered output unchanged" means equal after whitespace normalisation

**Decision:** FR-014 and SC-006 are checked by rendering every touched component before and after with the same attributes and comparing the output with runs of whitespace collapsed and both ends stripped, plus the existing tests passing unmodified. For `mockup.code.line`, whose content sits inside `<pre>`, the rendered `<pre …>…</pre>` must also be byte-identical.

**Why:** a `{# … #}` line renders nothing, but the newline after it still reaches the output, so a byte-for-byte comparison would report every annotated template as changed while the markup a browser builds is identical.

**Revisit if:** another component renders its content inside `<pre>` or anywhere else whitespace is visible.

**ADR:** none — how this feature verifies one requirement.

## D4 — Design review applied

**Decision:** all four design-review findings were applied as plan and task edits: the lint check reads every report from one `lint_catalog` call, the annotation stories prove the three rules the annotation check will later enforce, both new test modules are registered in one task, and the render comparison strips both ends and holds `mockup.code.line`'s `<pre>` byte-identical.

**Why:** none needed a spec change, and each was a sentence in `plan.md` or `tasks.md`.

**ADR:** none — review record for this feature.

## D5 — Discovery checks grouped into classes

**Decision:** the two "catalog is not empty" tests written in US7 and US1 were moved into `TestPackageTemplates` and `TestPackageCatalog` during convergence, rather than reopening those stories.

**Why:** the test-structure check requires every test to sit in a `Test<Subject>` class. The fix is a two-line move with no change to what either test asserts.

**ADR:** none — a structural correction inside this feature.

## D6 — One earlier scratch test's source changed with the slot rule

**Decision:** `test_default_slot_rendered_with_annotation_passes` in `tests/test_gallery_annotations.py` now uses `{# @slot — The body. #}` as its scratch source instead of `{# @slot The body. #}`. Its assertion is unchanged.

**Why:** the slot rule now requires a description as the gallery parses it, and the old source has none, so the test would have failed for the behaviour the fix introduces. The new source is the form the fix specifies as passing.

**Revisit if:** the gallery parser's separator changes.

## D6 — The review fix changed one of this feature's own scratch tests

**Decision:** the scratch test for a passing default slot now uses `{# @slot — The body. #}` instead of `{# @slot The body. #}`.

**Why:** the review showed the gallery reads no description from the second form: it takes the text as sample content. The slot rule now requires a description, so that input is meant to fail, and a new test asserts that it does. The test was written earlier in this feature and never ran on main.

**ADR:** none — a correction inside this feature.
