"""Shared rules across the specialised inputs, tested once per rule.

Parametrised once per rule rather than duplicated per component: no <script>
or on*= handler in the rendered output, and a page context carrying the
component's own declared names leaves its declared defaults in place (model:
tests/test_form_controls.py). Each story extends this module with its own
component's row rather than repeating the rule.
"""

import re

import pytest

EVENT_HANDLER = re.compile(r"\son[a-z]+\s*=", re.IGNORECASE)

# Every attribute the component offers, filled in.
CALLER_STRINGS = {
    "filter": (
        '<c-form.filter name="status" value="Open" label="Status" '
        'reset_label="Clear" variant="primary" size="sm" required disabled '
        'form="search" id="status-filter" class="mb-4" data-testid="f" '
        ":options=\"['Open', 'Closed']\" />"
    ),
}

# The bare component, and a page context naming every declared attribute with
# a value that must not leak into the rendered output.
PAGE_CONTEXT_LEAK = {
    "filter": (
        "<c-form.filter />",
        {
            "options": "leaked-options",
            "value": "leaked-value",
            "name": "leaked-name",
            "label": "leaked-label",
            "reset_label": "leaked-reset-label",
            "variant": "leaked-variant",
            "size": "leaked-size",
            "required": "leaked-required",
            "disabled": "leaked-disabled",
            "form": "leaked-form",
            "class": "leaked-class",
        },
    ),
}


class TestSpecialisedInputsNoScript:
    @pytest.mark.parametrize(
        "source", CALLER_STRINGS.values(), ids=CALLER_STRINGS.keys()
    )
    def test_rendered_output_has_no_script_element(self, cotton_render_string, source):
        assert "<script" not in cotton_render_string(source).lower()

    @pytest.mark.parametrize(
        "source", CALLER_STRINGS.values(), ids=CALLER_STRINGS.keys()
    )
    def test_rendered_output_has_no_event_handler_attribute(
        self, cotton_render_string, source
    ):
        assert not EVENT_HANDLER.search(cotton_render_string(source))


class TestSpecialisedInputsPageContextDoesNotLeak:
    @pytest.mark.parametrize(
        "source_and_context", PAGE_CONTEXT_LEAK.values(), ids=PAGE_CONTEXT_LEAK.keys()
    )
    def test_declared_names_do_not_leak_from_the_page_context(
        self, cotton_render_string, source_and_context
    ):
        source, context = source_and_context
        html = cotton_render_string(source, dict(context))

        for leaked_value in context.values():
            assert leaked_value not in html
