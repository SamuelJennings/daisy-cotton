# Progress: Core form controls

## 2026-09-28T23:14Z · Plan

Did: branch cut from origin/main 6c8464a; verify green on that commit. Re-read the spec against FS-001 to FS-008, which landed after it: no contradiction (D1). Read daisyUI 5.7.46's CSS and class reference for the ten components, and checked through django-cotton 2.7.2 that bare boolean attributes, named slots, list-valued errors and declared defaults behave as the plan needs (research R4). Wrote plan.md, research.md, tasks.md, decisions D1–D4 and the ledger.
Next: design review, then batch 1 (US1 text input, US2 label and fieldset).
Watch: the wrapped input and select send `class` to the wrapper and everything else to the control.
