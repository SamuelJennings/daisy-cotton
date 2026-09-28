"""No feedback component ships a script (SC-003).

Each component is rendered from a caller's template string, with every slot and
modifier the component offers filled in, and the output is checked for a
``<script>`` element and for any ``on*=`` event-handler attribute.
"""

import re

import pytest

EVENT_HANDLER = re.compile(r"\son[a-z]+\s*=", re.IGNORECASE)

CALLER_STRINGS = {
    "alert": (
        '<c-alert variant="success" icon="bi bi-check" dismissible delay="4000" '
        'class="mt-4">Saved.</c-alert>'
    ),
    "loading": '<c-loading spinner size="sm" label="Saving" class="text-primary" />',
    "tooltip": (
        '<c-tooltip tip="Copy link" placement="bottom end" variant="primary" open '
        'id="copy-hint" class="mt-4"><c-button circle icon="bi bi-share" '
        'aria-label="Share" /></c-tooltip>'
    ),
    "progress": (
        '<c-progress value="40" max="100" variant="primary" label="Upload progress" '
        'class="mt-4" />'
    ),
    "radial-progress": (
        '<c-radial-progress value="70" label="Upload progress" style="color:red;" '
        'class="mt-4"><i class="bi bi-cloud-upload" aria-hidden="true"></i>'
        "</c-radial-progress>"
    ),
    "toast": (
        '<c-toast placement="top center" class="mt-4">'
        '<c-alert variant="info" icon="bi bi-info-circle">New version.</c-alert>'
        '<c-alert variant="warning" dismissible delay="4000">Expiring soon.</c-alert>'
        "</c-toast>"
    ),
}


class TestFeedbackNoScript:
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
