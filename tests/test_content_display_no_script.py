"""No content display component ships a script (SC-003).

Each component is rendered from a caller's template string, with every slot and
modifier the component offers filled in, and the output is checked for a
``<script>`` element and for any ``on*=`` event-handler attribute.
"""

import re

import pytest

EVENT_HANDLER = re.compile(r"\son[a-z]+\s*=", re.IGNORECASE)

CALLER_STRINGS = {
    "accordion": '<c-accordion name="faq" title="Question" arrow open>Answer</c-accordion>',
    "avatar": '<c-avatar src="/p.jpg" alt="Ada" online />',
    "avatar.group": '<c-avatar.group class="-space-x-6"><c-avatar placeholder="AL" /></c-avatar.group>',
    "badge": '<c-badge variant="success" size="sm" soft text="Paid" />',
    "card": (
        '<c-card title="Plan" size="sm" border side="md" image-full>'
        '<c-slot name="figure"><img src="/a.jpg" alt="A"></c-slot>Body'
        '<c-slot name="actions"><c-button text="Go" /></c-slot></c-card>'
    ),
    "collapse": '<c-collapse title="Details" plus open>Content</c-collapse>',
    "kbd": '<c-kbd size="sm" text="Ctrl" />',
    "list": "<c-list><c-list.row><div>Row</div></c-list.row></c-list>",
    "stat.group": (
        '<c-stat.group vertical horizontal="lg"><c-stat title="Downloads" value="31K" desc="Jan">'
        '<c-slot name="figure">F</c-slot><c-slot name="actions">A</c-slot></c-stat></c-stat.group>'
    ),
    "status": '<c-status variant="error" size="lg" label="Down" />',
    "table": (
        '<c-table caption="Invoices" zebra pin-rows pin-cols size="xs">'
        '<tbody><tr><th scope="row">1</th></tr></tbody></c-table>'
    ),
    "timeline": (
        '<c-timeline vertical horizontal="md" compact snap-icon>'
        '<c-timeline.item start="1984" end="Mac" box><c-slot name="middle">M</c-slot>'
        "</c-timeline.item></c-timeline>"
    ),
}


class TestContentDisplayNoScript:
    """The rendered output of every component carries no script."""

    @pytest.mark.parametrize("source", CALLER_STRINGS.values(), ids=CALLER_STRINGS.keys())
    def test_rendered_output_has_no_script_element(self, cotton_render_string, source):
        assert "<script" not in cotton_render_string(source).lower()

    @pytest.mark.parametrize("source", CALLER_STRINGS.values(), ids=CALLER_STRINGS.keys())
    def test_rendered_output_has_no_event_handler_attribute(
        self, cotton_render_string, source
    ):
        assert not EVENT_HANDLER.search(cotton_render_string(source))
