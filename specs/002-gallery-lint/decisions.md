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
