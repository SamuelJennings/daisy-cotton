"""Shared rules across every form control (plan "Shared rules, tested once").

Parametrised once per rule rather than duplicated per component: no <script>
or on*= handler in the rendered output (FR-005, SC-003; model: FS-008's
tests/test_feedback_no_script.py), no aria-invalid or *-error class on a
control the caller gave neither to (FR-006, controls only), and a page
context carrying the component's own declared names leaves its declared
defaults in place (research R4). Each story extends this module with its own
components' rows rather than repeating the rule.
"""

import re

import pytest

EVENT_HANDLER = re.compile(r"\son[a-z]+\s*=", re.IGNORECASE)
ERROR_CLASS = re.compile(r"-error\b")

# Every slot and modifier the component offers, filled in.
CALLER_STRINGS = {
    "input": (
        '<c-form.input type="email" variant="primary" size="lg" ghost name="q" '
        'placeholder="Search">'
        '<c-slot name="start"><span class="label">$</span></c-slot>'
        '<c-slot name="end"><kbd>Enter</kbd></c-slot>'
        "</c-form.input>"
    ),
    "label": (
        '<c-form.label text="Email" floating class="my-label" for="id_email">'
        '<c-form.input placeholder="Email" />'
        "</c-form.label>"
    ),
    "fieldset": (
        '<c-form.fieldset legend="Shipping" description="We never share it." '
        'errors="Pick a shipping option." id="shipping" class="my-fieldset">'
        "<p>Fields</p>"
        "</c-form.fieldset>"
    ),
    "textarea": (
        '<c-form.textarea variant="primary" size="lg" ghost name="bio" rows="3">'
        "Hello"
        "</c-form.textarea>"
    ),
    "select": (
        '<c-form.select variant="primary" size="lg" ghost name="plan">'
        '<c-slot name="start"><span class="label">Plan</span></c-slot>'
        '<c-slot name="end"><kbd>Enter</kbd></c-slot>'
        '<option value="a">A</option>'
        "</c-form.select>"
    ),
    "checkbox": '<c-form.checkbox name="terms" variant="primary" size="sm" checked />',
    "radio": '<c-form.radio name="shipping" value="standard" variant="accent" />',
    "toggle": '<c-form.toggle name="dark_mode" variant="primary" size="lg" checked />',
    "file_input": (
        '<c-form.file-input name="resume" accept=".pdf" variant="primary" size="sm" ghost />'
    ),
    "range": '<c-form.range name="volume" value="40" variant="primary" size="sm" />',
}

# A bare control: no variant and no aria-invalid given, so neither may appear.
NO_OWN_INVALID_STATE = {
    "input": '<c-form.input name="q" />',
    "textarea": '<c-form.textarea name="bio" />',
    "select": '<c-form.select name="plan" />',
    "checkbox": '<c-form.checkbox name="terms" />',
    "radio": '<c-form.radio name="shipping" />',
    "toggle": '<c-form.toggle name="dark_mode" />',
    "file_input": '<c-form.file-input name="resume" />',
    "range": '<c-form.range name="volume" />',
}

# The bare component, and a page context naming every declared attribute with
# a value that must not leak into the rendered output.
PAGE_CONTEXT_LEAK = {
    "input": (
        "<c-form.input />",
        {
            "type": "leaked-type",
            "variant": "leaked-variant",
            "size": "leaked-size",
            "ghost": "leaked-ghost",
            "start": "leaked-start",
            "end": "leaked-end",
            "class": "leaked-class",
        },
    ),
    "label": (
        "<c-form.label />",
        {
            "text": "leaked-text",
            "floating": "leaked-floating",
            "class": "leaked-class",
        },
    ),
    "fieldset": (
        "<c-form.fieldset />",
        {
            "legend": "leaked-legend",
            "description": "leaked-description",
            "errors": "leaked-errors",
            "id": "leaked-id",
            "class": "leaked-class",
        },
    ),
    "textarea": (
        "<c-form.textarea />",
        {
            "variant": "leaked-variant",
            "size": "leaked-size",
            "ghost": "leaked-ghost",
            "class": "leaked-class",
        },
    ),
    "select": (
        "<c-form.select />",
        {
            "variant": "leaked-variant",
            "size": "leaked-size",
            "ghost": "leaked-ghost",
            "start": "leaked-start",
            "end": "leaked-end",
            "class": "leaked-class",
        },
    ),
    "checkbox": (
        "<c-form.checkbox />",
        {
            "variant": "leaked-variant",
            "size": "leaked-size",
            "class": "leaked-class",
        },
    ),
    "radio": (
        "<c-form.radio />",
        {
            "variant": "leaked-variant",
            "size": "leaked-size",
            "class": "leaked-class",
        },
    ),
    "toggle": (
        "<c-form.toggle />",
        {
            "variant": "leaked-variant",
            "size": "leaked-size",
            "class": "leaked-class",
        },
    ),
    "file_input": (
        "<c-form.file-input />",
        {
            "variant": "leaked-variant",
            "size": "leaked-size",
            "ghost": "leaked-ghost",
            "class": "leaked-class",
        },
    ),
    "range": (
        "<c-form.range />",
        {
            "variant": "leaked-variant",
            "size": "leaked-size",
            "vertical": "leaked-vertical",
            "min": "leaked-min",
            "max": "leaked-max",
            "class": "leaked-class",
        },
    ),
}


class TestFormControlsNoScript:
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


class TestFormControlsNoOwnInvalidState:
    @pytest.mark.parametrize(
        "source", NO_OWN_INVALID_STATE.values(), ids=NO_OWN_INVALID_STATE.keys()
    )
    def test_no_aria_invalid_or_error_class_without_the_caller_asking(
        self, cotton_render_string, source
    ):
        html = cotton_render_string(source)
        assert "aria-invalid" not in html
        assert not ERROR_CLASS.search(html)


class TestFormControlsPageContextDoesNotLeak:
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
