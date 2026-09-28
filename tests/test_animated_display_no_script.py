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
    "chat": (
        '<c-chat placement="end" variant="primary">'
        '<c-slot name="image"><c-avatar src="/a.jpg" alt="Sam" /></c-slot>'
        '<c-slot name="header">Sam</c-slot>'
        '<c-slot name="footer">Delivered</c-slot>'
        "Hello"
        "</c-chat>"
    ),
    "countdown": '<c-countdown value="42" class="font-mono" />',
    "diff": (
        '<c-diff aria-label="Before and after">'
        '<c-slot name="item_1"><img src="/a.jpg" alt="Before"></c-slot>'
        '<c-slot name="item_2"><img src="/b.jpg" alt="After"></c-slot>'
        "</c-diff>"
    ),
    "hover-gallery": (
        '<c-hover-gallery class="max-w-60">'
        '<img src="/a.jpg" alt="A">'
        '<img src="/b.jpg" alt="B">'
        "</c-hover-gallery>"
    ),
    "hover-3d": (
        '<c-hover-3d href="/cards/1"><figure><img src="/a.jpg" alt="A"></figure></c-hover-3d>'
    ),
    "text-rotate": (
        '<c-text-rotate content_class="justify-items-center">'
        "<span>One</span><span>Two</span><span>Three</span>"
        "</c-text-rotate>"
    ),
}


class TestAnimatedDisplayNoScript:
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
