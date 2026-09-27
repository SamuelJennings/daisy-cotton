"""No animated or decorative display component ships a script (SC-003).

Each component is rendered from a caller's template string, with every slot and
modifier the component offers filled in, and the output is checked for a
``<script>`` element and for any ``on*=`` event-handler attribute.
"""

import re

import pytest

EVENT_HANDLER = re.compile(r"\son[a-z]+\s*=", re.IGNORECASE)

CALLER_STRINGS = {
    "carousel": (
        '<c-carousel aria-label="Photos" snap="center" horizontal vertical="md">'
        '<c-carousel.item id="slide1" class="w-full">'
        '<img src="/a.jpg" alt="A"></c-carousel.item>'
        "</c-carousel>"
    ),
}


class TestAnimatedDisplayNoScript:
    """The rendered output of every component carries no script."""

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
